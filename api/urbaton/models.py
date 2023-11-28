import datetime
from typing import List

from sqlalchemy import ForeignKey, Text, Date, Boolean, Integer, Time, Float, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker
import mimesis

from settings import config


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(Text)
    user_type: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)
    surname: Mapped[str] = mapped_column(Text)
    middle_name: Mapped[str] = mapped_column(Text)
    gender: Mapped[bool] = mapped_column(Boolean)  # 0 - male, 1 - female?

    schedules: Mapped[List["ScheduleModel"]] = relationship('ScheduleModel', back_populates='created_user')


class StudentModel(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    date_of_birth: Mapped[datetime.date] = mapped_column(Date)
    phone_number: Mapped[str] = mapped_column(Text)

    user: Mapped[UserModel] = relationship('UserModel')

    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey('institutions.id'))
    institution: Mapped["InstitutionModel"] = relationship('InstitutionModel', back_populates='students')

    # klass_id: Mapped[int] = mapped_column(Integer, ForeignKey('classes.id'), nullable=True)
    # klass: Mapped["ClassModel"] = relationship('ClassModel', back_populates='students')

    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id'))
    group: Mapped["GroupModel"] = relationship('GroupModel', back_populates='students')

    appointments: Mapped[List["AppointmentModel"]] = relationship('AppointmentModel', back_populates='student')
    classes: Mapped[List["ClassModel"]] = relationship('ClassModel', back_populates='student')


class InstitutionModel(Base):
    __tablename__ = "institutions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    state: Mapped[str] = mapped_column(Text)

    students: Mapped[List["StudentModel"]] = relationship('StudentModel', back_populates='institution')
    schedules: Mapped[List["ScheduleModel"]] = relationship('ScheduleModel', back_populates='institution')

    teachers: Mapped[List["TeacherModel"]] = relationship('TeacherModel', back_populates='institution')


class ScheduleModel(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[str] = mapped_column(Text)
    create_date: Mapped[datetime.date] = mapped_column(Date)
    week_day: Mapped[int] = mapped_column(Integer)

    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey('institutions.id'))
    institution: Mapped["InstitutionModel"] = relationship('InstitutionModel', back_populates='schedules')

    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey('teachers.id'))
    teacher: Mapped["TeacherModel"] = relationship('TeacherModel', back_populates='schedules')

    created_user_id: Mapped[str] = mapped_column(Integer, ForeignKey('users.id'))
    created_user: Mapped["UserModel"] = relationship('UserModel', back_populates='schedules')

    schedule_slots: Mapped[List["ScheduleSlotModel"]] = relationship('ScheduleSlotModel', back_populates='schedule')


class ClassModel(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    # home_task: Mapped[str] = mapped_column(Text)
    is_individual: Mapped[bool] = mapped_column(Boolean)

    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey('teachers.id'))
    teacher: Mapped["TeacherModel"] = relationship('TeacherModel', back_populates='classes')

    slot_id: Mapped[int] = mapped_column(Integer, ForeignKey('schedule_slots.id'))
    slot: Mapped["ScheduleSlotModel"] = relationship('ScheduleSlotModel', back_populates='klass')

    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'), nullable=True)
    student: Mapped["StudentModel"] = relationship('StudentModel', back_populates='classes')

    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id'), nullable=True)
    group: Mapped["GroupModel"] = relationship('GroupModel', back_populates='classes')

    appointments: Mapped[List["AppointmentModel"]] = relationship('AppointmentModel', back_populates='klass')


class ScheduleSlotModel(Base):
    __tablename__ = "schedule_slots"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column(Text)
    room: Mapped[str] = mapped_column(Text)
    time_begin: Mapped[datetime.time] = mapped_column(Time)
    time_end: Mapped[datetime.time] = mapped_column(Time)

    schedule_id: Mapped[int] = mapped_column(Integer, ForeignKey('schedules.id'))
    schedule: Mapped["ScheduleModel"] = relationship('ScheduleModel', back_populates='schedule_slots')

    klass: Mapped["ClassModel"] = relationship('ClassModel', back_populates='slot')


