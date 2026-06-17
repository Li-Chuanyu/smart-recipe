"""Shopping List API endpoints."""
import re
from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.shopping_list import ShoppingList, ShoppingItem
from app.models.recipe import Recipe
from app.models.meal_plan import MealPlan
from app.utils.decorators import login_required

shopping_list_bp = Blueprint('shopping_list', __name__)

# Ingredient-to-category keyword mapping
CATEGORY_RULES = [
    ('肉类', r'肉|鸡|鸭|鱼|虾|蟹|贝|牛|猪|羊|排骨|培根|香肠|腊|火腿'),
    ('蔬菜', r'菜|白菜|青菜|菠菜|生菜|油麦菜|番茄|西红柿|土豆|萝卜|黄瓜|茄子|豆角|青椒|辣椒|洋葱|西兰花|花菜|芹菜|玉米|南瓜|冬瓜|苦瓜|丝瓜|蘑菇|香菇|木耳|藕|笋|葱|姜|蒜|香菜|韭菜'),
    ('调料', r'盐|糖|酱油|醋|料酒|生抽|老抽|蚝油|味精|鸡精|胡椒|花椒|辣椒|豆瓣|甜面|番茄酱|沙拉|麻油|香油|橄榄油|食用油|油$|淀粉|生粉|酵母|苏打'),
    ('主食', r'米|面|粉|面包|馒头|饼|面条|饺子|馄饨|饭|年糕|粉丝|意面|意大|pasta|noodle|rice'),
    ('乳制品', r'奶|牛奶|酸奶|黄油|芝士|奶油|奶酪|炼乳|淡奶'),
    ('蛋类', r'蛋|鸡蛋|鸭蛋|鹌鹑'),
    ('豆制品', r'豆腐|豆皮|豆浆|豆干|腐竹|千张|豆泡|毛豆|黄豆'),
]


def _classify_ingredient(name: str) -> str:
    """Classify an ingredient name into a category."""
    for category, pattern in CATEGORY_RULES:
        if re.search(pattern, name):
            return category
    return '其他'


def _merge_and_classify(ingredients_list: list[list[dict]]) -> list[dict]:
    """
    Merge ingredients from multiple recipes.
    Returns list of {name, amount, category} dicts sorted by category.
    """
    merged: dict[str, dict] = {}

    for ings in ingredients_list:
        for ing in ings:
            name = ing.get('name', '').strip()
            amount = ing.get('amount', '适量').strip()
            if not name:
                continue

            if name in merged:
                # Try to combine amounts
                existing = merged[name]['amount']
                merged[name]['amount'] = _combine_amounts(existing, amount)
            else:
                merged[name] = {
                    'name': name,
                    'amount': amount,
                    'category': _classify_ingredient(name),
                }

    # Sort by category then name
    category_order = {cat: i for i, (cat, _) in enumerate(CATEGORY_RULES)}
    result = sorted(merged.values(), key=lambda x: (category_order.get(x['category'], 99), x['name']))
    return result


def _combine_amounts(a: str, b: str) -> str:
    """Try to combine two amount strings. If numeric, sum; otherwise join."""
    if a == b:
        return a
    if a == '适量':
        return b
    if b == '适量':
        return a

    # Try extract numbers
    num_a = re.findall(r'[\d.]+', a)
    num_b = re.findall(r'[\d.]+', b)
    if num_a and num_b:
        try:
            total = float(num_a[0]) + float(num_b[0])
            unit_match = re.search(r'[^\d.]+', a)
            unit = unit_match.group(0) if unit_match else ''
            return f'{total:.0f}{unit}' if total == int(total) else f'{total:.1f}{unit}'
        except ValueError:
            pass

    return f'{a}、{b}'


# ==================== CRUD ====================

@shopping_list_bp.route('/', methods=['GET'])
@login_required
def list_shopping_lists():
    """List user's shopping lists."""
    query = ShoppingList.query.filter_by(user_id=g.user_id)\
        .order_by(ShoppingList.created_at.desc())
    lists = query.all()
    # Return without items for list view
    result = []
    for lst in lists:
        d = lst.to_dict()
        d['itemCount'] = len(lst.items)
        d['item_count'] = len(lst.items)
        d['checkedCount'] = sum(1 for i in lst.items if i.checked)
        d['checked_count'] = sum(1 for i in lst.items if i.checked)
        result.append(d)
    return jsonify({'code': 200, 'data': result}), 200


@shopping_list_bp.route('/', methods=['POST'])
@login_required
def create_shopping_list():
    """Create a new empty shopping list."""
    data = request.get_json() or {}
    lst = ShoppingList(
        user_id=g.user_id,
        name=data.get('name', '购物清单'),
    )
    db.session.add(lst)
    db.session.commit()
    return jsonify({'code': 200, 'data': lst.to_dict()}), 201


