import React from 'react';
import { Link } from 'react-router-dom';

const SidebarElementApplication = ({to, children}) => {
    return (
        <div className='SidebarElementApplication'>
            <Link to={to} className='sidebarElementApplicationLink'>{children}</Link>
        </div>
    );
}

export default SidebarElementApplication;
