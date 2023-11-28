import React from 'react'
import {DAY_HEIGHT_PX, END_HOUR, HEADER_HEIGHT, HOUR_WIDTH_PX, START_HOUR, TEACHER_WIDTH_PX} from "../Timetable";


function TimetableTeachers(props) {

    return (
        <div className="TimetableTeachers" style={{
            top: -props.scrollFromTop
        }}>
            <div style={{
                top: 0,
                left: 0,
                height: HEADER_HEIGHT,
                width: TEACHER_WIDTH_PX
            }}></div>
            {
                props.teachers.map((el, index) => (
                    <div key={index} style={{
                        top: HEADER_HEIGHT + DAY_HEIGHT_PX * index,
                        left: 0,
                        height: DAY_HEIGHT_PX,
                        width: TEACHER_WIDTH_PX
                    }}>{ el.teacher }</div>
                ))
            }
        </div>
    )

}

export default TimetableTeachers