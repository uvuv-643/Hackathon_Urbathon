import datetime
from collections import defaultdict
from functools import reduce

from attr import define
from flask import jsonify, request
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt, get_jwt_identity
from sqlalchemy.orm import selectinload, contains_eager

from urbaton.models import Session, TeacherModel, ScheduleModel, ScheduleSlotModel, ClassModel, UserModel
import sqlalchemy as sa

import itertools

from cattrs import Converter

converter = Converter()
converter.register_unstructure_hook(datetime.date, lambda d: d.isoformat())
converter.register_unstructure_hook(datetime.time, lambda d: d.isoformat())
converter.register_structure_hook(datetime.date, lambda v, _: datetime.date.fromisoformat(v))
converter.register_structure_hook(datetime.time, lambda v, _: datetime.time.fromisoformat(v))


@define
class ClassesItemData:
    time_start: datetime.time
    time_end: datetime.time
    subject: str
    room: str
    is_individual: bool
    teacher_name: str
    teacher_surname: str
    teacher_middle_name: str


@define
class ScheduleItemData:
    week_day: int
    classes: list[ClassesItemData]


@define
class GetStudentScheduleResponse:
    schedule: list[ScheduleItemData]


@jwt_required()
def get_student_schedule(student_id):
    verify_jwt_in_request()

    current_user = get_jwt_identity()
    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

    with Session() as session:
        query = (
            sa.select(ClassModel)
            .where(ClassModel.student_id == student_id)
            .options(
                selectinload(ClassModel.teacher)
                .selectinload(TeacherModel.user),
                selectinload(ClassModel.slot)
                .selectinload(ScheduleSlotModel.schedule),
                # selectinload(ClassModel.appointments)

            )
        )
        classes = session.execute(query).scalars().all()

        result = [ScheduleItemData(
            week_day=klass.slot.schedule.week_day,
            classes=[ClassesItemData(
                time_start=klass.slot.time_begin,
                time_end=klass.slot.time_end,
                subject=klass.slot.subject_name,
                room=klass.slot.room,
                is_individual=klass.is_individual,
                teacher_name=klass.teacher.user.name,
                teacher_surname=klass.teacher.user.surname,
                teacher_middle_name=klass.teacher.user.middle_name,
            )])
            for klass in classes]
        grouped = itertools.groupby(result, lambda schedule_item: schedule_item.week_day)
        result = defaultdict()
        for k, v in grouped:
            result[k] = ScheduleItemData(week_day=k, classes=[item.classes[0] for item in v])

    return jsonify(schedule=converter.unstructure(list(result.values()))), 200
