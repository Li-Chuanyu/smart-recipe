from datetime import datetime, date
from app.extensions import db

class MealPlan(db.Model):
    __tablename__ = 'meal_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), default='本周食谱计划')
    week_start = db.Column(db.Date, nullable=False)  # Monday of the week
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    entries = db.relationship('MealPlanEntry', backref='meal_plan', lazy='joined',
                               cascade='all, delete-orphan',
                               order_by='MealPlanEntry.day_of_week, MealPlanEntry.meal_type')

    def to_dict(self, include_recipes: bool = True) -> dict:
        result = {
            'id': self.id,
            'userId': self.user_id,
            'user_id': self.user_id,
            'name': self.name,
            'weekStart': self.week_start.isoformat() if self.week_start else None,
            'week_start': self.week_start.isoformat() if self.week_start else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_recipes:
            result['entries'] = [e.to_dict() for e in self.entries]
        return result


class MealPlanEntry(db.Model):
    __tablename__ = 'meal_plan_entries'

    id = db.Column(db.Integer, primary_key=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plans.id'), nullable=False, index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Mon ... 6=Sun
    meal_type = db.Column(db.Enum('breakfast', 'lunch', 'dinner', name='meal_type_enum'), nullable=False)
    notes = db.Column(db.String(200), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('meal_plan_id', 'day_of_week', 'meal_type',
                           name='uq_plan_day_meal'),
    )

    recipe = db.relationship('Recipe', lazy='joined')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'mealPlanId': self.meal_plan_id,
            'meal_plan_id': self.meal_plan_id,
            'recipeId': self.recipe_id,
            'recipe_id': self.recipe_id,
            'recipe': self.recipe.to_dict() if self.recipe else None,
            'dayOfWeek': self.day_of_week,
            'day_of_week': self.day_of_week,
            'mealType': self.meal_type,
            'meal_type': self.meal_type,
            'notes': self.notes or '',
        }
