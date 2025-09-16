import React from 'react';

const RecentActivityApplication = ({profilePicture, username, title, dateTime }) => {
    return (
        <div className='recentActivityApplication'>
            <div className='recentActivityApplicationProfilePictureWrapper'>
                <img width="15px" src={profilePicture} alt="Profile" />
            </div>
            <div className='recentActivityApplicationInfoWrapper'>
                <span className='recentActivityApplicationUsername'>{username}</span>
                <span className='recentActivityApplicationTitle'>{title}</span>
                <span className='recentActivityApplicationDateTime'>{dateTime}</span>
            </div>
        </div>
    );
}

export default RecentActivityApplication;
