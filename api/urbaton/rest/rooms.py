import datetime

import sqlalchemy as sa
from attr import define
from cattrs import Converter
from flask import request, jsonify
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity
from sqlalchemy.orm import selectinload

from urbaton.models import UserModel, Session, TeacherModel, StudentModel, GroupModel, ScheduleSlotModel


def get_rooms():
    verify_jwt_in_request()

    current_user = get_jwt_identity()
    with Session() as session:
        query = sa.select(UserModel).where(UserModel.email == current_user)
        user = session.execute(query).scalar()
        if not user:
            return jsonify({"error": "Bad token"}), 403

    with Session() as session:
        query = sa.select(ScheduleSlotModel.room.distinct())
        rooms = session.execute(query).scalars().all()

    return jsonify(rooms), 200
