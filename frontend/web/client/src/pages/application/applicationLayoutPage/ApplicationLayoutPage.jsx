import React from 'react';
import { Routes, Route, Link, Outlet } from 'react-router-dom';

const ApplicationLayoutPage = () => {
    return (
        <div className='applicationLayoutPage'>
            ApplicationLayoutPage
            <main>
                <Outlet />
            </main>
        </div>
    );
}

export default ApplicationLayoutPage;
