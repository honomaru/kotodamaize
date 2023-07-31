import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import './fonts/Press_Start_2P/PressStart2P-Regular.ttf';
import { makeServer } from './mockServer';  // API mocking. If you want to use the real API, comment out this line.


if (process.env.NODE_ENV === 'development') {
  // makeServer(); // API mocking. If you want to use the real API, comment out this line.
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
