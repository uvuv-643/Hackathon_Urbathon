import sqlalchemy as sa
from flask import request, jsonify
from flask_jwt_extended import create_access_token

from urbaton.models import UserModel, Session, TeacherModel, StudentModel


def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({"error": "Missing username or password"}), 400

    with Session() as session:
        get_user_query = sa.select(UserModel).where(UserModel.email == email)
        user = session.execute(get_user_query).scalar()

        if not user:
            return jsonify({"error": "Wrong email"}), 400

        match user.user_type:
            case 'TEACHER':
                get_institution_query = sa.select(TeacherModel).where(TeacherModel.id == user.id)
                institution = session.execute(get_user_query).scalar()
            case 'STUDENT':
                get_institution_query = sa.select(StudentModel).where(StudentModel.id == user.id)
                institution = session.execute(get_user_query).scalar()
            case _:
                institution = None
        institution = session.execute(get_user_query).scalar()
    if user.password != password:
        return jsonify({"error": "Bad username or password"}), 401

    # Создание JWT-токена
    access_token = create_access_token(identity=email, additional_claims={
        'ROLE': user.user_type,
        'INSTITUTION':  institution.id if institution else None})
    return jsonify(access_token=access_token), 200
