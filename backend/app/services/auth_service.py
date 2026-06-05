from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
from app.extensions import db, get_redis
from app.models.user import User

class AuthService:
    @staticmethod
    def register(username: str, email: str, password: str) -> tuple[dict | None, str | None]:
        """Register a new user. Returns (user_dict, error)."""
        if User.query.filter_by(email=email).first():
            return None, '该邮箱已被注册'
        if User.query.filter_by(username=username).first():
            return None, '该用户名已被使用'

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), None

    @staticmethod
    def login(email: str, password: str) -> tuple[dict | None, str | None]:
        """Authenticate user and return tokens. Returns (tokens_dict, error)."""
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return None, '邮箱或密码错误'
        if not user.is_active:
            return None, '账号已被禁用'

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'expires_in': 7200,  # 2 hours
        }, None

    @staticmethod
    def logout(jti: str, exp_timestamp: int):
        """Add token JTI to Redis blacklist."""
        redis = get_redis()
        if redis:
            ttl = max(1, int(exp_timestamp - __import__('time').time()))
            redis.setex(f"session:bl:{jti}", ttl, "1")

    @staticmethod
    def is_token_blacklisted(jti: str) -> bool:
        redis = get_redis()
        if not redis:
            return False
        return redis.exists(f"session:bl:{jti}") > 0

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        return User.query.get(user_id)
