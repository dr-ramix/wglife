import React from 'react';
import RecentActivityApplication from '../recentActivityApplication/RecentActivityApplication';

const RecentActivitiesApplication = () => {
    return (
        <div>
            Recent Activities
            <RecentActivityApplication profilePicture={"https://www.w3schools.com/howto/img_avatar.png"} username={"Ramtin"} title={"Created a new post"} dateTime={"2 hours ago"} />
            <RecentActivityApplication profilePicture={"https://www.w3schools.com/howto/img_avatar.png"} username={"Alice"} title={"Commented on your post"} dateTime={"3 hours ago"} />
            <RecentActivityApplication profilePicture={"https://www.w3schools.com/howto/img_avatar.png"} username={"Bob"} title={"Liked your photo"} dateTime={"5 hours ago"} />
            <RecentActivityApplication profilePicture={"https://www.w3schools.com/howto/img_avatar.png"} username={"Charlie"} title={"Started following you"} dateTime={"1 day ago"} />
            <RecentActivityApplication profilePicture={"https://www.w3schools.com/howto/img_avatar.png"} username={"Diana"} title={"Shared your post"} dateTime={"2 days ago"} />
        </div>
    );
}

export default RecentActivitiesApplication;
