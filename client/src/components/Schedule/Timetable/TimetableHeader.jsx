import React from 'react'
import {END_HOUR, HEADER_HEIGHT, HOUR_WIDTH_PX, START_HOUR, TEACHER_WIDTH_PX} from "../Timetable";


function TimetableHeader(props) {

    return (
        <div className="TimetableHeader" style={{
            left: -props.scrollFromLeft
        }}>
            {
                [...Array(END_HOUR - START_HOUR + 1)].map((el, index) => (
                    <div key={index} style={{
                        top: 0,
                        left: TEACHER_WIDTH_PX + HOUR_WIDTH_PX * index,
                        height: HEADER_HEIGHT,
                        width: HOUR_WIDTH_PX
                    }}>{ (index + START_HOUR)?.toString()?.length > 1 ? ((index + START_HOUR) + ':00') : ('0' + (index + START_HOUR) + ':00') }</div>
                ))
            }
        </div>
    )

}

export default TimetableHeader