import React from 'react';
import { Outlet } from 'react-router-dom';
const LandingLayoutPage = () => {
    return (
        <div className='landingLayoutPage'>
            <main>
                <Outlet />
            </main>
        </div>
    );
}
export default LandingLayoutPage;
