import React from 'react'

const DAYS_OF_WEEK = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
const MONTH_TITLES = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];


function SmallCalendar(props) {

    const currentDate = props.currentDate
    let weekDays = []
    let currentMonth = MONTH_TITLES[currentDate?.getMonth()]
    if (currentDate) {
        const day = currentDate?.getDate();
        const startOfWeek = new Date(currentDate);
        startOfWeek.setDate(currentDate.getDate() - day + (day === 0 ? -6 : 1));
        weekDays = Array.from({ length: 7 }, (_, index) => {
            const day = new Date(startOfWeek);
            day.setDate(startOfWeek.getDate() + index);
            return {
                'day': day.getDay(),
                'dayOfWeek': DAYS_OF_WEEK[index]
            };
        });
    }


    return (
        <div className="SmallCalendar">
            <div className="SmallCalendar__Month">{ currentMonth }</div>
            <div className="SmallCalendar__Days">
            { weekDays.map((el, index) => (
                <div onClick={() => {props.setSelected(index)}} className={"SmallCalendar__Item " + (props.selected == index ? '_active' : '')} >
                    <div className="SmallCalendar__Day">{ el.day }</div>
                    <div className="SmallCalendar__DayWeek">{ el.dayOfWeek }</div>
                </div>
            )) }
            </div>
        </div>
    )

}

export default SmallCalendar