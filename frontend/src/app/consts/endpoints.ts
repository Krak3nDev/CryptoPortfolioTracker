export const BASE_API_URL = "http://localhost:8000"

export const ENDPOINTS = {
  auth: {
    register: `${BASE_API_URL}/auth/register`,
    login: `${BASE_API_URL}/auth/login`,
    logout: `${BASE_API_URL}/auth/logout`
  },
  users: {
    confirm: (token: string) => `${BASE_API_URL}/users/confirm/${token}`
  }
}
