import React, {useEffect, useState} from 'react'
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import ru from 'date-fns/locale/ru';
import Select from 'react-select';

function ScheduleForm(props) {

    const [startedTime, setStartedTime] = useState(new Date('2000-01-01 10:00:00'));
    const [finishedTime, setFinishedTime] = useState(new Date('2000-01-01 14:00:00'));
    const [selectedRoom, setSelectedRoom] = useState(props.rooms[0])
    const [selectedTeacher, setSelectedTeacher] = useState(props.teachers[0])
    const [selectedStudent, setSelectedStudent] = useState(props.students[0])

    useEffect(() => {
        console.log(selectedRoom)
    }, [selectedRoom])

    return (
        <div className="ScheduleForm">
            <div className="ScheduleForm__Item">
                <p>Время начало занятия</p>
                <DatePicker
                    selected={startedTime}
                    onChange={(time) => setStartedTime(time)}
                    showTimeSelect
                    showTimeSelectOnly
                    timeIntervals={15}
                    locale={ru}
                    dateFormat="HH:mm"
                    timeCaption="Начало"
                    minTime={new Date(0, 0, 0, 6, 0)}
                    maxTime={new Date(0, 0, 0, 22, 0)}
                />
            </div>
            <div className="ScheduleForm__Item">
                <p>Время окончания занятия</p>
                <DatePicker
                    selected={finishedTime}
                    onChange={(time) => setFinishedTime(time)}
                    showTimeSelect
                    showTimeSelectOnly
                    timeIntervals={15}
                    locale={ru}
                    dateFormat="HH:mm"
                    timeCaption="Конец"
                    minTime={startedTime}
                    maxTime={new Date(0, 0, 0, 22, 0)}
                />
            </div>

            <div className="ScheduleForm__Item">
                <p>Аудитория</p>
                <Select
                    className="basic-single"
                    classNamePrefix="select"
                    isSearchable={true}
                    name="room"
                    onChange={(e)=> setSelectedRoom(e.value)}
                    options={
                    props.rooms.map((el) => {
                        return { value: el.id, label: el.room }
                    })}
                />
            </div>

            <div className="ScheduleForm__Item">
                <p>Преподаватель</p>
                <Select
                    className="basic-single"
                    classNamePrefix="select"
                    isSearchable={true}
                    name="teacher"
                    onChange={(e)=> setSelectedTeacher(e.value)}
                    options={
                        props.teachers.map((el) => {
                            return { value: el.id, label: el.name }
                        })
                    }
                />
            </div>

            <div className="ScheduleForm__Item">
                <p>Учащийся</p>
                <Select
                    className="basic-single"
                    classNamePrefix="select"
                    isSearchable={true}
                    name="student"
                    onChange={(e)=> setSelectedStudent(e.value)}
                    options={
                        props.students.map((el) => {
                            return { value: el.id, label: el.name }
                        })
                    }
                />
            </div>

            <div className="ScheduleForm__Item">
                <button>Сохранить</button>
            </div>

        </div>
    )
}

export default ScheduleForm