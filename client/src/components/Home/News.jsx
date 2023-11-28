import React from 'react'

function News(props) {

    return (
        <div className="News">
            <div className="News__Header">
                {/*<div className="News__Header__Logo">*/}
                {/*    <img src="assets/images/logo.svg" alt="Звёздник" />*/}
                {/*</div>*/}
                <div className="News__Header__Title">
                    <h3>Моя школа</h3>
                    <p>{ props.school }</p>
                </div>
            </div>
            <div className="News__Content">
                <h3>Новости</h3>
                <div className="News__Scroll">
                    { props.news.map((el) => (
                        <div className="News__Item" key={el.id}>
                            <div className="News__Item__Title">
                                <h4>{ el.title }</h4>
                                <p>
                                    <img src="assets/images/time.svg" alt="#"/>
                                    { el.time }
                                </p>
                            </div>
                            <div className="News__Item__Status">
                                { el.passed ? (
                                    <img src="assets/images/checked.svg" alt="#"/>
                                ) : (
                                    <img src="assets/images/unchecked.svg" alt="#"/>
                                ) }
                            </div>
                        </div>
                    )) }
                </div>
                <div className="News__Button">
                    <button>Добавить новость</button>
                </div>
            </div>
        </div>
    )

}

export default News
