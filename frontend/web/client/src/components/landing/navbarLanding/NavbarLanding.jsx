import React from 'react';
import ButtonLightMain from '../../common/buttons/buttonLightMain/ButtonLightMain';
import ButtonDarkMain from '../../common/buttons/buttonDarkMain/ButtonDarkMain';

const NavbarLanding = () => {
    return (
        <nav className='navbarLanding'>
          <div className='navbarLandingContainer'>
          <div className='navbarLandingLeft'>
            <span>Lego</span>
            <span>WGLife</span>
          </div>
          <div className='navbarLadingRight'>
             <ButtonLightMain to="/tutorial">Tutorial</ButtonLightMain>
             <ButtonLightMain to="/pricing">Pricing</ButtonLightMain>
             <ButtonLightMain to="/contact">Contact</ButtonLightMain>
             <ButtonDarkMain to="/login">Log In</ButtonDarkMain>
             <ButtonDarkMain to="/register">Sign In</ButtonDarkMain>
          </div>
          </div>
        </nav>
    );
}

export default NavbarLanding;