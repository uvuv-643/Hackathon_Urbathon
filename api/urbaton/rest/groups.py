import datetime

import sqlalchemy as sa
from attr import define
from cattrs import Converter
from flask import request, jsonify
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity
from sqlalchemy.orm import selectinload

from urbaton.models import UserModel, Session, TeacherModel, StudentModel, GroupModel

converter = Converter()
converter.register_unstructure_hook(datetime.date, lambda d: d.isoformat())
converter.register_unstructure_hook(datetime.time, lambda d: d.isoformat())
converter.register_structure_hook(datetime.date, lambda v, _: datetime.date.fromisoformat(v))
converter.register_structure_hook(datetime.time, lambda v, _: datetime.time.fromisoformat(v))


@define
class GroupData:
    name: str
    speciality: str
    year_of_study: str


def create_group():
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
    request_data: GroupData = converter.structure(request_data, GroupData)
    with Session() as session:
        group = GroupModel(
            name=request_data.name,
            speciality=request_data.speciality,
            year_of_study=request_data.year_of_study
        )
        session.add(group)
        session.commit()
        session.refresh(group)

    return jsonify({"id": group.id}), 201


def update_group(group_id):
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
    request_data: GroupData = converter.structure(request_data, GroupData)

    with Session() as session:
        group = session.query(GroupModel).get(group_id)
        if not group:
            return jsonify({"error": "Group not found"}), 404

        group.name = request_data.name
        group.speciality = request_data.speciality
        group.year_of_study = request_data.year_of_study

        session.commit()

    return jsonify({}), 200


# Удаление группы
def delete_group(group_id):
    verify_jwt_in_request()

    current_user = get_jwt_identity()

    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

        if user.user_type != 'ADMIN':
            return jsonify({"error": "No permissions"}), 403

    # if not request.json:
    #     return jsonify({"error": "Empty body"}), 400
    #
    # request_data = request.get_json()

    with Session() as session:
        group = session.query(GroupModel).get(group_id)
        if not group:
            return jsonify({"error": "Group not found"}), 404

        session.delete(group)
        session.commit()

    return jsonify({}), 204


# Получение списка всех групп
def get_all_groups():
    verify_jwt_in_request()

    current_user = get_jwt_identity()

    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

        # if user.user_type != 'ADMIN':
        #     return jsonify({"error": "No permissions"}), 403

    with Session() as session:
        groups = session.query(GroupModel).all()
        group_list = [
            {
                "id": group.id,
                "name": group.name,
                "speciality": group.speciality,
                "year_of_study": group.year_of_study
            }
            for group in groups
        ]

    return jsonify({"groups": group_list}), 200


def get_group(group_id):
    verify_jwt_in_request()

    current_user = get_jwt_identity()

    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

        # if user.user_type != 'ADMIN':
        #     return jsonify({"error": "No permissions"}), 403

    with (Session() as session):
        group = session.query(GroupModel).where(GroupModel.id == group_id).options(
            selectinload(GroupModel.students)
            .selectinload(StudentModel.user)
        ).first()
        result = {
            "id": group.id,
            "name": group.name,
            "speciality": group.speciality,
            "year_of_study": group.year_of_study,
            'students': [{
                "name": student.user.name,
                "surname": student.user.surname,
                "middle_name": student.user.middle_name,
                "user_id": student.user.id,
            } for student in group.students]
        }

    return jsonify(result), 200
