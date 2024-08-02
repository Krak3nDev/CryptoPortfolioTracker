import React, { useState } from "react"
import { AiFillEye, AiFillEyeInvisible } from "react-icons/ai"

function SignIn() {
  const [showPassword, setShowPassword] = useState(false)

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword)
  }

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="container mx-auto bg-white text-white p-4 w-[496px] h-[683px] rounded-xl flex flex-col items-center">
        <div className="flex space-x-12 mt-3">
          <button className="font-bold text-[22px] text-black">Log In</button>
          <button className="font-bold text-[22px] text-black">Sign Up</button>
        </div>
        <div className="mt-10 w-full px-[30px]">
          <div className="mb-4 w-full">
            <label className="block text-gray-600 mb-2 text-xs" htmlFor="email">
              Email Address
            </label>
            <div className="flex items-center border border-gray-300 rounded-lg bg-white h-14 transition duration-300 ease-in-out hover:border-blue-500 focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-200">
              <input
                type="email"
                id="email"
                placeholder="Enter your email address"
                className="flex-1 bg-transparent outline-none text-black h-full px-4"
              />
            </div>
          </div>
          <div className="mb-4 w-full">
            <div className="flex justify-between items-center mb-2">
              <label className="text-gray-600 text-xs" htmlFor="password">
                Password
              </label>
              <a
                href="/forgot-password"
                className="text-blue-500 text-xs hover:underline"
              >
                Forgot password?
              </a>
            </div>
            <div className="flex items-center border border-gray-300 rounded-lg bg-white h-14 transition duration-300 ease-in-out hover:border-blue-500 focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-200">
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                placeholder="Enter your password"
                className="flex-1 bg-transparent outline-none text-black h-full px-4"
              />
              <button
                type="button"
                onClick={togglePasswordVisibility}
                className="text-gray-500 hover:text-gray-700 flex justify-center items-center w-8 h-8 mr-4 transition duration-300 ease-in-out"
              >
                {showPassword ? (
                  <AiFillEye size={24} />
                ) : (
                  <AiFillEyeInvisible size={24} />
                )}
              </button>
            </div>
          </div>
          <button className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg text-[18px] mt-4">
            Log In
          </button>
        </div>
      </div>
    </div>
  )
}

export default SignIn
