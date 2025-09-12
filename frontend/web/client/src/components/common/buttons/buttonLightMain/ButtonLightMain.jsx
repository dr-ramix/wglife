import React from 'react';
import { Link } from 'react-router-dom';

const ButtonLightMain = ({to, children}) => {
    return (
        <Link to={to} className='buttonLightMain'>{children}</Link>
    );
}
export default ButtonLightMain;
