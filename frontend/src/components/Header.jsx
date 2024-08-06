import React from "react"
import { Link, useNavigate } from "react-router-dom"

function Header() {
  const navigate = useNavigate()

  const handleClick = () => {
    navigate("/", { replace: true })
    window.location.reload()
  }

  return (
    <nav className="bg-white shadow-md">
      <div className="w-full px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center flex-1 space-x-6">
            <Link
              to="/"
              className="text-2xl font-bold text-black"
              onClick={handleClick}
            >
              CryptoTracker
            </Link>
            <div className="flex items-center space-x-4">
              <Link
                to="/cryptocurrencies"
                className="text-sm text-black font-bold hover:text-blue-600"
              >
                Cryptocurrencies
              </Link>
              <Link
                to="/portfolio"
                className="text-sm text-black font-bold hover:text-blue-600"
              >
                Portfolio
              </Link>
            </div>
          </div>
          <div className="flex items-center justify-end space-x-4">
            <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-gray-100 hover:border-blue-800 hover:text-blue-800 transition">
              Login
            </button>
            <button className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
              Sign Up
            </button>
          </div>
        </div>
        <hr className="border-t border-gray-300 my-2" />
        {/* Зменшено відступи */}
      </div>
    </nav>
  )
}

export default Header
