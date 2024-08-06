import React from "react"
import "./App.css"
import { BrowserRouter, Route, Routes } from "react-router-dom"
import MainPage from "./pages/MainPage.jsx"

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<MainPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
