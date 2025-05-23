import { TestBed } from "@angular/core/testing"
import {
  HttpClientTestingModule,
  HttpTestingController
} from "@angular/common/http/testing"
import { PortfoliosService } from "../portfolios/portfolios.service"
import {
  PortfolioData,
  PortfolioStats,
  PortfolioSummary
} from "../portfolios/portfolios.interface"
import { ENDPOINTS } from "../../consts/endpoints"

describe("PortfoliosService", () => {
  let service: PortfoliosService
  let httpMock: HttpTestingController

  const mockPortfolioData: PortfolioData = {
    portfolio_id: 1,
    portfolio_name: "Test Portfolio",
    avatar: "avatar.jpg",
    total_value: "10000",
    value_change_24h: "100",
    percent_change_24h: "1"
  }

  const mockPortfolioSummary: PortfolioSummary = {
    total_value: "10000",
    total_value_change_24h: "100",
    total_value_change_24h_percentage: "1",
    holdings: []
  }

  const mockPortfolioStats: PortfolioStats = {
    total_value: "10000",
    total_value_change_24h: "100",
    total_value_change_24h_percentage: "1",
    all_time_profit: "500",
    cost_basis: "9500",
    best_performer: {
      symbol: "BTC",
      name: "Bitcoin",
      change_value: "50",
      change_percentage: "5"
    },
    worst_performer: {
      symbol: "ETH",
      name: "Ethereum",
      change_value: "-10",
      change_percentage: "-1"
    },
    holdings: []
  }

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [PortfoliosService]
    })

    service = TestBed.inject(PortfoliosService)
    httpMock = TestBed.inject(HttpTestingController)
  })

  afterEach(() => {
    httpMock.verify()
  })

  it("should be created", () => {
    expect(service).toBeTruthy()
  })

  describe("getAll", () => {
    it("should fetch all portfolios", () => {
      const mockResponse: PortfolioData[] = [mockPortfolioData]

      service.getAll().subscribe(response => {
        expect(response).toEqual(mockResponse)
      })

      const req = httpMock.expectOne(ENDPOINTS.portfolios.main)
      expect(req.request.method).toBe("GET")
      req.flush(mockResponse)
    })
  })

  describe("getSummary", () => {
    it("should fetch portfolio summary", () => {
      service.getSummary().subscribe(response => {
        expect(response).toEqual(mockPortfolioSummary)
      })

      const req = httpMock.expectOne(ENDPOINTS.portfolios.summary)
      expect(req.request.method).toBe("GET")
      req.flush(mockPortfolioSummary)
    })
  })

  describe("getById", () => {
    it("should fetch portfolio stats by id", () => {
      const portfolioId = "1"

      service.getById(portfolioId).subscribe(response => {
        expect(response).toEqual(mockPortfolioStats)
      })

      const req = httpMock.expectOne(
        ENDPOINTS.portfolios.byIdSummary(portfolioId)
      )
      expect(req.request.method).toBe("GET")
      req.flush(mockPortfolioStats)
    })
  })

  describe("create", () => {
    it("should create a new portfolio", () => {
      const formData = new FormData()
      formData.append("name", "New Portfolio")

      service.create(formData).subscribe(response => {
        expect(response).toBeTruthy()
      })

      const req = httpMock.expectOne(ENDPOINTS.portfolios.main)
      expect(req.request.method).toBe("POST")
      expect(req.request.body).toEqual(formData)
      req.flush({})
    })
  })

  describe("update", () => {
    it("should update a portfolio", () => {
      const formData = new FormData()
      formData.append("portfolio_id", "1")
      formData.append("portfolio_name", "Updated Portfolio")

      service.update(formData).subscribe(response => {
        expect(response).toBeTruthy()
      })

      const req = httpMock.expectOne(ENDPOINTS.portfolios.main)
      expect(req.request.method).toBe("PATCH")
      expect(req.request.body).toEqual(formData)
      req.flush({})
    })
  })

  describe("delete", () => {
    it("should delete a portfolio", () => {
      const portfolioId = "1"

      service.delete(portfolioId).subscribe(response => {
        expect(response).toBeTruthy()
      })

      const req = httpMock.expectOne(ENDPOINTS.portfolios.byId(portfolioId))
      expect(req.request.method).toBe("DELETE")
      req.flush({})
    })
  })
})
