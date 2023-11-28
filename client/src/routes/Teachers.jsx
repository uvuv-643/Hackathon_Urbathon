import React, {useEffect, useState} from 'react'
import {Link} from "react-router-dom";
import axios from "axios";

function Teachers(props) {

    const [fakeData, setFakeData] = useState([])

    useEffect(() => {
        axios.get('teachers.json').then(response => {
            if (response && response.status === 200) {
                setFakeData(response.data)
            }
        })
    }, []);

    return (
        <div className="Schedule Table">
            <Link to='/' className="Schedule__Back"><img src="assets/images/back.svg" alt="back"/>На главную</Link>
            <div className="Table__Wrapper">
                <table border="1">
                    <thead>
                    <tr>
                        <th>ID</th>
                        <th>ФИО</th>
                        <th>Стаж</th>
                        <th>Специализация</th>
                        <th>Роль</th>
                        <th>Количество рабочих часов</th>
                    </tr>
                    </thead>
                    <tbody>
                    {fakeData.map((row) => (
                        <tr key={row.id}>
                            <td>{row.id}</td>
                            <td>{row.fullName}</td>
                            <td>{row.experience}</td>
                            <td>{row.specialization}</td>
                            <td>{row.role}</td>
                            <td>{row.workingHours}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default Teachers