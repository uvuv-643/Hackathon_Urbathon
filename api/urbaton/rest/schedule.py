import datetime

from attr import define
from flask import jsonify, request
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt, get_jwt_identity
from sqlalchemy.orm import selectinload, contains_eager

from urbaton.models import Session, TeacherModel, ScheduleModel, ScheduleSlotModel, ClassModel, UserModel
import sqlalchemy as sa

from cattrs import Converter

converter = Converter()
converter.register_unstructure_hook(datetime.date, lambda d: d.isoformat())
converter.register_unstructure_hook(datetime.time, lambda d: d.isoformat())
converter.register_structure_hook(datetime.date, lambda v, _: datetime.date.fromisoformat(v))
converter.register_structure_hook(datetime.time, lambda v, _: datetime.time.fromisoformat(v))


@define
class SlotItemData:
    time_start: str
    time_end: str
    subject: str
    room: str
    is_individual: bool
    group_id: int | None
    student_id: int | None
    class_id: int | None


@define
class ScheduleItemData:
    week_day: int
    slots: list[SlotItemData]
    id: int


@define
class TeacherItemData:
    teacher_id: int
    schedule: list[ScheduleItemData]


@define
class GetScheduleResponse:
    teachers: list[TeacherItemData]


@jwt_required()
def get_schedule():
    verify_jwt_in_request()

    current_user = get_jwt_identity()
    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403
    teacher_ids = request.args.getlist('teacher_id')
    student_ids = request.args.getlist('student_id')
    group_ids = request.args.getlist('group_id')
    subjects = request.args.getlist('subject')
    rooms = request.args.getlist('room')

    with Session() as session:
        query = (
            sa.select(TeacherModel)
            .where(TeacherModel.institution_id == 1)
            .where(True if not teacher_ids else TeacherModel.id.in_(list(map(int, teacher_ids))))
            .options(
                selectinload(TeacherModel.schedules)
                .selectinload(ScheduleModel.schedule_slots)
                .selectinload(ScheduleSlotModel.klass)

            )
        )
        query = session.execute(query).scalars().all()
    result = (GetScheduleResponse(
        teachers=[TeacherItemData(teacher_id=teacher.id,
                                  schedule=[ScheduleItemData(
                                      week_day=schedule.week_day,
                                      id=schedule.id,
                                      slots=[SlotItemData(
                                          time_start=slot.time_begin.isoformat(),
                                          time_end=slot.time_end.isoformat(),
                                          subject=slot.subject_name,
                                          room=slot.room,
                                          is_individual=slot.klass.is_individual,
                                          group_id=slot.klass.group_id,
                                          class_id=slot.klass.id,

                                          student_id=slot.klass.student_id
                                      ) for slot in schedule.schedule_slots
                                          if
                                          (True if not rooms else slot in (set(map(str, rooms)))) and (
                                              True if not subjects else slot.subject_name in (list(map(str, subjects))))
                                          and (True if not student_ids else slot.klass.student_id in (
                                              set(map(int, student_ids))))
                                      ]
                                  ) for schedule in teacher.schedules])
                  for teacher in query]))
    result = converter.unstructure(result)
    for teacher in result['teachers']:
        for index, sched in enumerate(teacher['schedule']):
            if not sched['slots']:
                print(index, sched)
                teacher['schedule'].pop(index)

    return jsonify(converter.unstructure(result)), 200
