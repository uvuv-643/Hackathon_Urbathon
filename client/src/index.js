/* existing imports */
import React from 'react';
import ReactDOM from 'react-dom/client';
import Home from "./routes/Home";
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import './styles/main.scss'
import Login from "./routes/Login";
import Schedule from "./routes/Schedule";
import Teachers from "./routes/Teachers";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Home />,
    },
    {
        path: "/login",
        element: <Login />,
    },
    {
        path: "/schedule",
        element: <Schedule />,
    },
    {
        path: "/teachers",
        element: <Teachers />,
    },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>
);