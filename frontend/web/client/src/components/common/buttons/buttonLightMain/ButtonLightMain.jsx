import React from 'react';

const ButtonLightMain = ({to, children}) => {
    return (
        <Link to={to} className='buttonLightMain'>{children}</Link>
    );
}
export default ButtonLightMain;
