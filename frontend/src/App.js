import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';
import axios from 'axios';


function MyApp({ setApiResponse, isLoading, setIsLoading }) {
    const [text, setText] = useState('');
    const [selectedButton, setSelectedButton] = useState(null);
    const navigate = useNavigate();

    const handleTextChange = (event) => {
        if (event.target.value.length <= 2000) { // 1000文字の制限
            setText(event.target.value);
        }
    };

    const handleButtonClick = (index) => {
        setSelectedButton(index);
    };

    const handleSubmit = async () => {
        setIsLoading(true); // ローディング開始
        try {
            const response = await axios.post(`${process.env.REACT_APP_API_URL}/text2audio`, {
                text: text,
                ButtonID: selectedButton,
            });

            const data = response.data;
            setApiResponse(data);
            // console.log(data);
            navigate('/result');

        } catch (error) {
            console.error(error);
        }
        setIsLoading(false); // ローディング終了
    };

    const buttonTexts = [
        "I'll infuse radio power!",
        "I'll infuse narrative power!",
        "I'll infuse lecture power!",
        "I'll infuse comedy power!"
    ];

    const buttons = [0, 1, 2, 3].map((index) => (
        <button
            key={index}
            className="kotodama-selector"
            onClick={() => handleButtonClick(index)}
            style={selectedButton === index ? { backgroundColor: 'gray' } : {}}
        >
            <img src={`./images/kotodaman-${index + 1}.png`} alt={`kotodama ${index + 1}`} />
            <span>{buttonTexts[index]}</span>
        </button>
    ));


    if (isLoading) {
        return <div className="infusing">Infusing... (Might wait a few minutes)</div>;
    }

    return (
        <div className="app">
            <div className="title">
                <h1>Kotodamize!</h1>
            </div>

            <div className="explain">
                <p>Let's infuse <a href="https://en.wikipedia.org/wiki/Kotodama">KOTODAMA</a> into the text!</p>
            </div>

            <textarea
                className="input"
                value={text}
                onChange={handleTextChange}
                maxLength={2000} 
                wrap="soft" 
            />
            <div className="button-container">{buttons}</div>
            <div className="kotodamize">
                <button onClick={handleSubmit}>Kotodamize!</button>
            </div>
        </div>
    );
}

function Result({ apiResponse }) {
    return (
        <div className="app">
            <h1>Listen to KOTODAMA whispering...</h1>
            <audio controls src={`${process.env.REACT_APP_API_URL}/audio/${apiResponse.audio_path}`} />
            <div className="transformed-text">
                {apiResponse.transformed_text.split('\n').map((line, index) => (
                    <span key={index}>
                        {line}
                        <br />
                    </span>
                ))}
            </div>
        </div>
    );
}

function App() {
    const [apiResponse, setApiResponse] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    return (
        <Router>
            <Routes>
                <Route path="/result" element={<Result apiResponse={apiResponse} />} />
                <Route path="/" element={<MyApp setApiResponse={setApiResponse} isLoading={isLoading} setIsLoading={setIsLoading} />} />
            </Routes>
        </Router>
    );
}

export default App;
