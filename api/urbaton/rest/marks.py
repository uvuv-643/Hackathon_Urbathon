import datetime

import cattr
from attr import define
from flask import jsonify, request
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt, get_jwt_identity
from sqlalchemy.orm import selectinload

from urbaton.models import Session, TeacherModel, ScheduleModel, ScheduleSlotModel, ClassModel, UserModel, \
    AppointmentModel
import sqlalchemy as sa
from cattrs import Converter

converter = Converter()
converter.register_unstructure_hook(datetime.date, lambda d: d.isoformat())
converter.register_structure_hook(datetime.date, lambda v, _: datetime.date.fromisoformat(v))
@define
class AppointmentData:
    student_id: int
    mark: float
    comment: str
    attendance: bool


@define
class AddMarksRequest:
    class_id: int
    date: datetime.date
    grades: list[AppointmentData]


# POST
@jwt_required()
def add_marks():
    verify_jwt_in_request()

    current_user = get_jwt_identity()


    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

        if user.user_type != 'TEACHER':
            return jsonify({"error": "No permissions"}), 403
    if not request.json:
        return jsonify({"error": "Empty body"}), 400
    request_data = request.get_json()

    request_data: AddMarksRequest = converter.structure(request_data, AddMarksRequest)

    with Session() as session:
        appointments = [AppointmentModel(
            attendance=appointment.attendance,
            mark=appointment.mark,
            comment=appointment.comment,
            student_id=appointment.student_id,
            klass_id=request_data.class_id,
            date=request_data.date,
        ) for appointment in request_data.grades]
        session.add_all(appointments)

        session.commit()

    return jsonify({}), 200
