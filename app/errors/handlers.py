from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response
from flask import render_template, request
# from flask_babel import _
# from flask_babel import lazy_gettext as _l

def wants_json_response():
    # accept_mimetypes ==> request Header 'Accept'
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500