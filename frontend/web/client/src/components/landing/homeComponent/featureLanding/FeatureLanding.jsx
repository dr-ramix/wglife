import React from 'react';

const FeatureLanding = ({logo, title, description}) => {
    return (
        <div className='featureLanding'>
          <span>{logo}</span>
          <span>{title}</span>
          <p>{description}</p>
        </div>
    );
}

export default FeatureLanding;
