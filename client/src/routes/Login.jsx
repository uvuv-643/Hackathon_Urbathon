import React, {useState} from 'react'
import {Link} from "react-router-dom";

function Login(props) {

    const [login, setLogin] = useState('')
    const [password, setPassword] = useState('')

    return (
        <div className="Login">
            <div className="Login__Wrapper">
                <div className="Login__Logo">
                    <img src="assets/images/logo.svg" alt="Звёздник"/>
                </div>
                <div className="Login__Information">
                    <h1>Звёздник</h1>
                    <p>Добро пожаловать в ваш личный дневник</p>
                </div>
                <div className="Login__Form">
                    <label htmlFor="login">
                        Пожалуйста, <br/>
                        введите ваш e-mail и пароль
                    </label>
                    <input
                        onChange={(event) => setLogin(event.target.value)}
                        name="login" id="login"
                        placeholder="Введите Ваш e-mail"
                        value={login}
                    />
                    <input
                        onChange={(event) => setPassword(event.target.value)}
                        name="login" id="login"
                        placeholder="Введите Ваш пароль"
                        value={login}
                    />
                    <Link to="/">Поехали <img src="assets/images/next.svg" alt="Go!"/></Link>
                </div>
            </div>
        </div>
    )

}

export default Login