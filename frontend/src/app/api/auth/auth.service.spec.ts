import { TestBed } from "@angular/core/testing"
import { AuthService } from "./auth.service"
import {
  HttpClientTestingModule,
  HttpTestingController
} from "@angular/common/http/testing"
import { LoginBodyRequest, RegisterBodyRequest } from "./auth.interface"
import { ENDPOINTS } from "../../consts/endpoints"

describe("AuthService", () => {
  let service: AuthService
  let httpMock: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    })
    service = TestBed.inject(AuthService)
    httpMock = TestBed.inject(HttpTestingController)
  })

  afterEach(() => {
    httpMock.verify()
  })

  it("should be created", () => {
    expect(service).toBeTruthy()
  })

  describe("register", () => {
    it("should send POST request to register endpoint", () => {
      const mockPayload: RegisterBodyRequest = {
        username: "testuser",
        email: "test@example.com",
        password: "password123"
      }

      service.register(mockPayload).subscribe()

      const req = httpMock.expectOne(ENDPOINTS.auth.register)
      expect(req.request.method).toBe("POST")
      expect(req.request.body).toEqual(mockPayload)
      req.flush({})
    })
  })

  describe("login", () => {
    it("should send POST request to login endpoint", () => {
      const mockPayload: LoginBodyRequest = {
        username: "testuser",
        password: "password123"
      }

      service.login(mockPayload).subscribe()

      const req = httpMock.expectOne(ENDPOINTS.auth.login)
      expect(req.request.method).toBe("POST")
      expect(req.request.body).toEqual(mockPayload)
      req.flush({})
    })
  })

  describe("logout", () => {
    it("should send POST request to logout endpoint", () => {
      service.logout().subscribe()

      const req = httpMock.expectOne(ENDPOINTS.auth.logout)
      expect(req.request.method).toBe("POST")
      req.flush({})
    })
  })
})
