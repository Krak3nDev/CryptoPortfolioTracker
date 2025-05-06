export interface RegisterBodyRequest {
  username: string
  email: string
  password: string
}

export interface LoginBodyRequest {
  username: string
  password: string
}

export interface User {
  user_id: number
  email: string
  username: string
  is_active: boolean
}

