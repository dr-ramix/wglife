import React from 'react';
import { Routes, Route, Link, Outlet } from 'react-router-dom';

const AppLayoutPage = () => {
    return (
        <div className='applicationAppLayoutPage'>
            AppLayoutPage
            <main>
                <Outlet /> 
            </main>
        </div>
    );
}

export default AppLayoutPage;
