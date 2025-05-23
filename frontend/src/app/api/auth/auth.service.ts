import { inject, Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { LoginBodyRequest, RegisterBodyRequest, User } from "./auth.interface"
import { ENDPOINTS } from "../../consts/endpoints"
import { BehaviorSubject, tap } from "rxjs"
import { httpConfig } from "../../config/http.config"
import { Router } from "@angular/router"
import { ROUTES } from "../../consts/routes"

@Injectable({
  providedIn: "root"
})
export class AuthService {
  http = inject(HttpClient)
  router = inject(Router)

  private meSubject = new BehaviorSubject<User | null>(null)
  me$ = this.meSubject.asObservable()

  get me() {
    return this.meSubject.value
  }

  constructor() {
    this.updateMe()
  }

  private updateMe() {
    this.getMe().subscribe(
      user => this.meSubject.next(user),
      _error => this.meSubject.next(null)
    )
  }

  register(payload: RegisterBodyRequest) {
    return this.http
      .post(ENDPOINTS.auth.register, payload, httpConfig)
      .pipe(tap(() => this.updateMe()))
  }

  login(payload: LoginBodyRequest) {
    return this.http
      .post(ENDPOINTS.auth.login, payload, httpConfig)
      .pipe(tap(() => this.updateMe()))
  }

  logout() {
    return this.http.post(ENDPOINTS.auth.logout, {}, httpConfig).pipe(
      tap(() => {
        this.meSubject.next(null)
        this.router.navigate(["/" + ROUTES.home])
      })
    )
  }

  getMe() {
    return this.http.get<User>(ENDPOINTS.users.me, httpConfig)
  }
}
