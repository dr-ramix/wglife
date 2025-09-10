
import './App.css'
import {Route, Routes, Link} from "react-router-dom"
import Home from './pages/home/Home'
function App() {

  return (
    <div>
      <Routes>
        <Route path="/home" element={<Home />} />
      </Routes>
    </div>
  )
}

export default App
