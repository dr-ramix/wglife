import React from 'react';

const ButtonDarkMain = ({to, children}) => {
    return (
        <Link to={to} className='buttonDarkMain'>{children}</Link>
    );
}
export default ButtonDarkMain;
