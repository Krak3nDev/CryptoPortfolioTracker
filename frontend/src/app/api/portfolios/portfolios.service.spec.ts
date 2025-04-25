import { TestBed } from "@angular/core/testing"
import { PortfoliosService } from "./portfolios.service"
import { HttpClient } from "@angular/common/http"
import { ENDPOINTS } from "../../consts/endpoints"
import {
  Asset,
  AssetWithProfitLoss,
  CreatePortfolioRequest,
  CreatePortfolioResponse,
  PerformerData,
  PortfolioData,
  PortfolioStats,
  PortfolioSummary,
  UpdatePortfolioRequest
} from "./portfolios.interface"
import { of } from "rxjs"

describe("PortfoliosService", () => {
  let service: PortfoliosService
  let httpClientMock: jest.Mocked<HttpClient>

  const mockAsset: Asset = {
    asset_id: 1,
    asset_symbol: "BTC",
    total_quantity: "0.5",
    current_price: "50000",
    change_1h: "0.5",
    change_24h: "2.5",
    change_7d: "5.0",
    total_value: "25000",
    allocation_percentage: "50"
  }

  const mockAssetWithProfit: AssetWithProfitLoss = {
    ...mockAsset,
    asset_name: "Bitcoin",
    average_buy_price: "40000",
    profit_loss_usd: "5000",
    profit_loss_percentage: "25"
  }

  const mockPerformer: PerformerData = {
    symbol: "ETH",
    name: "Ethereum",
    change_value: "200",
    change_percentage: "5.0"
  }

  const mockPortfolioData: PortfolioData = {
    portfolio_id: 1,
    portfolio_name: "My Portfolio",
    avatar: "avatar-url",
    total_value: "50000",
    value_change_24h: "1000",
    percent_change_24h: "2.0"
  }

  const mockPortfolioSummary: PortfolioSummary = {
    total_value: "100000",
    total_value_change_24h: "2000",
    total_value_change_24h_percentage: "2.0",
    holdings: [mockAsset]
  }

  const mockPortfolioStats: PortfolioStats = {
    total_value: "50000",
    total_value_change_24h: "1000",
    total_value_change_24h_percentage: "2.0",
    all_time_profit: "5000",
    cost_basis: "45000",
    best_performer: mockPerformer,
    worst_performer: {
      ...mockPerformer,
      change_value: "-100",
      change_percentage: "-2.0"
    },
    holdings: [mockAssetWithProfit]
  }

  const mockCreateResponse: CreatePortfolioResponse = {
    portfolio_id: "1",
    name: "New Portfolio",
    avatar: "new-avatar-url"
  }

  beforeEach(() => {
    httpClientMock = {
      post: jest.fn(),
      patch: jest.fn(),
      delete: jest.fn(),
      get: jest.fn()
    } as unknown as jest.Mocked<HttpClient>

    TestBed.configureTestingModule({
      providers: [
        PortfoliosService,
        { provide: HttpClient, useValue: httpClientMock }
      ]
    })

    service = TestBed.inject(PortfoliosService)
  })

  it("should be created", () => {
    expect(service).toBeTruthy()
  })

  describe("create", () => {
    it("should call POST with correct endpoint and return response", () => {
      const payload: CreatePortfolioRequest = { name: "New Portfolio" }
      httpClientMock.post.mockReturnValue(of(mockCreateResponse))

      service.create(payload).subscribe(response => {
        expect(response).toEqual(mockCreateResponse)
        expect(response.portfolio_id).toBeDefined()
      })

      expect(httpClientMock.post).toHaveBeenCalledWith(
        ENDPOINTS.portfolios.main,
        payload
      )
    })

    it("should handle optional avatar field", () => {
      const payload: CreatePortfolioRequest = {
        name: "New Portfolio",
        avatar: "custom-avatar.png"
      }
      httpClientMock.post.mockReturnValue(of(mockCreateResponse))

      service.create(payload).subscribe()

      expect(httpClientMock.post).toHaveBeenCalledWith(
        ENDPOINTS.portfolios.main,
        payload
      )
    })
  })

  describe("update", () => {
    it("should call PATCH with correct endpoint and payload", () => {
      const payload: UpdatePortfolioRequest = {
        portfolio_id: "1",
        name: "Updated Name"
      }
      httpClientMock.patch.mockReturnValue(of({}))

      service.update(payload).subscribe()

      expect(httpClientMock.patch).toHaveBeenCalledWith(
        ENDPOINTS.portfolios.main,
        payload
      )
    })

    it("should handle partial updates", () => {
      const payload: UpdatePortfolioRequest = {
        portfolio_id: "1",
        avatar: "new-avatar.png"
      }
      httpClientMock.patch.mockReturnValue(of({}))

      service.update(payload).subscribe()

      expect(httpClientMock.patch).toHaveBeenCalledWith(
        ENDPOINTS.portfolios.main,
        payload
      )
    })
  })

  describe("delete", () => {
    it("should call DELETE with correct endpoint", () => {
      const portfolioId = "1"
      httpClientMock.delete.mockReturnValue(of({}))

      service.delete(portfolioId).subscribe()

      expect(httpClientMock.delete).toHaveBeenCalledWith(
        ENDPOINTS.portfolios.byId(portfolioId)
      )
    })
  })

  describe("getAll", () => {
    it("should call GET and return array of portfolios", () => {
      const mockResponse: PortfolioData[] = [mockPortfolioData]
      httpClientMock.get.mockReturnValue(of(mockResponse))

      service.getAll().subscribe(response => {
        expect(response).toBeInstanceOf(Array)
        expect(response[0].portfolio_id).toBeDefined()
      })

      expect(httpClientMock.get).toHaveBeenCalledWith(ENDPOINTS.portfolios.main)
    })
  })

  describe("summary", () => {
    it("should call GET and return summary with holdings", () => {
      httpClientMock.get.mockReturnValue(of(mockPortfolioSummary))

      service.summary().subscribe(response => {
        expect(response.total_value).toBeDefined()
        expect(response.holdings).toBeInstanceOf(Array)
      })

      expect(httpClientMock.get).toHaveBeenCalledWith(
        ENDPOINTS.portfolios.summary
      )
    })
  })

  describe("getById", () => {
    it("should call GET with ID and return detailed stats", () => {
      const portfolioId = "1"
      httpClientMock.get.mockReturnValue(of(mockPortfolioStats))

      service.getById(portfolioId).subscribe(response => {
        expect(response.holdings).toBeInstanceOf(Array)
        expect(response.best_performer).toBeDefined()
        expect(response.worst_performer).toBeDefined()
      })

      expect(httpClientMock.get).toHaveBeenCalledWith(
        ENDPOINTS.portfolios.byIdSummary(portfolioId)
      )
    })

    it("should handle optional fields in response", () => {
      const portfolioId = "1"
      const minimalResponse: PortfolioStats = {
        holdings: [mockAssetWithProfit]
      }
      httpClientMock.get.mockReturnValue(of(minimalResponse))

      service.getById(portfolioId).subscribe(response => {
        expect(response.holdings.length).toBe(1)
        expect(response.best_performer).toBeUndefined()
      })
    })
  })
})
