import datetime
from typing import Optional

from attr import define, field, attrs
from cattrs import Converter
from flask import jsonify, request
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt, get_jwt_identity
from attrs import validators
from urbaton.models import Session, TeacherModel, ScheduleModel, ScheduleSlotModel, ClassModel, UserModel
import sqlalchemy as sa

from urbaton.models import Session

converter = Converter()
converter.register_unstructure_hook(datetime.date, lambda d: d.isoformat())
converter.register_structure_hook(datetime.date, lambda v, _: datetime.date.fromisoformat(v))


@define
class SlotItemData:
    time_start: str
    time_end: str
    subject: str
    room: str
    is_individual: bool
    group_id: int | None
    student_id: int | None


@define
class ScheduleItemData:
    id: Optional[int]
    week_day: int
    slots: list[SlotItemData]


@define
class TeacherItemData:
    teacher_id: int
    schedule: list[ScheduleItemData]


@define
class ChangeScheduleRequest:
    teachers: list[TeacherItemData]


@jwt_required()
def change_schedule():
    verify_jwt_in_request()

    current_user = get_jwt_identity()
    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

    if not request.json:
        return jsonify({"error": "Empty body"}), 400

    request_data = request.get_json()

    request_data: ChangeScheduleRequest = converter.structure(request_data, ChangeScheduleRequest)
    with Session() as session:
        # result = user.insert(session.execute(insert_stmt=sa.insert(user).values(username="example_username")))
        slots = []
        classes = []
        new_schedules = []

        for teacher in request_data.teachers:
            for schedule in teacher.schedule:
                if schedule.id is None:
                    schedule_instance = ScheduleModel(
                        state='',
                        week_day=schedule.week_day,
                        institution_id=1,
                        teacher_id=teacher.teacher_id,
                        create_date=datetime.datetime.now(),
                        created_user_id=user.id,
                    )
                    for slot_class in schedule.slots:
                        slot = ScheduleSlotModel(
                            subject_name=slot_class.subject,
                            room=slot_class.room,
                            time_begin=slot_class.time_start,
                            time_end=slot_class.time_end,
                            schedule_id=schedule.id,
                        )
                        klass = ClassModel(
                            name='рисование кровью',
                            is_individual=slot_class.is_individual,
                            group_id=slot_class.group_id,
                            student_id=slot_class.student_id,
                            teacher_id=teacher.teacher_id,
                            slot=slot,
                        )
                        slot.klass = klass
                        slots.append(slot)
                        classes.append(klass)
                    schedule_instance.schedule_slots = slots
                    new_schedules.append(schedule_instance)
        session.add_all([*slots, *classes, *new_schedules])

        slots = []
        classes = []
        new_schedules = []

        for teacher in request_data.teachers:
            for schedule in teacher.schedule:
                if schedule.id is None:
                    schedule_instance = ScheduleModel(
                        state='',
                        week_day=schedule.week_day,
                        institution_id=1,
                        teacher_id=teacher.teacher_id,
                        create_date=datetime.datetime.now(),
                        created_user_id=user.id,
                    )
                    for slot_class in schedule.slots:
                        slot = ScheduleSlotModel(
                            subject_name=slot_class.subject,
                            room=slot_class.room,
                            time_begin=slot_class.time_start,
                            time_end=slot_class.time_end,
                            schedule_id=schedule.id,
                        )
                        klass = ClassModel(
                            name='рисование кровью',
                            is_individual=slot_class.is_individual,
                            group_id=slot_class.group_id,
                            student_id=slot_class.student_id,
                            teacher_id=teacher.teacher_id,
                            slot=slot,
                        )
                        slot.klass = klass
                        slots.append(slot)
                        classes.append(klass)
                    schedule_instance.schedule_slots = slots
                    new_schedules.append(schedule_instance)
        session.add_all([*slots, *classes, *new_schedules])

        # on_conflict_do_update
        # session.on
        # result = session.execute(
        #     sa.insert(ScheduleSlotModel).values(
        #         [
        #             {
        #                 "subject_name": slot.subject_name,
        #                 "room": slot.room,
        #                 "time_begin": slot.time_begin,
        #                 "time_end": slot.time_end,
        #                 "schedule_id": slot.schedule_id,
        #                 # "schedule": slot.schedule,
        #                 # "klass": slot.klass,
        #             } for slot in slots
        #         ]),
        # )
        # print(result.first())
        session.commit()
        return jsonify({}), 200
