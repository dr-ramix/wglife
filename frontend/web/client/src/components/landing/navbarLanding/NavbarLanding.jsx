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
             <ButtonLightMain content="Tutorial" />
             <ButtonLightMain content="Contact" />
             <ButtonLightMain content="Pricing" />
             <ButtonDarkMain content="Log in" />
             <ButtonDarkMain content="Sign up" />
          </div>
          </div>
        </nav>
    );
}

export default NavbarLanding;