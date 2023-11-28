import React, {useState} from 'react'

function Welcome(props) {

    const [LLMQuery, setLLMQuery] = useState('')

    return (
        <div className="Welcome">
            <div className="Welcome__Wrapper">
                <div className="Welcome__Logo">
                    <img src="assets/images/logo.svg" alt="Звёздник"/>
                </div>
                <div className="Welcome__Information">
                    <h1>Звёздник</h1>
                    <p>Добро пожаловать в дневник администратора</p>
                </div>
                <div className="Welcome__LLM">
                    <label htmlFor="llm-query">
                        Пожалуйста, <br/>
                        сформулируйте свой запрос
                    </label>
                    <textarea
                        onChange={(event) => setLLMQuery(event.target.value)}
                        name="llm-query" id="llm-query"
                        placeholder="Выведи список оценок и их среднее арифметическое за прошедшую четверть у Иванова А.С."
                        value={LLMQuery}
                    ></textarea>
                    <button>Поехали <img src="assets/images/next.svg" alt="Go!"/></button>
                </div>
            </div>
        </div>
    )

}

export default Welcome