from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, log_reponse
from app.models import Post, User
from flask import abort, jsonify, request, url_for
import logging, json

@bp.route('/posts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_post(id):
    # return jsonify({'test':'test'})
    return jsonify(Post.query.get_or_404(id).to_dict())

@bp.route('/posts', methods=['GET'])
@token_auth.login_required
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 3, type=int), 100)
    data = Post.to_collection_dict(Post.query, page, per_page, 'api.get_posts')
    return jsonify(data)

@bp.route('/posts/user', methods=['GET'])
@token_auth.login_required
def get_user_post():
    user_id = token_auth.current_user().id
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 3, type=int), 100)
    data = Post.to_collection_dict(Post.query.filter_by(user_id=user_id), page, per_page, 'api.get_posts')
    return jsonify(data)

@bp.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    data = request.get_json() or None
    if (data == None):
        return bad_request('Error: Empty data')
    if 'body' not in data:
        logging.error('%s raised an error', data)
        return bad_request('Error: must include post body fields: {}'.format(data))

    post = Post()
    data['user_id'] = token_auth.current_user().id

    post.from_dict(data)
    db.session.add(post)
    db.session.commit()

    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response

@bp.route('/posts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_post(id):
    data = request.get_json() or None
    if (data == None):
        return bad_request('Error: Empty data')
    if 'body' not in data:
        logging.error('%s raised an error', data)
        return bad_request('Error: must include post body fields: {}'.format(data))

    post = Post.query.get_or_404(id)
    post.from_dict(data)
    db.session.add(post)
    db.session.commit()

    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response

@bp.route('/posts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    response = jsonify({"status":"success"})
    response.status_code = 200
    return response