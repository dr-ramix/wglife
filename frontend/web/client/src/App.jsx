
import './App.css'
import {Route, Routes, Link} from "react-router-dom"

import HomePage from './pages/landing/homePage/HomePage'
import LoginPage from './pages/landing/loginPage/LoginPage'
import RegisterPage from './pages/landing/resgisterPage/RegisterPage'
import DocsPage from './pages/landing/docsPage/DocsPage'
import ContactPage from './pages/landing/contactPage/ContactPage'
import NotFoundPage from './pages/landing/notFoundPage/NotFoundPage'
import AppLayoutPage from './pages/application/appLayoutPage/AppLayoutPage'
import MyProfilePage from './pages/application/myProfilePage/MyProfilePage'
import DashboardPage from './pages/application/dashboardPage/DashboardPage'


function App() {

  return (
    <div>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/docs" element={<DocsPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/app/" element={<AppLayoutPage />}>
            <Route index element={<DashboardPage />} /> {/* /app */}
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="my-profile" element={<MyProfilePage />} />
        </Route>
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </div>
  )
}

export default App
