from datetime import datetime
from app.extensions import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cooking_time = db.Column(db.Integer, nullable=False, default=30)
    difficulty = db.Column(db.Enum('简单', '中等', '困难', name='difficulty_enum'), default='简单')
    diet_type = db.Column(db.Enum('减脂', '家常', '儿童餐', '素食', '不限', name='diet_type_enum'), default='家常')
    tags = db.Column(db.JSON, default=list)
    servings = db.Column(db.Integer, default=2)
    nutrition = db.Column(db.JSON, default=dict)
    tips = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    is_ai_generated = db.Column(db.Boolean, default=False)
    prompt_hash = db.Column(db.String(64), nullable=True, index=True)
    status = db.Column(db.Enum('published', 'hidden', 'deleted', name='recipe_status_enum'), default='published', index=True)
    view_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)
    avg_rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ingredients = db.relationship('Ingredient', backref='recipe', lazy='joined',
                                  cascade='all, delete-orphan', order_by='Ingredient.id')
    steps = db.relationship('Step', backref='recipe', lazy='joined',
                            cascade='all, delete-orphan', order_by='Step.step_number')
    favorites = db.relationship('Favorite', backref='recipe', lazy='dynamic',
                                cascade='all, delete-orphan')

    def to_dict(self, include_details=True) -> dict:
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'cookingTime': f'{self.cooking_time}分钟',
            'cooking_time': self.cooking_time,
            'difficulty': self.difficulty,
            'dietType': self.diet_type,
            'diet_type': self.diet_type,
            'tags': self.tags or [],
            'servings': self.servings,
            'nutrition': self.nutrition or {},
            'tips': self.tips,
            'imageUrl': self.image_url,
            'image_url': self.image_url,
            'isAiGenerated': self.is_ai_generated,
            'is_ai_generated': self.is_ai_generated,
            'status': self.status,
            'viewCount': self.view_count,
            'view_count': self.view_count,
            'favoriteCount': self.favorite_count,
            'favorite_count': self.favorite_count,
            'avgRating': self.avg_rating,
            'avg_rating': self.avg_rating,
            'ratingCount': self.rating_count,
            'rating_count': self.rating_count,
            'categoryId': self.category_id,
            'category_id': self.category_id,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'dbId': self.id,
        }
        if include_details:
            result['ingredients'] = [ing.to_dict() for ing in self.ingredients]
            result['steps'] = [s.to_dict() for s in self.steps]
        return result

    def __repr__(self):
        return f'<Recipe {self.title}>'


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(50), nullable=False, default='适量')
    notes = db.Column(db.String(200), default='')

    def to_dict(self) -> dict:
        return {'name': self.name, 'amount': self.amount, 'notes': self.notes or ''}


class Step(db.Model):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)

    def to_dict(self) -> dict:
        return {'stepNumber': self.step_number, 'step_number': self.step_number, 'instruction': self.instruction}


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'recipe_id', name='uq_user_recipe_favorite'),
    )
