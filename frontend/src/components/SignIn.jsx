import React, { useState } from "react"
import { AiFillEye, AiFillEyeInvisible } from "react-icons/ai"

function SignIn() {
  const [showPassword, setShowPassword] = useState(false)
  const [isButtonFocused, setIsButtonFocused] = useState(false) // State for button focus

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword)
  }

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="container mx-auto bg-white p-4 w-[496px] h-[683px] rounded-xl flex flex-col items-center">
        <div className="space-x-12 mt-3">
          <button className="font-bold text-[22px] text-black">Log In</button>
          <button className="font-bold text-[22px] text-black">Sign Up</button>
        </div>
        <div className="mt-10 w-full px-[30px]">
          <label htmlFor="email" className="block text-gray-600 mb-2 text-xs">
            Email Address
          </label>
          <div
            className={`flex items-center border border-gray-300 rounded-lg bg-white h-14 transition duration-300 ease-in-out ${
              isButtonFocused ? "" : "hover:border-blue-500"
            } focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-200`}
          >
            <input
              type="email"
              id="email"
              placeholder="Enter your email address"
              className="flex-1 bg-transparent outline-none text-black h-full px-4"
            />
          </div>
          <div className="flex justify-between items-center mt-4 mb-2">
            <label htmlFor="password" className="text-gray-600 text-xs">
              Password
            </label>
            <a
              href="/forgot-password"
              className="text-blue-500 text-xs hover:underline"
            >
              Forgot password?
            </a>
          </div>
          <div
            className={`relative flex items-center border border-gray-300 rounded-lg bg-white h-14 transition duration-300 ease-in-out ${
              isButtonFocused ? "" : "hover:border-blue-500"
            } focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-200`}
          >
            <input
              type={showPassword ? "text" : "password"}
              id="password"
              placeholder="Enter your password"
              className="w-full bg-transparent outline-none text-black h-full pl-4 pr-12 border-none rounded-lg transition duration-300 ease-in-out"
            />
            <button
              type="button"
              onMouseDown={togglePasswordVisibility}
              onMouseEnter={() => setIsButtonFocused(true)}
              onMouseLeave={() => setIsButtonFocused(false)}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 p-0 text-gray-500 hover:text-gray-700 flex justify-center items-center transition duration-300 ease-in-out"
              style={{ width: "24px", height: "24px" }}
            >
              {showPassword ? (
                <AiFillEye size={24} />
              ) : (
                <AiFillEyeInvisible size={24} />
              )}
            </button>
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
