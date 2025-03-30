import { inject, Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { LoginBodyRequest, RegisterBodyRequest } from "./auth.interface"
import { ENDPOINTS } from "../../consts/endpoints"

@Injectable({
  providedIn: "root"
})
export class AuthService {
  http = inject(HttpClient)

  register(payload: RegisterBodyRequest) {
    return this.http.post(ENDPOINTS.auth.register, payload)
  }

  login(payload: LoginBodyRequest) {
    return this.http.post(ENDPOINTS.auth.login, payload)
  }

  logout() {
    return this.http.post(ENDPOINTS.auth.logout, {})
  }
}
