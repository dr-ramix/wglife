import React from 'react';
import { Outlet } from 'react-router-dom';
import NavbarLanding from '../../../components/landing/navbarLanding/NavbarLanding';
import FooterLanding from '../../../components/landing/footerLanding/FooterLanding';
const LandingLayoutPage = () => {
    return (
        <div className='landingLayoutPage'>
            <NavbarLanding />
            <main>
                <Outlet />
            </main>
            <FooterLanding />
        </div>
    );
}
export default LandingLayoutPage;
