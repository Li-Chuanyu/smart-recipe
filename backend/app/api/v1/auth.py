"""Authentication API endpoints."""
from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.auth_service import AuthService
from app.models.user import User
from app.utils.decorators import login_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'code': 400, 'message': '请填写所有必填字段'}), 400
    if len(username) < 2 or len(username) > 20:
        return jsonify({'code': 400, 'message': '用户名需要 2-20 个字符'}), 400
    if len(password) < 6:
        return jsonify({'code': 400, 'message': '密码需要至少 6 位'}), 400

    user, error = AuthService.register(username, email, password)
    if error:
        return jsonify({'code': 409, 'message': error}), 409

    return jsonify({'code': 200, 'message': '注册成功', 'data': user}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'code': 400, 'message': '请填写邮箱和密码'}), 400

    tokens, error = AuthService.login(email, password)
    if error:
        return jsonify({'code': 401, 'message': error}), 401

    return jsonify({'code': 200, 'message': '登录成功', 'data': tokens}), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = User.query.get(int(identity))
    if not user:
        return jsonify({'code': 401, 'message': '用户不存在'}), 401

    from flask_jwt_extended import create_access_token
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'code': 200,
        'data': {
            'access_token': access_token,
            'token_type': 'bearer',
            'expires_in': 7200,
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    jti = get_jwt()['jti']
    exp = get_jwt()['exp']
    AuthService.logout(jti, exp)
    return jsonify({'code': 200, 'message': '已登出'}), 200


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_me():
    user = User.query.get(int(g.user_id))
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404
    return jsonify({'code': 200, 'data': user.to_dict()}), 200


@auth_bp.route('/me', methods=['PUT'])
@login_required
def update_me():
    user = User.query.get(int(g.user_id))
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    data = request.get_json()
    if 'username' in data:
        username = data['username'].strip()
        if 2 <= len(username) <= 20:
            existing = User.query.filter(User.username == username, User.id != user.id).first()
            if existing:
                return jsonify({'code': 409, 'message': '用户名已被使用'}), 409
            user.username = username

    if 'avatar_url' in data:
        user.avatar_url = data['avatar_url']

    from app.extensions import db
    db.session.commit()
    return jsonify({'code': 200, 'data': user.to_dict()}), 200


@auth_bp.route('/me/password', methods=['PUT'])
@login_required
def change_password():
    user = User.query.get(int(g.user_id))
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    data = request.get_json()
    old_pwd = data.get('old_password', '')
    new_pwd = data.get('new_password', '')

    if not old_pwd or not new_pwd:
        return jsonify({'code': 400, 'message': '请填写旧密码和新密码'}), 400
    if len(new_pwd) < 6:
        return jsonify({'code': 400, 'message': '新密码至少 6 位'}), 400
    if not user.check_password(old_pwd):
        return jsonify({'code': 400, 'message': '旧密码不正确'}), 400

    user.set_password(new_pwd)
    from app.extensions import db
    db.session.commit()
    return jsonify({'code': 200, 'message': '密码修改成功'}), 200
