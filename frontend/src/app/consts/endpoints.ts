export const BASE_API_URL = "http://localhost/api"

export const ENDPOINTS = {
  auth: {
    register: `${BASE_API_URL}/auth/register`,
    login: `${BASE_API_URL}/auth/login`,
    logout: `${BASE_API_URL}/auth/logout`
  },
  users: {
    confirm: (token: string) => `${BASE_API_URL}/users/confirm/${token}`,
    me: `${BASE_API_URL}/users/me`
  },
  portfolios: {
    main: `${BASE_API_URL}/portfolios`,
    summary: `${BASE_API_URL}/portfolios/summary`,
    byId: (id: string) => `${BASE_API_URL}/portfolios/${id}`,
    byIdSummary: (id: string) => `${BASE_API_URL}/portfolios/${id}/summary`
  },
  transactions: (portfolio_id: string) => ({
    main: `${BASE_API_URL}/portfolios/${portfolio_id}/transactions`,
    byId: (transaction_id: string) =>
      `${BASE_API_URL}/portfolios/${portfolio_id}/transactions/${transaction_id}`
  })
}
