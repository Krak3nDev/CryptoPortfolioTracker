import {
  ComponentFixture,
  fakeAsync,
  TestBed,
  tick
} from "@angular/core/testing"
import { PortfoliosListComponent } from "./portfoliosList.component"
import { PortfoliosService } from "../../api/portfolios/portfolios.service"
import { PortfoliosListAdapter } from "./state/portfoliosList.adapter"
import { ModalAdapter } from "../../components/modal/state/modal.adapter"
import { ReactiveFormsModule } from "@angular/forms"
import { MockStore, provideMockStore } from "@ngrx/store/testing"
import { of, throwError } from "rxjs"
import {
  CreatePortfolioRequest,
  CreatePortfolioResponse,
  PortfolioData
} from "../../api/portfolios/portfolios.interface"
import { HttpClientTestingModule } from "@angular/common/http/testing"

describe("PortfoliosListComponent", () => {
  let component: PortfoliosListComponent
  let fixture: ComponentFixture<PortfoliosListComponent>
  let portfoliosService: jest.Mocked<PortfoliosService>
  let portfoliosListAdapter: jest.Mocked<PortfoliosListAdapter>
  let modalAdapter: jest.Mocked<ModalAdapter>

  const mockPortfolioData: PortfolioData = {
    portfolio_id: 1,
    portfolio_name: "Test Portfolio",
    avatar: "test-avatar.png",
    total_value: "10000",
    value_change_24h: "100",
    percent_change_24h: "1.0"
  }

  beforeEach(async () => {
    portfoliosService = {
      getAll: jest.fn(),
      create: jest.fn(),
      delete: jest.fn()
    } as unknown as jest.Mocked<PortfoliosService>

    portfoliosListAdapter = {
      select: jest.fn(() =>
        of({
          list: { isLoading: false, error: null, result: [mockPortfolioData] },
          newPortfolio: { isLoading: false, error: null }
        })
      ),
      updateList: jest.fn(),
      createNewPortfolio: jest.fn()
    } as unknown as jest.Mocked<PortfoliosListAdapter>

    modalAdapter = {
      open: jest.fn(),
      close: jest.fn(),
      select: jest.fn(() => of({}))
    } as unknown as jest.Mocked<ModalAdapter>

    await TestBed.configureTestingModule({
      imports: [
        PortfoliosListComponent,
        ReactiveFormsModule,
        HttpClientTestingModule
      ],
      providers: [
        { provide: PortfoliosService, useValue: portfoliosService },
        { provide: PortfoliosListAdapter, useValue: portfoliosListAdapter },
        { provide: ModalAdapter, useValue: modalAdapter },
        provideMockStore()
      ]
    }).compileComponents()

    fixture = TestBed.createComponent(PortfoliosListComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it("should create", () => {
    expect(component).toBeTruthy()
  })

  it("should initialize form with validators", () => {
    expect(component.createPortfolioForm).toBeDefined()
    expect(component.createPortfolioForm.controls.name.validator).toBeTruthy()
    expect(component.createPortfolioForm.controls.avatar.validator).toBeTruthy()
  })

  it("should call updateList on init", () => {
    expect(portfoliosListAdapter.updateList).toHaveBeenCalled()
  })

  it("should handle file upload", () => {
    const mockFile = new File([""], "test.png", { type: "image/png" })
    const mockEvent = {
      target: {
        files: [mockFile]
      }
    } as unknown as Event

    component.uploadFile(mockEvent)
    expect(component.createPortfolioForm.controls.avatar.value).toBe(mockFile)
  })

  it("should validate form before submission", () => {
    component.createPortfolioForm.controls.name.setValue("")
    component.createPortfolio()

    expect(component.createPortfolioForm.touched).toBe(true)
    expect(portfoliosListAdapter.createNewPortfolio).not.toHaveBeenCalled()
  })

  it("should call createNewPortfolio with valid form", () => {
    const mockFile = new File([""], "test.png", { type: "image/png" })
    component.createPortfolioForm.controls.name.setValue("Test Portfolio")
    component.createPortfolioForm.controls.avatar.setValue(mockFile)

    component.createPortfolio()
    expect(portfoliosListAdapter.createNewPortfolio).toHaveBeenCalled()
  })

  it("should delete portfolio", fakeAsync(() => {
    portfoliosService.delete.mockReturnValue(of({}))

    const portfolioId = "1"
    component.deletePortfolio(portfolioId)
    tick()

    expect(portfoliosService.delete).toHaveBeenCalledWith(portfolioId)
    expect(modalAdapter.close).toHaveBeenCalledWith(portfolioId)
    expect(portfoliosListAdapter.updateList).toHaveBeenCalled()
  }))

  it("should display portfolio list", () => {
    const rows = fixture.nativeElement.querySelectorAll(
      ".table-portfolios__row"
    )
    expect(rows.length).toBe(1)
    expect(rows[0].textContent).toContain("Test Portfolio")
  })
})

describe("PortfoliosListAdapter", () => {
  let adapter: PortfoliosListAdapter
  let portfoliosService: jest.Mocked<PortfoliosService>
  let store: MockStore

  const mockPortfolioData: PortfolioData = {
    portfolio_id: 1,
    portfolio_name: "Test Portfolio",
    avatar: "test-avatar.png",
    total_value: "10000",
    value_change_24h: "100",
    percent_change_24h: "1.0"
  }

  beforeEach(() => {
    portfoliosService = {
      getAll: jest.fn(),
      create: jest.fn()
    } as unknown as jest.Mocked<PortfoliosService>

    TestBed.configureTestingModule({
      providers: [
        PortfoliosListAdapter,
        { provide: PortfoliosService, useValue: portfoliosService },
        provideMockStore()
      ]
    })

    adapter = TestBed.inject(PortfoliosListAdapter)
    store = TestBed.inject(MockStore)
    jest.spyOn(store, "dispatch")
  })

  it("should dispatch actions for successful list update", fakeAsync(() => {
    const mockData: PortfolioData[] = [
      {
        portfolio_id: 1,
        portfolio_name: "Test",
        avatar: "test.png",
        total_value: "1000",
        value_change_24h: "10",
        percent_change_24h: "1.0"
      }
    ]

    portfoliosService.getAll.mockReturnValue(of(mockData))

    adapter.updateList()
    tick()

    expect(store.dispatch).toHaveBeenCalledWith(
      expect.objectContaining({ type: "[Portfolios List] Update List" })
    )
    expect(store.dispatch).toHaveBeenCalledWith(
      expect.objectContaining({ type: "[Portfolios List] Update List Success" })
    )
  }))

  it("should dispatch actions for failed list update", fakeAsync(() => {
    portfoliosService.getAll.mockReturnValue(
      throwError(() => new Error("Test error"))
    )

    adapter.updateList()
    tick()

    expect(store.dispatch).toHaveBeenCalledWith(
      expect.objectContaining({ type: "[Portfolios List] Update List Failure" })
    )
  }))

  it("should dispatch actions for successful portfolio creation", fakeAsync(() => {
    const mockCreateRequest: CreatePortfolioRequest = {
      name: "name",
      avatar: "http://api/test.png"
    }
    const mockCreateResponse: CreatePortfolioResponse = {
      portfolio_id: "1",
      name: "name",
      avatar: "http://api/test.png"
    }
    portfoliosService.create.mockReturnValue(of(mockCreateResponse))

    adapter.createNewPortfolio(mockCreateRequest)
    tick()

    expect(store.dispatch).toHaveBeenCalledWith(
      expect.objectContaining({ type: "[Portfolios List] Create Portfolio" })
    )
    expect(store.dispatch).toHaveBeenCalledWith(
      expect.objectContaining({
        type: "[Portfolios List] Create Portfolio Success"
      })
    )
  }))

  it("should map portfolio data with growth type", () => {
    const data: PortfolioData[] = [
      {
        ...mockPortfolioData,
        value_change_24h: "100"
      }
    ]

    const result = adapter["mapPortfoliosDataWithType"](data)
    expect(result[0].type).toBeDefined()
  })
})
