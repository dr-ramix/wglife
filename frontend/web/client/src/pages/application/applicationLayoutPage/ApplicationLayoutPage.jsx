import React from 'react';
import { Routes, Route, Link, Outlet } from 'react-router-dom';
import NavbarApplication from '../../../components/application/navbarApplication/NavbarApplication';
import SidebarApplication from '../../../components/application/sidebarApplication/SidebarApplication';

const ApplicationLayoutPage = () => {
    return (
        <div className='applicationLayoutPage'>
            ApplicationLayoutPage
            <NavbarApplication />
            <SidebarApplication />
            <main>
                <Outlet />
            </main>
        </div>
    );
}

export default ApplicationLayoutPage;
