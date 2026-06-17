"""Recipe API endpoints including AI generation."""
from flask import Blueprint, request, jsonify, g, Response, stream_with_context
from app.extensions import db
from app.models.recipe import Recipe, Ingredient, Step, Favorite
from app.models.rating import Rating
from app.models.admin import Category
from app.services.llm_service import LLMService
from app.services.cache_service import CacheService
from app.extensions import get_redis
from app.utils.decorators import login_required, optional_auth, rate_limit
import json

recipes_bp = Blueprint('recipes', __name__)


def _get_cache_service():
    return CacheService(get_redis())


def _get_llm_service():
    return LLMService(_get_cache_service())


def _paginate(query, page: int = 1, per_page: int = 12):
    """Helper to paginate SQLAlchemy query and return dict."""
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        'items': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'perPage': pagination.per_page,
        'pages': pagination.pages,
    }


# ==================== AI Generation ====================

@recipes_bp.route('/generate', methods=['POST'])
@optional_auth
@rate_limit('ai_generate', max_req=20, window=60)
def generate_recipes():
    """AI recipe generation endpoint."""
    params = request.get_json() or {}

    # Normalize params
    normalized = {
        'ingredients': params.get('ingredients', []),
        'tastePreference': params.get('tastePreference', params.get('taste_preference', '')),
        'cookingTime': params.get('cookingTime', params.get('cooking_time', 30)),
        'dietType': params.get('dietType', params.get('diet_type', '家常')),
        'servings': params.get('servings', 2),
        'recipeCount': params.get('recipeCount', params.get('recipe_count', 2)),
        'additionalNotes': params.get('additionalNotes', params.get('additional_notes', '')),
    }

    model = request.headers.get('X-Model', None)

    llm = _get_llm_service()
    recipes, error = llm.generate(normalized, model=model)

    if error:
        return jsonify({'code': 500, 'message': error}), 500

    # Save generated recipes to database if user is authenticated
    user_id = getattr(g, 'user_id', None)
    if user_id and recipes:
        _save_generated_recipes(recipes, user_id, params)

    return jsonify({
        'code': 200,
        'message': f'成功生成 {len(recipes)} 个食谱',
        'data': recipes,
    }), 200


@recipes_bp.route('/generate/stream', methods=['POST'])
@optional_auth
@rate_limit('ai_generate_stream', max_req=20, window=60)
def generate_recipes_stream():
    """SSE streaming recipe generation."""
    params = request.get_json() or {}
    normalized = {
        'ingredients': params.get('ingredients', []),
        'tastePreference': params.get('tastePreference', ''),
        'cookingTime': params.get('cookingTime', 30),
        'dietType': params.get('dietType', '家常'),
        'servings': params.get('servings', 2),
        'recipeCount': params.get('recipeCount', 2),
        'additionalNotes': params.get('additionalNotes', ''),
    }
    model = request.headers.get('X-Model', None)
    llm = _get_llm_service()

    def generate():
        for chunk in llm.generate_stream(normalized, model=model):
            yield f"data: {json.dumps({'content': chunk})}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        },
    )


