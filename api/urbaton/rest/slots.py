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
converter.register_unstructure_hook(datetime.time, lambda d: d.isoformat())
converter.register_structure_hook(datetime.date, lambda v, _: datetime.date.fromisoformat(v))
converter.register_structure_hook(datetime.time, lambda v, _: datetime.time.fromisoformat(v))


@define
class SlotClassRequest:
    time_start: datetime.time
    time_end: datetime.time
    subject: str
    room: str
    is_individual: bool
    group_id: int | None
    student_id: int | None
    class_id: int


@define
class CreateSlotClassRequest:
    time_start: datetime.time
    time_end: datetime.time
    subject: str
    room: str
    is_individual: bool
    group_id: int | None
    student_id: int | None
    class_id: int
    schedule_id: int


# POST
@jwt_required()
def add_slot():
    verify_jwt_in_request()

    current_user = get_jwt_identity()

    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

        # if user.user_type != 'ADMIN':
        #     return jsonify({"error": "No permissions"}), 403
    if not request.json:
        return jsonify({"error": "Empty body"}), 400

    request_data = request.get_json()

    request_data: CreateSlotClassRequest = converter.structure(request_data, CreateSlotClassRequest)

    with Session() as session:
        schedule_query = (sa.select(ScheduleModel)
                          .where(ScheduleModel.id == request_data.schedule_id)
                          )

        schedule = session.execute(schedule_query).scalar()
        slot = ScheduleSlotModel(
            time_begin=request_data.time_start,
            time_end=request_data.time_end,
            subject_name=request_data.subject,
            room=request_data.room,
            schedule_id=schedule,
        )
        session.add(slot)
        session.commit()
        session.refresh(slot)

        klass = ClassModel(
            is_individual=request_data.is_individual,
            group_id=request_data.group_id,
            student_id=request_data.student_id,
            teacher_id=schedule.teacher_id,
            slot_id=slot.id,
            name=request_data.subject
        )

        session.add(klass)
        session.commit()

    return jsonify({}), 200


@jwt_required()
def change_slot():
    verify_jwt_in_request()

    current_user = get_jwt_identity()

    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

        # if user.user_type != 'ADMIN':
        #     return jsonify({"error": "No permissions"}), 403
    if not request.json:
        return jsonify({"error": "Empty body"}), 400

    request_data = request.get_json()

    request_data: SlotClassRequest = converter.structure(request_data, SlotClassRequest)

    with Session() as session:
        slot_class_query = (sa.select(ClassModel)
                            .where(ClassModel.id == request_data.class_id)
                            .options(selectinload(ClassModel.slot))
                            )
        slot_class = session.execute(slot_class_query).scalar()
        slot_class.slot.time_begin = request_data.time_start  # ScheduleSlotModel.time_begin
        slot_class.slot.time_end = request_data.time_end
        slot_class.slot.subject_name = request_data.subject
        slot_class.slot.room = request_data.room
        slot_class.is_individual = request_data.is_individual
        slot_class.group_id = request_data.group_id
        slot_class.student_id = request_data.student_id

        session.add(slot_class)
        session.commit()

    return jsonify({}), 200


@define
class DeleteClassRequest:
    id: int


@jwt_required()
def delete_slot(id: int):
    verify_jwt_in_request()

    current_user = get_jwt_identity()

    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

    try:
        id = int(id)
    except Exception as exc:
        return jsonify({"error": "Bad id"}), 400
        # if user.user_type != 'ADMIN':
        #     return jsonify({"error": "No permissions"}), 403
    # if not request.json:
    #     return jsonify({"error": "Empty body"}), 400

    with Session() as session:
        slot_class_query = (sa.select(ClassModel)
                            .where(ClassModel.id == id)
                            .options(selectinload(ClassModel.slot))
                            )
        slot_class = session.execute(slot_class_query).scalar()
        if not slot_class:
            return jsonify({"error": "Bad id"}), 404
        result = session.execute(sa.delete(ClassModel).where(ClassModel.id == slot_class.id))
        session.execute(sa.delete(ScheduleSlotModel).where(ScheduleSlotModel.id == slot_class.slot.id))
        session.commit()
        if result:
            return jsonify({}), 200
    return jsonify({"error": "Bad id"}), 400
