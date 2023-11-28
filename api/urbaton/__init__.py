from cattrs import ClassValidationError
from flask import Flask
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import IntegrityError

from settings import config
from urbaton.rest.groups import delete_group, create_group, update_group, get_all_groups, get_group
from urbaton.rest.marks import add_marks
from urbaton.rest.put_schedule import change_schedule
from urbaton.rest.rooms import get_rooms
from urbaton.rest.schedule import get_schedule
from urbaton.rest.error_handlers import forbidden, not_found, internal_server_error, validation_handler, \
    integrity_handler
from urbaton.rest.login import login
from urbaton.rest.slots import change_slot, delete_slot, add_slot
from urbaton.rest.student_schedule import get_student_schedule
from urbaton.rest.teacher import register_teacher
from urbaton.rest.users import create_teacher, create_student, get_all_teachers


def flask_config(app: Flask) -> Flask:
    # jwt config
    app.config['JWT_SECRET_KEY'] = config.jwt.secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.jwt.access_token_expires
    app.config['JWT_ERROR_MESSAGE_KEY'] = config.jwt.error_message_key
    jwt = JWTManager(app)

    return app


def rest_init(app: Flask) -> Flask:
    app.add_url_rule('/login', '/login', login, methods=['POST'])
    app.add_url_rule('/schedule', '/schedule', get_schedule, methods=['GET'])
    app.add_url_rule('/schedule', '/schedule_put', change_schedule, methods=['PUT'])
    app.add_url_rule('/marks', '/marks', add_marks, methods=['POST'])
    app.add_url_rule('/teacher', '/teacher', register_teacher, methods=['POST'])
    app.add_url_rule('/class', '/class_update', change_slot, methods=['PUT'])
    app.add_url_rule('/class/<int:id>', '/class_delete', delete_slot, methods=['DELETE'])
    app.add_url_rule('/class', '/class_create', add_slot, methods=['POST'])
    app.add_url_rule('/groups/<int:group_id>', '/delete_group', delete_group, methods=['DELETE'])
    app.add_url_rule('/groups', '/create_group', create_group, methods=['POST'])
    app.add_url_rule('/groups/<int:group_id>', '/update_group', update_group, methods=['PUT'])
    app.add_url_rule('/groups', '/get_all_groups', get_all_groups, methods=['GET'])
    app.add_url_rule('/groups/<int:group_id>', '/get_group', get_group, methods=['GET'])
    app.add_url_rule('/teachers', '/create_teacher', create_teacher, methods=['POST'])
    app.add_url_rule('/students', '/create_student', create_student, methods=['POST'])
    app.add_url_rule('/teachers', '/get_all_teachers', get_all_teachers, methods=['GET'])
    app.add_url_rule('/rooms', '/get_rooms', get_rooms, methods=['GET'])
    app.add_url_rule('/schedule/student/<int:student_id>', '/get_student_schedule', get_student_schedule, methods=['GET'])

    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(ClassValidationError, validation_handler)
    app.register_error_handler(IntegrityError, integrity_handler)
    app.register_error_handler(Exception, internal_server_error)

    return app
