import datetime

import sqlalchemy as sa
from attr import define
from cattrs import Converter
from flask import request, jsonify
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity, jwt_required
from sqlalchemy.orm import selectinload

from urbaton.models import UserModel, Session, TeacherModel, StudentModel, GroupModel
from urbaton.rest.groups import converter

converter = Converter()
converter.register_unstructure_hook(datetime.date, lambda d: d.isoformat())
converter.register_unstructure_hook(datetime.time, lambda d: d.isoformat())
converter.register_structure_hook(datetime.date, lambda v, _: datetime.date.fromisoformat(v))
converter.register_structure_hook(datetime.time, lambda v, _: datetime.time.fromisoformat(v))


@define
class CreateTeacherData:
    email: str
    password: str
    name: str
    surname: str
    middle_name: str
    gender: bool

    role: str
    experience: str
    speciality: str
    # institution = 1,


def create_teacher():
    verify_jwt_in_request()

    current_user = get_jwt_identity()

    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

        if user.user_type != 'ADMIN':
            return jsonify({"error": "No permissions"}), 403

    if not request.json:
        return jsonify({"error": "Empty body"}), 400

    request_data = request.get_json()
    request_data: CreateTeacherData = converter.structure(request_data, CreateTeacherData)

    with Session() as session:
        user = UserModel(
            email=request_data.email,
            user_type="TEACHER",
            password=request_data.password,
            name=request_data.name,
            surname=request_data.surname,
            middle_name=request_data.middle_name,
            gender=request_data.gender
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        teacher = TeacherModel(
            role=request_data.role,
            experience=request_data.experience,
            speciality=request_data.speciality,
            user=user,
            institution=1,
        )
        session.add(teacher)

        session.commit()

    return jsonify({"id": user.id}), 201


@define
class CreateStudentData:
    email: str
    password: str
    name: str
    surname: str
    middle_name: str
    gender: bool

    date_of_birth: datetime.date
    phone_number: str

    institution_id: int

    group_id: int


def create_student():
    verify_jwt_in_request()

    current_user = get_jwt_identity()

    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

        if user.user_type != 'ADMIN':
            return jsonify({"error": "No permissions"}), 403

    if not request.json:
        return jsonify({"error": "Empty body"}), 400

    request_data = request.get_json()
    request_data: CreateStudentData = converter.structure(request_data, CreateStudentData)

    with Session() as session:
        query = sa.select(GroupModel).where(GroupModel.id == request_data.group_id)
        group = session.execute(query).scalar()
        if not group:
            return jsonify({"error": "Wrong group id"}), 400

        user = UserModel(
            email=request_data.email,
            user_type="STUDENT",
            password=request_data.password,
            name=request_data.name,
            surname=request_data.surname,
            middle_name=request_data.middle_name,
            gender=request_data.gender
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        session.refresh(group)

        student = StudentModel(
            user=user,
            date_of_birth=request_data.date_of_birth,
            phone_number=request_data.phone_number,
            institution_id=request_data.institution_id,
            group=group,
        )
        session.add(student)

        session.commit()

        return jsonify({"id": user.id}), 201


# # @app.route('/users/<int:user_id>', methods=['PUT'])
# @jwt_required()
# def update_user(user_id):
#     verify_jwt_in_request()
#
#     current_user = get_jwt_identity()
#
#     with Session() as session:
#         query = sa.select(UserModel).where(UserModel.email == current_user)
#         user = session.execute(query).scalar()
#         if not user:
#             return jsonify({"error": "Bad token"}), 403
#
#         if user.user_type != 'ADMIN':
#             return jsonify({"error": "No permissions"}), 403
#
#     if not request.json:
#         return jsonify({"error": "Empty body"}), 400
#
#     request_data = request.get_json()
#
#     with Session() as session:
#         query = session.query(UserModel).filter(UserModel.id == user_id)
#         user = query.scalar()
#         if not user:
#             return jsonify({"error": "Bad token"}), 404
#
#         user.name = request_data.get('name', user.name)
#         user.surname = request_data.get('surname', user.surname)
#         user.middle_name = request_data.get('middle_name', user.middle_name)
#         user.gender = request_data.get('gender', user.gender)
#
#         session.commit()
#
#     return jsonify({}), 200
#

# Удаление пользователя
# @jwt_required()
# def delete_user(user_id):
#     verify_jwt_in_request()
#
#     current_user = get_jwt_identity()
#
#     with Session() as session:
#         query = sa.select(UserModel).where(UserModel.email == current_user)
#         user = session.execute(query).scalar()
#         if not user:
#             return jsonify({"error": "Bad token"}), 403
#
#         if user.user_type != 'ADMIN':
#             return jsonify({"error": "No permissions"}), 403
#
#         if not request.json:
#             return jsonify({"error": "Empty body"}), 400
#
#     with Session() as session:
#         user_to_delete = session.query(UserModel).get(user_id)
#         if not user_to_delete:
#             return jsonify({"error": "User not found"}), 404
#
#         session.delete(user_to_delete)
#         session.commit()
#
#     return jsonify({}), 204
#
#
# # Получение пользователя
# @jwt_required()
# def get_user(user_id):
#     current_user = get_jwt_identity()
#
#     with Session() as session:
#         query = session.query(UserModel).filter(UserModel.email == current_user)
#         user = query.scalar()
#         if not user:
#             return jsonify({"error": "Bad token"}), 403
#
#         if user.id != user_id:
#             return jsonify({"error": "Unauthorized"}), 403
#
#         user_to_get = session.query(UserModel).get(user_id)
#         if not user_to_get:
#             return jsonify({"error": "User not found"}), 404
#
#         user_data = {
#             "id": user_to_get.id,
#             "email": user_to_get.email,
#             "user_type": user_to_get.user_type,
#             "name": user_to_get.name,
#             "surname": user_to_get.surname,
#             "middle_name": user_to_get.middle_name,
#             "gender": user_to_get.gender
#         }
#
#     return jsonify({"user": user_data}), 200


@jwt_required()
def get_all_teachers():
    current_user = get_jwt_identity()

    with Session() as session:
        query = session.query(TeacherModel, UserModel).join(UserModel, TeacherModel.id == UserModel.id).all()

        teachers_list = [
            {
                "teacher_id": teacher.id,
                "email": teacher.user.email,
                "user_type": teacher.user.user_type,
                # "password": teacher.user.password,
                "name": teacher.user.name,
                "surname": teacher.user.surname,
                "middle_name": teacher.user.middle_name,
                "gender": teacher.user.gender,
                # Другие поля из модели TeacherModel
                "role": teacher.role,
                "experience": teacher.experience,
                "speciality": teacher.speciality,
                "institution": 1,

            }
            for teacher, user in query
        ]

    return jsonify({"teachers": teachers_list}), 200
