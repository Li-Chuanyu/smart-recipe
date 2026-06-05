from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import redis

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
redis_client: redis.Redis | None = None

def init_redis(app):
    global redis_client
    redis_url = app.config.get('REDIS_URL', '')
    if redis_url:
        try:
            redis_client = redis.Redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
            )
            redis_client.ping()
        except Exception:
            redis_client = None
    return redis_client

def get_redis():
    return redis_client
