import React from 'react'
import {DAY_HEIGHT_PX, HEADER_HEIGHT, HOUR_WIDTH_PX, START_HOUR, TEACHER_WIDTH_PX} from "../Timetable";

function TimetableContent(props) {
    return (
        <div className="TimetableContent">

            {props.teachers.map((el, index) => (
                el.schedule.map((sched, index1) => (
                    sched.slots.map((slot, index2) => {
                        let startDate = new Date(slot.timestart)
                        let endDate = new Date(slot.timeend)
                        console.log(slot.timestart, slot.timeend, endDate.toString(), endDate.getHours())

                        let hoursS = startDate.getHours()
                        if (hoursS.toString().length === 1) {
                            hoursS = '0' + hoursS
                        }
                        let minutesS = startDate.getMinutes()
                        if (minutesS.toString().length === 1) {
                            minutesS = '0' + minutesS
                        }
                        let hoursE = endDate.getHours()
                        if (hoursE.toString().length === 1) {
                            hoursE = '0' + hoursE
                        }
                        let minutesE = endDate.getMinutes()
                        if (minutesE.toString().length === 1) {
                            minutesE = '0' + minutesE
                        }
                        let startTime = hoursS + ':' + minutesS
                        let endTime = hoursE + ':' + minutesE
                        return (
                            <div className="TimetableContent__Item" key={el.id}
                                 style={{
                                     top: HEADER_HEIGHT + DAY_HEIGHT_PX * index,
                                     left: TEACHER_WIDTH_PX + HOUR_WIDTH_PX * (((startDate.getHours() - START_HOUR) * 60 + startDate.getMinutes())) / 60,
                                     height: DAY_HEIGHT_PX,
                                     width: HOUR_WIDTH_PX * (endDate.getHours() * 60 + endDate.getMinutes() - (startDate.getHours() * 60 + startDate.getMinutes())) / 60
                                 }}>
                                <h4>{slot.subject}</h4>
                                <p className="_time">
                                    <img src="assets/images/time.svg" alt="#"/>
                                    {startTime} - {endTime}
                                </p>
                                <p>{slot.room}</p>
                                {slot.isIndividual ? (
                                    <p>{slot.student}</p>
                                ) : (
                                    <p>{slot.group}</p>
                                )}
                            </div>
                        )
                    })
                ))
            ))}
        </div>
    )
}

export default TimetableContent