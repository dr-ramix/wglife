import React from 'react';
import { Link } from 'react-router-dom';

const ButtonDarkMain = ({to, children}) => {
    return (
        <Link to={to} className='buttonDarkMain'>{children}</Link>
    );
}
export default ButtonDarkMain;
