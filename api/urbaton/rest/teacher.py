import attrs
import cattr
from flask import jsonify, request
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity

from urbaton.models import Session, UserModel, TeacherModel
import sqlalchemy as sa


@attrs.define
class RegisterTeacherRequest:
    institution_id: int
    email: str
    password: str
    name: str
    surname: str
    middleName: str
    experience: str
    speciality: str

    role: str


@jwt_required()
def register_teacher():
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

    register_teacher_data: RegisterTeacherRequest = cattr.structure(request_data, RegisterTeacherRequest)

    with Session() as session:
        teacher_user = UserModel(
            user_type='TEACHER',
            password=register_teacher_data.password,
            name=register_teacher_data.name,
            surname=register_teacher_data.surname,
            middle_name=register_teacher_data.middleName,
            gender=True,
        )
        session.add(teacher_user)
        session.refresh(teacher_user)
        teacher = TeacherModel(
            role=register_teacher_data.role,
            experience=register_teacher_data.experience,
            speciality=register_teacher_data.speciality,
            user=teacher_user,
            institution=register_teacher_data.institution_id,
        )
        session.add_all(teacher)

        session.commit()

    return jsonify({}), 201


def register_student():
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

    register_teacher_data: RegisterTeacherRequest = cattr.structure(request_data, RegisterTeacherRequest)

    with Session() as session:
        teacher_user = UserModel(
            user_type='TEACHER',
            password=register_teacher_data.password,
            name=register_teacher_data.name,
            surname=register_teacher_data.surname,
            middle_name=register_teacher_data.middleName,
            gender=True,
        )
        session.add(teacher_user)
        session.refresh(teacher_user)
        teacher = TeacherModel(
            role=register_teacher_data.role,
            experience=register_teacher_data.experience,
            speciality=register_teacher_data.speciality,
            user=teacher_user,
            institution=register_teacher_data.institution_id,
        )
        session.add_all(teacher)

        session.commit()

    return jsonify({}), 201
