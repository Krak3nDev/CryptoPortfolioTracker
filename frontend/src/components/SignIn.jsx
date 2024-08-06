import React, { useEffect, useRef, useState } from "react"
import { AiFillEye, AiFillEyeInvisible } from "react-icons/ai"

function SignIn() {
  const [showPassword, setShowPassword] = useState(false)
  const [isButtonFocused, setIsButtonFocused] = useState(false)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [username, setUsername] = useState("")
  const [isSignUp, setIsSignUp] = useState(false)
  const [isForgotPassword, setIsForgotPassword] = useState(false)
  const emailInputRef = useRef(null)
  const usernameInputRef = useRef(null)

  useEffect(() => {
    if (isSignUp && usernameInputRef.current) {
      usernameInputRef.current.focus()
    } else if (!isSignUp && emailInputRef.current) {
      emailInputRef.current.focus()
    } else if (isForgotPassword && emailInputRef.current) {
      emailInputRef.current.focus()
    }
  }, [isSignUp, isForgotPassword])

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword)
  }

  const isDisabled =
    email === "" || password === "" || (isSignUp && username === "")

  const resetFields = () => {
    setEmail("")
    setPassword("")
    setUsername("")
    setShowPassword(false)
    setIsButtonFocused(false)
  }

  const handleSignUpClick = () => {
    resetFields()
    setIsSignUp(true)
    setIsForgotPassword(false)
  }

  const handleLogInClick = () => {
    resetFields()
    setIsSignUp(false)
    setIsForgotPassword(false)
  }

  const handleForgotPasswordClick = () => {
    resetFields()
    setIsForgotPassword(true)
  }

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="container mx-auto bg-white p-6 w-[550px] h-[600px] transition-all duration-300 rounded-xl flex flex-col items-center">
        <div className="relative flex items-center justify-center w-full mt-5">
          <div className="space-x-12">
            <button
              className={`font-bold text-[35px] ${isSignUp ? "text-gray-500" : "text-black"}`}
              onClick={handleLogInClick}
            >
              Log In
            </button>
            <button
              className={`font-bold text-[35px] ${isSignUp ? "text-black" : "text-gray-500"}`}
              onClick={handleSignUpClick}
            >
              Sign Up
            </button>
          </div>
          <div
            className={`absolute bottom-0 w-[120px] h-[4px] rounded-full bg-[#3861FB] transition-all duration-300 ease-in-out ${
              isSignUp ? "translate-x-[96px]" : "-translate-x-[96px]"
            }`}
          ></div>
        </div>
        {isForgotPassword ? (
          <div className="mt-8 w-full px-[40px]">
            <h2 className="text-2xl font-bold">Forgot your password?</h2>
            <p className="text-gray-500 mt-2 mb-4">
              Enter your email below, you will receive an email with
              instructions on how to reset your password in a few minutes. You
              can also set a new password if you've never set one before.
            </p>
            <label htmlFor="email" className="block mb-3 text-lg font-bold">
              Email Address
            </label>
            <div
              className={`flex items-center border border-gray-300 rounded-lg bg-white h-16 transition duration-300 ease-in-out ${
                isButtonFocused ? "" : "hover:border-blue-500"
              } focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-200`}
            >
              <input
                type="email"
                id="email"
                ref={emailInputRef}
                placeholder="Enter your e-mail address"
                className="flex-1 bg-transparent outline-none text-black h-full px-4 text-lg"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <button
              className={`w-full py-3 px-4 rounded-lg text-[20px] mt-5 ${
                email === ""
                  ? "bg-[#9BB0FD] cursor-not-allowed text-white"
                  : "bg-blue-500 text-white hover:bg-blue-600"
              }`}
              disabled={email === ""}
            >
              Send Instructions
            </button>
          </div>
        ) : (
          <div className="mt-8 w-full px-[40px]">
            {isSignUp && (
              <>
                <label
                  htmlFor="username"
                  className="block mb-3 text-lg font-bold"
                >
                  Username
                </label>
                <div
                  className={`flex items-center border border-gray-300 rounded-lg bg-white h-16 transition duration-300 ease-in-out ${
                    isButtonFocused ? "" : "hover:border-blue-500"
                  } focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-200 mb-4`}
                >
                  <input
                    type="text"
                    id="username"
                    placeholder="Enter your username"
                    className="flex-1 bg-transparent outline-none text-black h-full px-4 text-lg"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    ref={usernameInputRef}
                  />
                </div>
              </>
            )}
            <label htmlFor="email" className="block mb-3 text-lg font-bold">
              Email Address
            </label>
            <div
              className={`flex items-center border border-gray-300 rounded-lg bg-white h-16 transition duration-300 ease-in-out ${
                isButtonFocused ? "" : "hover:border-blue-500"
              } focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-200`}
            >
              <input
                type="email"
                id="email"
                ref={emailInputRef}
                placeholder="Enter your email address"
                className="flex-1 bg-transparent outline-none text-black h-full px-4 text-lg"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="flex justify-between items-center mt-5 mb-3">
              <label htmlFor="password" className="text-lg font-bold">
                Password
              </label>
              {!isSignUp && (
                <button
                  onClick={handleForgotPasswordClick}
                  className="text-blue-500 text-sm hover:underline"
                >
                  Forgot password?
                </button>
              )}
            </div>
            <div
              className={`relative flex items-center border border-gray-300 rounded-lg bg-white h-16 transition duration-300 ease-in-out ${
                isButtonFocused ? "" : "hover:border-blue-500"
              } focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-200`}
            >
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                placeholder="Enter your password"
                className="w-full bg-transparent outline-none text-black h-full pl-4 pr-12 border-none rounded-lg transition duration-300 ease-in-out text-lg"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button
                type="button"
                onMouseDown={togglePasswordVisibility}
                onMouseEnter={() => setIsButtonFocused(true)}
                onMouseLeave={() => setIsButtonFocused(false)}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 p-0 text-gray-500 hover:text-gray-700 flex justify-center items-center transition duration-300 ease-in-out w-[28px] h-[28px]"
              >
                {showPassword ? (
                  <AiFillEye size={28} />
                ) : (
                  <AiFillEyeInvisible size={28} />
                )}
              </button>
            </div>
            <button
              className={`w-full py-3 px-4 rounded-lg text-[20px] mt-5 ${
                isDisabled
                  ? "bg-[#9BB0FD] cursor-not-allowed text-white"
                  : "bg-blue-500 text-white hover:bg-blue-600"
              }`}
              disabled={isDisabled}
            >
              {isSignUp ? "Sign Up" : "Log In"}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default SignIn
