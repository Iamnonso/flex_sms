import os
from flask import Blueprint, redirect, url_for, request, render_template, jsonify

blueprint = Blueprint('errorhandlers',__name__)


@blueprint.app_errorhandler(404)
@blueprint.app_errorhandler(405)
def not_found(e):
    """ Return error 404 & 405 """
    if request.path.startswith('/api/'):
        return {
                'message': "Bad request!",
                'status': 400,
                'Error': str(e),
            }, 400
    else:
        return render_template('pages/error/index.html', name=os.environ['APP_NAME']), 404
    

