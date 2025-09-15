import React from 'react';
import SidebarElementApplication from '../sidebarElementApplication/SidebarElementApplication';

const SidebarApplication = () => {
    return (
        <div className='SidebarApplication'>
            <SidebarElementApplication to="/app/dashboard">Dashboard</SidebarElementApplication>
            <SidebarElementApplication to="/app/jobs">Jobs</SidebarElementApplication>
            <SidebarElementApplication to="/app/polls">Polls</SidebarElementApplication>
            <SidebarElementApplication to="/app/conflicts">Conflicts</SidebarElementApplication>
            <SidebarElementApplication to="/app/clan">clan</SidebarElementApplication>
            <SidebarElementApplication to="/app/off-days">Off Days</SidebarElementApplication>
            <SidebarElementApplication to="/app/settings">Settings</SidebarElementApplication>
        </div>
    );
}

export default SidebarApplication;
