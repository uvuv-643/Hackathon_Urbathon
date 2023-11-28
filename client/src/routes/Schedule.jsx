import React, {useState} from 'react'
import Timetable from "../components/Schedule/Timetable";
import ScheduleForm from "../components/Schedule/ScheduleForm";
import SmallCalendar from "../components/SmallCalendar";
import {Link} from "react-router-dom";

function Schedule(props) {

    const [selectedDay, setSelectedDay] = useState(0)
    const [currentSchedule, setCurrentSchedule] = useState([])

    const teachers = [
        {"id": 1, "name": "Иванов Александр Николаевич"},
        {"id": 2, "name": "Смирнова Екатерина Игоревна"},
        {"id": 3, "name": "Кузнецов Павел Сергеевич"},
        {"id": 4, "name": "Попова Анастасия Валерьевна"},
        {"id": 5, "name": "Морозов Игорь Александрович"},
        {"id": 6, "name": "Новикова Татьяна Дмитриевна"},
        {"id": 7, "name": "Петров Владимир Андреевич"},
        {"id": 8, "name": "Соколова Мария Викторовна"},
        {"id": 9, "name": "Волков Артемий Станиславович"},
        {"id": 10, "name": "Федорова Анна Валентиновна"},
        {"id": 11, "name": "Медведев Сергей Алексеевич"},
        {"id": 12, "name": "Козлова Елена Степановна"},
        {"id": 13, "name": "Жуков Владислав Игоревич"},
        {"id": 14, "name": "Максимова Наталья Олеговна"},
        {"id": 15, "name": "Алексеев Даниил Валентинович"},
        {"id": 16, "name": "Савельева Виктория Петровна"},
        {"id": 17, "name": "Кудрявцев Павел Леонидович"},
        {"id": 18, "name": "Григорьева Алина Артемовна"},
        {"id": 19, "name": "Борисов Илья Васильевич"},
        {"id": 20, "name": "Тимофеева Елизавета Денисовна"}
    ]

    return (
        <div className="Schedule">
            <Link to='/' className="Schedule__Back"><img src="assets/images/back.svg" alt="back"/>На главную</Link>
            <SmallCalendar currentDate={new Date()} selected={selectedDay} setSelected={(el) => setSelectedDay(el)}/>
            <div className="Schedule__Wrapper">
                <div className="Schedule__Table">
                    <Timetable teachers={teachers}/>
                </div>
                <div className="Schedule__Form">
                    <h3>Выберите преподавателя / учащегося для добавления занятий или нажмите на существующее для
                        редактирования</h3>
                    <ScheduleForm
                        rooms={[
                            {id: 1, room: 'ауд 513'},
                            {id: 2, room: 'ауд 514'},
                            {id: 3, room: 'ауд 515'},
                            {id: 4, room: 'ауд 516'},
                            {id: 5, room: 'ауд 517'},
                            {id: 6, room: 'ауд 518'},
                            {id: 7, room: 'ауд 519'},
                            {id: 8, room: 'ауд 520'},
                            {id: 9, room: 'ауд 521'},
                        ]}
                        students={[
                            {id: 1, name: 'гр. А25'},
                            {id: 2, name: 'гр. P551'},
                            {id: 3, name: 'гр. 71'},
                            {id: 81, name: 'гр. 661'},
                            {id: 4, name: 'Иванов Александр Николаевич'},
                            {id: 5, name: 'Дмитриев Алексей Владимирович'},
                            {id: 6, name: 'Николаев Владимир Вячеславович'},
                            {id: 7, name: 'Коржов Антон Валерьевич'},
                            {id: 8, name: 'Иванова Полина Алексеевна'},
                            {id: 9, name: 'Зинатулин Артём Витальевич'},
                        ]}
                        teachers={teachers}
                    />
                </div>
            </div>
        </div>
    )

}

export default Schedule