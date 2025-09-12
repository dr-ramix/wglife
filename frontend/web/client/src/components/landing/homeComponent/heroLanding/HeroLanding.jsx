import React from 'react';
import ButtonLightMain from '../../../common/buttons/buttonLightMain/ButtonLightMain';
import ButtonDarkMain from '../../../common/buttons/buttonDarkMain/ButtonDarkMain';

const HeroLanding = () => {
    return (
        <div className='heroLanding'>
           <div className="heroLandingContainer">
              <div className='heroLandingLeft'>
                <h1>Manage your shared flat professionally</h1>
                <p>
                All you need for your shared flat, task scheduler, polls, conflicts and chats. 
                Build to automate your shared flat management.
                </p>
                <div className='heroLandingButtonGroupOne'>
                <ButtonDarkMain to="/app">Use Web Version</ButtonDarkMain>
                <button>Watch Demo</button>
                </div>
                <div className='heroLandingButtonGroupTwo'>
                 <span>Download for IOS</span>
                 <span>Download for Android</span>
                </div>
              </div>
              <div className='heroLandingRight'>

              </div>
           </div>
        </div>
    );
}

export default HeroLanding;