@shopping_list_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_shopping_list(id: int):
    """Get shopping list with items."""
    lst = ShoppingList.query.get(id)
    if not lst:
        return jsonify({'code': 404, 'message': '购物清单不存在'}), 404
    if lst.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权访问'}), 403
    return jsonify({'code': 200, 'data': lst.to_dict()}), 200


@shopping_list_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_shopping_list(id: int):
    """Delete shopping list."""
    lst = ShoppingList.query.get(id)
    if not lst:
        return jsonify({'code': 404, 'message': '购物清单不存在'}), 404
    if lst.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权操作'}), 403

    db.session.delete(lst)
    db.session.commit()
    return jsonify({'code': 200, 'message': '已删除'}), 200


@shopping_list_bp.route('/<int:id>/items/<int:item_id>/check', methods=['PUT'])
@login_required
def toggle_check(id: int, item_id: int):
    """Toggle checked state of an item."""
    lst = ShoppingList.query.get(id)
    if not lst or lst.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权操作'}), 403

    item = ShoppingItem.query.get(item_id)
    if not item or item.shopping_list_id != id:
        return jsonify({'code': 404, 'message': '条目不存在'}), 404

    item.checked = not item.checked
    db.session.commit()
    return jsonify({'code': 200, 'data': item.to_dict()}), 200


@shopping_list_bp.route('/<int:id>/items/<int:item_id>', methods=['DELETE'])
@login_required
def remove_item(id: int, item_id: int):
    """Remove an item from the list."""
    lst = ShoppingList.query.get(id)
    if not lst or lst.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权操作'}), 403

    item = ShoppingItem.query.get(item_id)
    if not item or item.shopping_list_id != id:
        return jsonify({'code': 404, 'message': '条目不存在'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'code': 200, 'message': '已删除'}), 200


# ==================== Generation ====================

@shopping_list_bp.route('/generate-from-meal-plan', methods=['POST'])
@login_required
def generate_from_meal_plan():
    """Generate shopping list from a meal plan."""
    data = request.get_json() or {}
    meal_plan_id = data.get('meal_plan_id')

    if not meal_plan_id:
        return jsonify({'code': 400, 'message': '请提供 meal_plan_id'}), 400

    plan = MealPlan.query.get(meal_plan_id)
    if not plan or plan.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权访问此计划'}), 403

    # Collect all ingredients from all recipes in the plan
    all_ingredients = []
    for entry in plan.entries:
        recipe = Recipe.query.get(entry.recipe_id)
        if recipe and recipe.status != 'deleted':
            all_ingredients.append([
                {'name': ing.name, 'amount': ing.amount}
                for ing in recipe.ingredients
            ])

    if not all_ingredients:
        return jsonify({'code': 400, 'message': '该食谱计划中没有食谱'}), 400

    # Merge and classify
    merged = _merge_and_classify(all_ingredients)

    # Create shopping list
    lst = ShoppingList(
        user_id=g.user_id,
        name=data.get('list_name', f'{plan.name} - 采购清单'),
        source_type='meal_plan',
        source_id=meal_plan_id,
    )
    db.session.add(lst)
    db.session.flush()

    for i, item_data in enumerate(merged):
        db.session.add(ShoppingItem(
            shopping_list_id=lst.id,
            name=item_data['name'],
            amount=item_data['amount'],
            category=item_data['category'],
            sort_order=i,
        ))

    db.session.commit()
    return jsonify({'code': 200, 'data': lst.to_dict()}), 201


@shopping_list_bp.route('/generate-from-recipes', methods=['POST'])
@login_required
def generate_from_recipes():
    """Generate shopping list from selected recipes."""
    data = request.get_json() or {}
    recipe_ids = data.get('recipe_ids', [])

    if not recipe_ids or not isinstance(recipe_ids, list):
        return jsonify({'code': 400, 'message': '请提供 recipe_ids 数组'}), 400

    all_ingredients = []
    for rid in recipe_ids:
        recipe = Recipe.query.get(rid)
        if recipe and recipe.status != 'deleted':
            all_ingredients.append([
                {'name': ing.name, 'amount': ing.amount}
                for ing in recipe.ingredients
            ])

    if not all_ingredients:
        return jsonify({'code': 400, 'message': '所选食谱中没有食材'}), 400

    merged = _merge_and_classify(all_ingredients)

    lst = ShoppingList(
        user_id=g.user_id,
        name=data.get('list_name', '自选食谱采购清单'),
        source_type='recipes',
    )
    db.session.add(lst)
    db.session.flush()

    for i, item_data in enumerate(merged):
        db.session.add(ShoppingItem(
            shopping_list_id=lst.id,
            name=item_data['name'],
            amount=item_data['amount'],
            category=item_data['category'],
            sort_order=i,
        ))

    db.session.commit()
    return jsonify({'code': 200, 'data': lst.to_dict()}), 201
