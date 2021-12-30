from flask import request, jsonify
from six import wraps

from model.EWallet import EWallet


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            ewallet = EWallet.query.filter_by(token = token).first()

        except:
            return jsonify({'message': 'token is invalid'})

        if ewallet:
            return f(ewallet, *args, **kwargs)
        else:
            return jsonify({'message': 'token is invalid'})

    return decorator