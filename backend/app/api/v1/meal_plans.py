"""Meal Plan API endpoints."""
from datetime import date, timedelta
from flask import Blueprint, request, jsonify, g
from app.extensions import db
from app.models.meal_plan import MealPlan, MealPlanEntry
from app.models.recipe import Recipe
from app.utils.decorators import login_required

meal_plans_bp = Blueprint('meal_plans', __name__)


def _get_week_start(date_str: str | None = None) -> date:
    """Get Monday of the week for a given date string, or today."""
    if date_str:
        try:
            d = date.fromisoformat(date_str)
        except (ValueError, TypeError):
            d = date.today()
    else:
        d = date.today()
    return d - timedelta(days=d.weekday())


@meal_plans_bp.route('/', methods=['GET'], strict_slashes=False)
@login_required
def list_plans():
    """List user's meal plans."""
    week_start = request.args.get('week_start')
    if week_start:
        ws = _get_week_start(week_start)
        plan = MealPlan.query.filter_by(user_id=g.user_id, week_start=ws).first()
        if plan:
            return jsonify({'code': 200, 'data': plan.to_dict()}), 200
        return jsonify({'code': 200, 'data': None}), 200

    page = request.args.get('page', 1, type=int)
    query = MealPlan.query.filter_by(user_id=g.user_id)\
        .order_by(MealPlan.week_start.desc())
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    return jsonify({
        'code': 200,
        'data': {
            'items': [p.to_dict(include_recipes=False) for p in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
        },
    }), 200


@meal_plans_bp.route('/', methods=['POST'], strict_slashes=False)
@login_required
def create_plan():
    """Create a new meal plan."""
    data = request.get_json() or {}
    week_start_str = data.get('week_start')

    if week_start_str:
        try:
            ws = date.fromisoformat(week_start_str)
        except (ValueError, TypeError):
            return jsonify({'code': 400, 'message': '无效的日期格式'}), 400
    else:
        ws = _get_week_start()

    # Check for existing plan for the same week
    existing = MealPlan.query.filter_by(user_id=g.user_id, week_start=ws).first()
    if existing:
        return jsonify({'code': 200, 'data': existing.to_dict()}), 200

    plan = MealPlan(
        user_id=g.user_id,
        name=data.get('name', f'{ws.isoformat()} 食谱计划'),
        week_start=ws,
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify({'code': 200, 'data': plan.to_dict()}), 201


@meal_plans_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_plan(id: int):
    """Get a meal plan with all entries."""
    plan = MealPlan.query.get(id)
    if not plan:
        return jsonify({'code': 404, 'message': '计划不存在'}), 404
    if plan.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权访问此计划'}), 403

    return jsonify({'code': 200, 'data': plan.to_dict()}), 200


@meal_plans_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_plan(id: int):
    """Delete a meal plan."""
    plan = MealPlan.query.get(id)
    if not plan:
        return jsonify({'code': 404, 'message': '计划不存在'}), 404
    if plan.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权删除此计划'}), 403

    db.session.delete(plan)
    db.session.commit()
    return jsonify({'code': 200, 'message': '已删除'}), 200


@meal_plans_bp.route('/<int:id>/entries', methods=['POST'])
@login_required
def add_entry(id: int):
    """Add or update a meal plan entry."""
    plan = MealPlan.query.get(id)
    if not plan:
        return jsonify({'code': 404, 'message': '计划不存在'}), 404
    if plan.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权操作此计划'}), 403

    data = request.get_json() or {}
    recipe_id = data.get('recipe_id')
    day_of_week = data.get('day_of_week')
    meal_type = data.get('meal_type')

    if recipe_id is None or day_of_week is None or not meal_type:
        return jsonify({'code': 400, 'message': '缺少必要参数'}), 400

    # Verify recipe exists
    recipe = Recipe.query.get(recipe_id)
    if not recipe or recipe.status == 'deleted':
        return jsonify({'code': 404, 'message': '食谱不存在'}), 404

    # Upsert: remove existing entry for this slot then add
    existing = MealPlanEntry.query.filter_by(
        meal_plan_id=id, day_of_week=day_of_week, meal_type=meal_type
    ).first()
    if existing:
        db.session.delete(existing)
        db.session.flush()

    entry = MealPlanEntry(
        meal_plan_id=id,
        recipe_id=recipe_id,
        day_of_week=day_of_week,
        meal_type=meal_type,
        notes=data.get('notes', ''),
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({'code': 200, 'data': entry.to_dict()}), 201


@meal_plans_bp.route('/<int:id>/entries/<int:entry_id>', methods=['DELETE'])
@login_required
def remove_entry(id: int, entry_id: int):
    """Remove an entry from a meal plan."""
    plan = MealPlan.query.get(id)
    if not plan or plan.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权操作'}), 403

    entry = MealPlanEntry.query.get(entry_id)
    if not entry or entry.meal_plan_id != id:
        return jsonify({'code': 404, 'message': '条目不存在'}), 404

    db.session.delete(entry)
    db.session.commit()
    return jsonify({'code': 200, 'message': '已移除'}), 200
