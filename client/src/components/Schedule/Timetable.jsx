import React, {useEffect, useState} from 'react'
import TimetableHeader from "./Timetable/TimetableHeader";
import TimetableTeachers from "./Timetable/TimetableTeachers";
import TimetableContent from "./Timetable/TimetableContent";
import axios from "axios";


export const START_HOUR = 6
export const END_HOUR = 22
export const TEACHER_WIDTH_PX = 200
export const DAY_HEIGHT_PX = 120
export const HOUR_WIDTH_PX = 200
export const HEADER_HEIGHT = 50

function Timetable(props) {

    const [scrollFromTop, setScrollFromTop] = useState(0)
    const [scrollFromLeft, setScrollFromLeft] = useState(0)
    const [scheduleData, setScheduleData] = useState()

    useEffect(() => {
        const handleScroll = (e) => {
            setScrollFromTop(e.target.scrollTop);
            setScrollFromLeft(e.target.scrollLeft);
        }
        let wrapper = document.querySelector('.Timetable__Wrapper')
        if (wrapper) {
            wrapper.addEventListener('scroll', handleScroll, {
                passive: true
            })
            return () => wrapper.removeEventListener("scroll", handleScroll);
        }
    }, [scheduleData])

    useEffect(() => {
        axios.get('schedule.json').then(response => {
            if (response && response.status === 200) {
                setScheduleData(response.data)
            }
        })
    }, []);

    if (scheduleData) {
        return (
            <div className="Timetable">

                <TimetableTeachers teachers={
                    scheduleData.teachers
                } scrollFromTop={scrollFromTop} />
                <TimetableHeader scrollFromLeft={scrollFromLeft}/>

                <div className="Timetable__Wrapper">
                    <div className="Timetable__Sidebar">

                    </div>
                    <div className="Timetable__Content">
                        <TimetableContent teachers={scheduleData.teachers} />
                    </div>
                </div>
            </div>
        )
    } else {
        return <></>
    }


}

export default Timetable