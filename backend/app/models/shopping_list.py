from datetime import datetime
from app.extensions import db

class ShoppingList(db.Model):
    __tablename__ = 'shopping_lists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), default='购物清单')
    source_type = db.Column(db.Enum('manual', 'meal_plan', 'recipes', name='shopping_source_enum'), default='manual')
    source_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('ShoppingItem', backref='shopping_list', lazy='joined',
                             cascade='all, delete-orphan',
                             order_by='ShoppingItem.category, ShoppingItem.sort_order, ShoppingItem.name')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'userId': self.user_id,
            'user_id': self.user_id,
            'name': self.name,
            'sourceType': self.source_type,
            'source_type': self.source_type,
            'sourceId': self.source_id,
            'source_id': self.source_id,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.to_dict() for item in self.items],
        }


class ShoppingItem(db.Model):
    __tablename__ = 'shopping_items'

    id = db.Column(db.Integer, primary_key=True)
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_lists.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(50), default='')
    category = db.Column(db.String(50), default='其他')
    checked = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'shoppingListId': self.shopping_list_id,
            'name': self.name,
            'amount': self.amount or '',
            'category': self.category or '其他',
            'checked': self.checked,
            'sortOrder': self.sort_order,
            'sort_order': self.sort_order,
        }
