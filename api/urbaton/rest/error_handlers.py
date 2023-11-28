import logging

from flask import jsonify


def not_found(error):
    logging.debug(f'%s', error)
    response = {
        'error': 'Not Found',
        'message': 'The requested URL was not found',
    }
    return jsonify(response), 404


def internal_server_error(error):
    logging.error(f'%s', error)
    response = {
        'error': 'Internal Server Error',
        'message': 'The server encountered an internal error and was unable to complete your request.',
    }
    return jsonify(response), 500


def forbidden(error):
    logging.debug(f'%s', error)
    response = {
        'error': 'Forbidden',
        'message': 'You don\'t have permission to access this resource.',
    }
    return jsonify(response), 403


def validation_handler(error):
    return jsonify({"error": "wrong data format"}), 400


def integrity_handler(error):
    return jsonify({"error": "integrity error"}), 400
