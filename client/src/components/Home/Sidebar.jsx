import React from 'react'
import {Link} from "react-router-dom";

function Sidebar(props) {

    return (
        <div className="Sidebar">
            <div className="Sidebar__Header">
                {/*<div className="News__Header__Logo">*/}
                {/*    <img src="assets/images/logo.svg" alt="Звёздник" />*/}
                {/*</div>*/}
                <div className="News__Header__Title">
                    <h3>Мой профиль</h3>
                    <p>{props.username}, {props.role}</p>
                    <Link to="/login">Сменить пользователя</Link>
                </div>
            </div>
            <div className="Sidebar__Content">
                <div className="Sidebar__Block Sidebar__Block--Teachers">
                    <div className="Sidebar__Block__Content">
                        <div className="Sidebar__Block__Links">
                            <h4>Преподаватели</h4>
                            <Link to="/teachers"><img src="assets/images/books.svg" alt="#"/> Таблица</Link>
                        </div>
                        <div className="Sidebar__Block__Count">
                            {props.teacherCount}
                        </div>
                    </div>
                </div>
                <div className="Sidebar__Block Sidebar__Block--Students">
                    <div className="Sidebar__Block__Content">
                        <div className="Sidebar__Block__Links">
                            <h4>Ученики</h4>
                            <Link to="#"><img src="assets/images/group.svg" alt="#"/> Группы</Link>
                        </div>
                        <div className="Sidebar__Block__Count">
                            {props.studentCount}
                        </div>
                    </div>
                </div>
            </div>

            <div className="Sidebar__Current">
                <h3>Сейчас проводятся занятия:</h3>
                <div className="Sidebar__Current__Scroll">
                    {props.current.map((el) => {
                        let startDate = new Date(el.timestart)
                        let endDate = new Date(el.timeend)
                        let hoursS = startDate.getHours()
                        if (hoursS.toString().length === 1) {
                            hoursS = '0' + hoursS
                        }
                        let minutesS = startDate.getHours()
                        if (minutesS.toString().length === 1) {
                            minutesS = '0' + minutesS
                        }
                        let hoursE = endDate.getHours()
                        if (hoursE.toString().length === 1) {
                            hoursE = '0' + hoursE
                        }
                        let minutesE = endDate.getHours()
                        if (minutesE.toString().length === 1) {
                            minutesE = '0' + minutesE
                        }
                        let startTime = hoursS + ':' + minutesS
                        let endTime = hoursE + ':' + minutesE
                        return (
                            <div className="Sidebar__Current__Item" key={el.id}>
                                <div className="Sidebar__Current__Item__Title">
                                    <h4>{el.subject}</h4>
                                    <p>
                                        <img src="assets/images/time.svg" alt="#"/>
                                        {startTime} - {endTime}
                                    </p>
                                    <p>Аудитория №{el.room}</p>
                                    <p>Преподаватель {el.teacher}</p>
                                    {el.isIndividual ? (
                                        <p>Ученик {el.student}</p>
                                    ) : (
                                        <p>Группа {el.group}</p>
                                    )}
                                </div>
                            </div>
                        )
                    })}
                </div>
                <div className="Sidebar__Button">
                    <Link to="/schedule">Изменить расписание</Link>
                </div>
            </div>

        </div>
    )

}

export default Sidebar