def _save_generated_recipes(recipes: list, user_id: int, params: dict):
    """Save AI-generated recipes to database."""
    import hashlib
    prompt_hash = hashlib.md5(
        json.dumps(params, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()

    for r in recipes:
        recipe = Recipe(
            user_id=user_id,
            title=r.get('title', '未命名'),
            description=r.get('description', ''),
            cooking_time=int(r.get('cooking_time', 30)) if 'cooking_time' in r else _parse_time(r.get('cookingTime', '30')),
            difficulty=r.get('difficulty', '中等'),
            diet_type=r.get('dietType', r.get('diet_type', '家常')),
            tags=r.get('tags', []),
            servings=r.get('servings', 2),
            nutrition=r.get('nutrition', {}),
            tips=r.get('tips', ''),
            is_ai_generated=True,
            prompt_hash=prompt_hash,
            status='published',
        )
        db.session.add(recipe)
        db.session.flush()

        for ing in r.get('ingredients', []):
            db.session.add(Ingredient(
                recipe_id=recipe.id,
                name=ing.get('name', ''),
                amount=ing.get('amount', '适量'),
                notes=ing.get('notes', ''),
            ))

        for step in r.get('steps', []):
            db.session.add(Step(
                recipe_id=recipe.id,
                step_number=step.get('stepNumber', step.get('step_number', 1)),
                instruction=step.get('instruction', ''),
            ))

    db.session.commit()


def _parse_time(t: str) -> int:
    """Parse '30分钟' to 30."""
    import re
    match = re.search(r'(\d+)', str(t))
    return int(match.group(1)) if match else 30


# ==================== Recipe CRUD ====================

@recipes_bp.route('/', methods=['GET'])
def list_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perPage', 12, type=int)
    keyword = request.args.get('keyword', '')
    diet_type = request.args.get('dietType', '')
    difficulty = request.args.get('difficulty', '')

    query = Recipe.query.filter(Recipe.status == 'published')

    if keyword:
        query = query.filter(
            db.or_(
                Recipe.title.ilike(f'%{keyword}%'),
                Recipe.tags.cast(db.String).ilike(f'%{keyword}%'),
            )
        )
    if diet_type:
        query = query.filter(Recipe.diet_type == diet_type)
    if difficulty:
        query = query.filter(Recipe.difficulty == difficulty)

    query = query.order_by(Recipe.created_at.desc())
    return jsonify({'code': 200, 'data': _paginate(query, page, per_page)}), 200


@recipes_bp.route('/<int:id>', methods=['GET'])
def get_recipe(id: int):
    recipe = Recipe.query.get(id)
    if not recipe or recipe.status == 'deleted':
        return jsonify({'code': 404, 'message': '食谱不存在'}), 404

    # Increment view count
    recipe.view_count += 1
    db.session.commit()

    # Update Redis view counter
    cache = _get_cache_service()
    cache.increment_view(id)

    return jsonify({'code': 200, 'data': recipe.to_dict()}), 200


@recipes_bp.route('/', methods=['POST'])
@login_required
def create_recipe():
    data = request.get_json()
    recipe = Recipe(
        user_id=g.user_id,
        title=data.get('title', '未命名'),
        description=data.get('description', ''),
        cooking_time=data.get('cooking_time', 30),
        difficulty=data.get('difficulty', '中等'),
        diet_type=data.get('diet_type', '家常'),
        tags=data.get('tags', []),
        servings=data.get('servings', 2),
        nutrition=data.get('nutrition', {}),
        tips=data.get('tips', ''),
        image_url=data.get('image_url', ''),
    )
    db.session.add(recipe)
    db.session.flush()

    for ing in data.get('ingredients', []):
        db.session.add(Ingredient(recipe_id=recipe.id, name=ing.get('name', ''), amount=ing.get('amount', '适量'), notes=ing.get('notes', '')))

    for step in data.get('steps', []):
        db.session.add(Step(recipe_id=recipe.id, step_number=step.get('step_number', 1), instruction=step.get('instruction', '')))

    db.session.commit()
    return jsonify({'code': 200, 'data': recipe.to_dict()}), 201


@recipes_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_recipe(id: int):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({'code': 404, 'message': '食谱不存在'}), 404
    if recipe.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权修改此食谱'}), 403

    data = request.get_json()
    for field in ['title', 'description', 'cooking_time', 'difficulty', 'diet_type', 'tags', 'servings', 'nutrition', 'tips', 'image_url']:
        if field in data:
            setattr(recipe, field, data[field])

    db.session.commit()
    return jsonify({'code': 200, 'data': recipe.to_dict()}), 200


@recipes_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_recipe(id: int):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({'code': 404, 'message': '食谱不存在'}), 404
    if recipe.user_id != g.user_id:
        return jsonify({'code': 403, 'message': '无权删除此食谱'}), 403

    recipe.status = 'deleted'
    db.session.commit()
    return jsonify({'code': 200, 'message': '已删除'}), 200


# ==================== Favorites ====================

@recipes_bp.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    page = request.args.get('page', 1, type=int)
    query = Recipe.query.join(Favorite, Favorite.recipe_id == Recipe.id)\
        .filter(Favorite.user_id == g.user_id, Recipe.status != 'deleted')\
        .order_by(Favorite.created_at.desc())
    return jsonify({'code': 200, 'data': _paginate(query, page)}), 200


@recipes_bp.route('/<int:id>/favorite', methods=['POST'])
@login_required
def add_favorite(id: int):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({'code': 404, 'message': '食谱不存在'}), 404

    existing = Favorite.query.filter_by(user_id=g.user_id, recipe_id=id).first()
    if existing:
        return jsonify({'code': 200, 'message': '已收藏'}), 200

    db.session.add(Favorite(user_id=g.user_id, recipe_id=id))
    recipe.favorite_count = (recipe.favorite_count or 0) + 1
    db.session.commit()
    return jsonify({'code': 200, 'message': '已收藏'}), 200


@recipes_bp.route('/<int:id>/favorite', methods=['DELETE'])
@login_required
def remove_favorite(id: int):
    fav = Favorite.query.filter_by(user_id=g.user_id, recipe_id=id).first()
    if fav:
        db.session.delete(fav)
        recipe = Recipe.query.get(id)
        if recipe:
            recipe.favorite_count = max((recipe.favorite_count or 1) - 1, 0)
        db.session.commit()
    return jsonify({'code': 200, 'message': '已取消收藏'}), 200


# ==================== Ratings ====================

def _recalc_recipe_rating(recipe_id: int):
    """Recalculate and update avg_rating and rating_count for a recipe."""
    result = db.session.query(
        db.func.avg(Rating.score),
        db.func.count(Rating.id),
    ).filter(Rating.recipe_id == recipe_id).first()

    recipe = Recipe.query.get(recipe_id)
    if recipe:
        recipe.avg_rating = round(float(result[0] or 0), 1)
        recipe.rating_count = int(result[1] or 0)
        db.session.commit()


@recipes_bp.route('/<int:id>/rate', methods=['POST'])
@login_required
def rate_recipe(id: int):
    """Create or update a rating for a recipe."""
    recipe = Recipe.query.get(id)
    if not recipe or recipe.status == 'deleted':
        return jsonify({'code': 404, 'message': '食谱不存在'}), 404

    data = request.get_json()
    score = data.get('score', 0)
    if not isinstance(score, int) or score < 1 or score > 5:
        return jsonify({'code': 400, 'message': '评分必须是 1-5 的整数'}), 400

    # Upsert rating
    rating = Rating.query.filter_by(user_id=g.user_id, recipe_id=id).first()
    if rating:
        rating.score = score
        rating.updated_at = db.func.now()
    else:
        rating = Rating(user_id=g.user_id, recipe_id=id, score=score)
        db.session.add(rating)

    db.session.commit()
    _recalc_recipe_rating(id)

    recipe = Recipe.query.get(id)
    return jsonify({
        'code': 200,
        'message': '评分成功',
        'data': {
            'avg_rating': recipe.avg_rating,
            'avgRating': recipe.avg_rating,
            'rating_count': recipe.rating_count,
            'ratingCount': recipe.rating_count,
            'user_score': score,
            'userScore': score,
        },
    }), 200


@recipes_bp.route('/<int:id>/my-rating', methods=['GET'])
@login_required
def get_my_rating(id: int):
    """Get current user's rating for a recipe."""
    rating = Rating.query.filter_by(user_id=g.user_id, recipe_id=id).first()
    return jsonify({
        'code': 200,
        'data': {'score': rating.score if rating else None},
    }), 200


@recipes_bp.route('/<int:id>/rate', methods=['DELETE'])
@login_required
def delete_rating(id: int):
    """Remove user's rating from a recipe."""
    rating = Rating.query.filter_by(user_id=g.user_id, recipe_id=id).first()
    if not rating:
        return jsonify({'code': 404, 'message': '未找到评分记录'}), 404

    db.session.delete(rating)
    db.session.commit()
    _recalc_recipe_rating(id)

    recipe = Recipe.query.get(id)
    return jsonify({
        'code': 200,
        'message': '已取消评分',
        'data': {
            'avg_rating': recipe.avg_rating,
            'avgRating': recipe.avg_rating,
            'rating_count': recipe.rating_count,
            'ratingCount': recipe.rating_count,
        },
    }), 200


# ==================== Categories ====================

@recipes_bp.route('/categories', methods=['GET'])
def list_categories():
    cats = Category.query.order_by(Category.sort_order).all()
    return jsonify({'code': 200, 'data': [c.to_dict() for c in cats]}), 200
