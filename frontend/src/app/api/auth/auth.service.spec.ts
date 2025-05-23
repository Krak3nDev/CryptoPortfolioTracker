import { TestBed } from "@angular/core/testing"
import {
  HttpClientTestingModule,
  HttpTestingController
} from "@angular/common/http/testing"
import { RouterTestingModule } from "@angular/router/testing"
import { AuthService } from "./auth.service"
import { LoginBodyRequest, RegisterBodyRequest, User } from "./auth.interface"
import { Router } from "@angular/router"
import { ENDPOINTS } from "../../consts/endpoints"
import { ROUTES } from "../../consts/routes"

describe("AuthService", () => {
  let service: AuthService
  let httpMock: HttpTestingController
  let router: Router

  const mockUser: User = {
    user_id: 1,
    email: "test@example.com",
    username: "testuser",
    is_active: true
  }

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, RouterTestingModule],
      providers: [AuthService]
    })

    service = TestBed.inject(AuthService)
    httpMock = TestBed.inject(HttpTestingController)
    router = TestBed.inject(Router)

    const req = httpMock.expectOne(ENDPOINTS.users.me)
    expect(req.request.method).toBe("GET")
    req.flush(null)
  })

  afterEach(() => {
    httpMock.verify()
  })

  it("should be created", () => {
    expect(service).toBeTruthy()
  })

  describe("getMe", () => {
    it("should fetch current user", () => {
      service.getMe().subscribe(user => {
        expect(user).toEqual(mockUser)
      })

      const req = httpMock.expectOne(ENDPOINTS.users.me)
      expect(req.request.method).toBe("GET")
      req.flush(mockUser)
    })
  })

  describe("register", () => {
    it("should register a new user", () => {
      const registerData: RegisterBodyRequest = {
        username: "newuser",
        email: "new@example.com",
        password: "password123"
      }

      service.register(registerData).subscribe(() => {
        expect(service.me).toEqual(mockUser)
      })

      const registerReq = httpMock.expectOne(ENDPOINTS.auth.register)
      expect(registerReq.request.method).toBe("POST")
      expect(registerReq.request.body).toEqual(registerData)
      registerReq.flush({})

      const meReq = httpMock.expectOne(ENDPOINTS.users.me)
      meReq.flush(mockUser)
    })
  })

  describe("login", () => {
    it("should login user", () => {
      const loginData: LoginBodyRequest = {
        username: "testuser",
        password: "password123"
      }

      service.login(loginData).subscribe(() => {
        expect(service.me).toEqual(mockUser)
      })

      const loginReq = httpMock.expectOne(ENDPOINTS.auth.login)
      expect(loginReq.request.method).toBe("POST")
      expect(loginReq.request.body).toEqual(loginData)
      loginReq.flush({})

      const meReq = httpMock.expectOne(ENDPOINTS.users.me)
      meReq.flush(mockUser)
    })
  })

  describe("logout", () => {
    it("should logout user and navigate to home", () => {
      const navigateSpy = jest.spyOn(router, "navigate")

      service.logout().subscribe(() => {
        expect(service.me).toBeNull()
        expect(navigateSpy).toHaveBeenCalledWith([ROUTES.home])
      })

      const req = httpMock.expectOne(ENDPOINTS.auth.logout)
      expect(req.request.method).toBe("POST")
      req.flush({})
    })
  })
})