class AppointmentModel(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    attendance: Mapped[bool] = mapped_column(Boolean)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    mark: Mapped[float] = mapped_column(Float)
    date: Mapped[datetime.date] = mapped_column(Date)

    student_id: Mapped[str] = mapped_column(Integer, ForeignKey('students.id'), primary_key=True)
    student: Mapped["StudentModel"] = relationship('StudentModel', back_populates='appointments')

    klass_id: Mapped[int] = mapped_column(Integer, ForeignKey('classes.id'))
    klass: Mapped["ClassModel"] = relationship('ClassModel', back_populates='appointments')

    __table_args__ = (
        UniqueConstraint('date', 'student_id', 'klass_id', name='unique_date_student_id_klass_id_constraint'),
    )


class TeacherModel(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    role: Mapped[str] = mapped_column(Text)
    experience: Mapped[str] = mapped_column(Text)
    speciality: Mapped[str] = mapped_column(Text)

    # user_id: Mapped[str] = mapped_column(Integer, )
    user: Mapped["UserModel"] = relationship('UserModel')

    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey('institutions.id'))
    institution: Mapped["InstitutionModel"] = relationship('InstitutionModel', back_populates='teachers')

    schedules: Mapped[List["ScheduleModel"]] = relationship('ScheduleModel', back_populates='teacher')
    classes: Mapped[List["ClassModel"]] = relationship('ClassModel', back_populates='teacher')


class GroupModel(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    speciality: Mapped[str] = mapped_column(Text)
    year_of_study: Mapped[int] = mapped_column(Integer)

    students: Mapped[List["StudentModel"]] = relationship('StudentModel', back_populates='group')
    classes: Mapped[List["ClassModel"]] = relationship('ClassModel', back_populates='group')


class ParentStudentModel(Base):
    __tablename__ = "parent_students"
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'), primary_key=True)
    student: Mapped["StudentModel"] = relationship('StudentModel', )
    parent_id: Mapped[str] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    parent: Mapped["UserModel"] = relationship('UserModel', )


db = config.db
engine = create_engine(
    f"postgresql+psycopg://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}",
    # connect_args={'options': f'-csearch_path={db.schema}'}
)

Session = sessionmaker(bind=engine)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with (Session() as session):
    generic = mimesis.Generic()

    parent_users = [UserModel(email=generic.person.email(),
                              user_type='PARENT',
                              password=generic.person.password(),
                              name=generic.person.first_name(),
                              surname=generic.person.last_name(),
                              middle_name=generic.person.first_name(),
                              gender=generic.random.choice([True, False]))
                    for _ in range(10)]
    student_users = [UserModel(email=generic.person.email(),
                               user_type='STUDENT',
                               password=generic.person.password(),
                               name=generic.person.first_name(),
                               surname=generic.person.last_name(),
                               middle_name=generic.person.first_name(),
                               gender=generic.random.choice([True, False]))
                     for _ in range(20)]
    teacher_users = [UserModel(email=generic.person.email(),
                               user_type='TEACHER',
                               password=generic.person.password(),
                               name=generic.person.first_name(),
                               surname=generic.person.last_name(),
                               middle_name=generic.person.first_name(),
                               gender=generic.random.choice([True, False]))
                     for _ in range(4)]

    admin_users = [UserModel(email=generic.person.email(),
                             user_type='ADMIN',
                             password=generic.person.password(),
                             name=generic.person.first_name(),
                             surname=generic.person.last_name(),
                             middle_name=generic.person.first_name(),
                             gender=generic.random.choice([True, False]))
                   for _ in range(2)]

    institutions = [InstitutionModel(name='art school',
                                     state=generic.random.choice(
                                         ['работает',
                                          # 'закрыто за педофилию', 'закрыто за эмоциональное насилие'
                                          ]))
                    for _ in range(1)]
    groups = [GroupModel(name=generic.person.email(),
                         speciality=generic.random.choice(['piano', 'guitar', 'nervous']),
                         year_of_study=generic.random.randint(1, 7), )
              for _ in range(7)]

    session.add_all([*parent_users, *student_users, *admin_users, *teacher_users])
    session.add_all([*institutions, *groups])
    session.commit()
    session.expire_all()
    session.add_all([*teacher_users, *institutions])
    teachers = [TeacherModel(
        role=generic.random.choice(['Professor', 'Assistant']),
        experience=generic.random.choice(['5 years', '10 years']),
        speciality=generic.random.choice(['piano', 'guitar', 'nervous']),
        user=teacher_user,
        institution=generic.random.choice(institutions),
    ) for teacher_user in teacher_users]
    session.add_all([*teachers])
    session.commit()
    print(f'{{"email":"{admin_users[0].email}","password":"{admin_users[0].password}"}}')
    session.expire_all()
    session.add_all([*student_users, *institutions, *groups])

    students = [StudentModel(
        id=student_user.id,
        date_of_birth=datetime.date.today(),
        phone_number=generic.person.telephone(),
        institution_id=generic.random.choice(institutions).id,
        group_id=generic.random.choice(groups).id,
    ) for student_user in student_users]
    session.add_all([*students])
    session.commit()
    session.add_all([*students, *parent_users])
    session.expire_all()

    parent_students = [ParentStudentModel(
        parent=generic.random.choice(parent_users),
        student_id=student.id,
    ) for student in students]

    session.add_all([*parent_students])
    session.commit()
    session.add_all([*student_users])
    session.expire_all()

    schedules = [ScheduleModel(
        state='',
        week_day=generic.random.choice([1, 2, 3, 4, 5, 6, 7]),
        institution_id=generic.random.choice(institutions).id,
        teacher_id=generic.random.choice(teachers).id,
        create_date=datetime.date.today(),
        created_user_id=generic.random.choice(admin_users).id,
    ) for student_user in student_users]

    session.add_all([*schedules])
    session.commit()
    session.expire_all()

    start_time = datetime.datetime.strptime('14:30:00', "%H:%M:%S")
    times = []
    for _ in range(8):
        begin_time = start_time.time()
        end_time = (start_time + datetime.timedelta(minutes=40)).time()
        start_time = (datetime.datetime.combine(datetime.datetime.today(), start_time.time()) + datetime.timedelta(
            minutes=20)
                      )
        times.append((begin_time, end_time))

    slots = [ScheduleSlotModel(
        subject_name=generic.random.choice(['piano', 'guitar', 'nervous']),
        room=generic.random.choice(['101', '120', '132', '132']),
        time_begin=time_begin,
        time_end=time_end,
        schedule_id=schedule.id,
    ) for schedule in schedules for time_begin, time_end in times]

    session.add_all([*slots])
    session.commit()
    session.expire_all()
    session.add_all([*slots, *teachers, *groups])

    klasses = []
    for slot in slots:
        is_individual = generic.random.choice([True, False])
        klasses.append(
            ClassModel(
                name='рисование кровью',
                # home_task='нарисовать',
                is_individual=is_individual,
                group_id=None if is_individual else generic.random.choice(groups).id,
                student_id=generic.random.choice(students).id if is_individual else None,
                teacher_id=generic.random.choice(teachers).id,
                slot_id=slot.id,
            )
        )

    # klass = ClassModel(
    #     name='рисование кровью',
    #     home_task='нарисовать',
    #     is_individual=False,
    #     group_id=group.id,
    #     teacher_id=teacher.id,
    #     slot_id=slot.id,
    # )
    session.add_all([*klasses])
    session.commit()
    session.expire_all()
