import News from "../components/Home/News";
import Welcome from "../components/Home/Welcome";
import Sidebar from "../components/Home/Sidebar";
import {useEffect} from "react";

export default function Home() {

    useEffect(() => {
        const sse = new EventSource('[YOUR_SSE_ENDPOINT_URL]',
            { withCredentials: true });
        function getRealtimeData(data) {
            console.log(data)
        }
        sse.onmessage = e => getRealtimeData(JSON.parse(e.data));
        sse.onerror = (error) => {
            console.error('sse error', error)
            sse.close();
        }
        return () => {
            sse.close();
        };
    }, []);

    return (
        <div className="Home">
            <div className="Container">
                <div className="Row Home__Row">
                    <div className="Home__Col">
                        <News school="Музыкальная академия" news={[
                            {"id": 2, "title": "Завершение музыкального фестиваля", "time": "вчера", "passed": true},
                            {"id": 4, "title": "Концерт студентов", "time": "вчера", "passed": false},
                            {"id": 8, "title": "Конкурс молодых талантов", "time": "вчера", "passed": false},
                            {"id": 11, "title": "Музыкальная программа в честь юбилея академии", "time": "вчера", "passed": true},
                            {"id": 3, "title": "Открытие выставки инструментов", "time": "3 дня назад", "passed": false},
                            {"id": 10, "title": "Театральная постановка на музыкальную тему", "time": "3 дня назад", "passed": false},
                            {"id": 7, "title": "Интервью с дирижером академии", "time": "4 дня назад", "passed": true}
                        ]}/>
                    </div>
                    <div className="Home__Col">
                        <Welcome />
                    </div>
                    <div className="Home__Col">
                        <Sidebar
                            current={[
                                {id: 7, timestart: new Date().toString(), timeend: new Date().toString(), subject: 'Живопись', room: 491, teacher: 'Иванова И.И.', group: 'P33121', isIndividual: false},
                                {id: 7, timestart: new Date().toString(), timeend: new Date().toString(), subject: 'Живопись', room: 491, teacher: 'Иванова И.И.', group: 'P33121', isIndividual: false},
                                {id: 7, timestart: new Date().toString(), timeend: new Date().toString(), subject: 'Живопись', room: 491, teacher: 'Иванова И.И.', group: 'P33121', isIndividual: false},
                                {id: 7, timestart: new Date().toString(), timeend: new Date().toString(), subject: 'Живопись', room: 491, teacher: 'Иванова И.И.', group: 'P33121', isIndividual: false},

                            ]}
                            teacherCount={16} studentCount={166} username="Зинатулин Артём Витальевич" role="администратор" />
                    </div>
                </div>
            </div>
        </div>
    );
}