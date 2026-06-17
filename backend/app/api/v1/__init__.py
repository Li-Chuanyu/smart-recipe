from flask import Flask, Blueprint

def register_blueprints(app: Flask):
    """Register all API v1 blueprints."""
    from app.api.v1.auth import auth_bp
    from app.api.v1.recipes import recipes_bp
    from app.api.v1.community import community_bp
    from app.api.v1.upload import upload_bp
    from app.api.v1.admin import admin_bp
    from app.api.v1.meal_plans import meal_plans_bp
    from app.api.v1.shopping_list import shopping_list_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(recipes_bp, url_prefix='/api/v1/recipes')
    app.register_blueprint(community_bp, url_prefix='/api/v1/community')
    app.register_blueprint(upload_bp, url_prefix='/api/v1/upload')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(meal_plans_bp, url_prefix='/api/v1/meal-plans')
    app.register_blueprint(shopping_list_bp, url_prefix='/api/v1/shopping-lists')
