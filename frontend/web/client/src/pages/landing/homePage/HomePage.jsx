import React from 'react'
import HeroLanding from '../../../components/landing/homeComponent/heroLanding/HeroLanding'
import FeaturesLanding from '../../../components/landing/homeComponent/featuresLanding/FeaturesLanding'

function HomePage() {
  return (
    <div className='landingHomePage'>
        <HeroLanding />
        <FeaturesLanding />
    </div>
  )
}

export default HomePage
