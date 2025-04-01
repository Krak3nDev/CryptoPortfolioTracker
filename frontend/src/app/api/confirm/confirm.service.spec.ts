import { TestBed } from "@angular/core/testing"
import { ConfirmService } from "./confirm.service"
import {
  HttpClientTestingModule,
  HttpTestingController
} from "@angular/common/http/testing"
import { ENDPOINTS } from "../../consts/endpoints"

describe("ConfirmService", () => {
  let service: ConfirmService
  let httpMock: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ConfirmService]
    })
    service = TestBed.inject(ConfirmService)
    httpMock = TestBed.inject(HttpTestingController)
  })

  afterEach(() => {
    httpMock.verify()
  })

  it("should be created", () => {
    expect(service).toBeTruthy()
  })

  describe("confirm", () => {
    const testToken = "test-token-123"

    it("should send GET request to confirm endpoint with token", () => {
      service.confirm({ token: testToken }).subscribe()

      const req = httpMock.expectOne(ENDPOINTS.users.confirm(testToken))
      expect(req.request.method).toBe("GET")
      req.flush({})
    })
  })
})
