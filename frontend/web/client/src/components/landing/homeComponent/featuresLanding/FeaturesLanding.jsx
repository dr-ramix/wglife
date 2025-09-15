import React from 'react';
import FeatureLanding from '../featureLanding/FeatureLanding';

const FeaturesLanding = () => {
    return (
        <div className='featuresLanding'>
            <h2>Features</h2>
            <div className='featuresLandingWrapper'>
                <FeatureLanding logo="LOGO" title="Tasks Scheduling" description="description" />
                <FeatureLanding logo="LOGO" title="Polls" description="description" />
                <FeatureLanding logo="LOGO" title="Conflicts" description="description" />
                <FeatureLanding logo="LOGO" title="Ranking" description="description" />
            </div>
        </div>
    );
}

export default FeaturesLanding;
