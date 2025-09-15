
import './App.css'
import {Route, Routes, Link} from "react-router-dom"

import HomePage from './pages/landing/homePage/HomePage'
import LoginPage from './pages/landing/loginPage/LoginPage'
import RegisterPage from './pages/landing/registerPage/RegisterPage'
import DocsPage from './pages/landing/docsPage/DocsPage'
import ContactPage from './pages/landing/contactPage/ContactPage'
import NotFoundPage from './pages/landing/notFoundPage/NotFoundPage'
import AppLayoutPage from './pages/application/applicationLayoutPage/ApplicationLayoutPage'
import MyProfilePage from './pages/application/myProfilePage/MyProfilePage'
import DashboardPage from './pages/application/dashboardPage/DashboardPage'
import ClanPage from './pages/application/clanPage/ClanPage'
import WelcomePage from './pages/application/welcomePage/WelcomePage'
import SettingPage from './pages/application/settingPage/SettingPage'
import OffDaysPage from './pages/application/offdaysPage/OffdaysPage'
import ConflictsPage from './pages/application/conflictsPage/ConflictsPage'
import PollsPage from './pages/application/pollsPage/PollsPage'
import ProfilePage from './pages/application/profilePage/ProfilePage'
import LandingLayoutPage from './pages/landing/landingLayoutPage/LandingLayoutPage'
import ApplicationLayoutPage from './pages/application/applicationLayoutPage/ApplicationLayoutPage'
import PricingPage from './pages/landing/pricingPage/PricingPage'
import TutorialPage from './pages/landing/tutorialPage/TutorialPage'
import JobsPage from './pages/application/jobsPage/JobsPage'

function App() {

  return (
    <div>
      <Routes>
        <Route path="/" element={<LandingLayoutPage />}>
            <Route index element={<HomePage />} />
            <Route path="/docs" element={<DocsPage />} />
            <Route path="/tutorial" element={<TutorialPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/pricing" element={<PricingPage />} />
        </Route>
        <Route path="/app" element={<ApplicationLayoutPage />}>
            <Route index element={<DashboardPage />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="jobs" element={<JobsPage />} />
            <Route path="my-profile" element={<MyProfilePage />} />
            <Route path="clan" element={<ClanPage />} />
            <Route path="welcome" element={<WelcomePage />} />
            <Route path="settings" element={<SettingPage />} />
            <Route path="polls" element={<PollsPage />} />
            <Route path="profile" element={<ProfilePage />} />
            <Route path="off-days" element={<OffDaysPage />} />
            <Route path="conflicts" element={<ConflictsPage />} />
        </Route>
         <Route path="/login" element={<LoginPage />} />
         <Route path="/register" element={<RegisterPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </div>
  )
}

export default App
