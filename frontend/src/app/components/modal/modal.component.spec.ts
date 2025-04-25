import { ComponentFixture, TestBed } from "@angular/core/testing"
import { ModalComponent } from "./modal.component"
import { ModalAdapter } from "./state/modal.adapter"
import { Store } from "@ngrx/store"
import { of } from "rxjs"
import { MockStore, provideMockStore } from "@ngrx/store/testing"
import { selectModals } from "./state/modal.selectors"

describe("ModalComponent", () => {
  let component: ModalComponent
  let fixture: ComponentFixture<ModalComponent>
  let modalAdapter: ModalAdapter

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalComponent],
      providers: [
        {
          provide: ModalAdapter,
          useValue: {
            select: jest.fn(() => of({})),
            close: jest.fn(),
            open: jest.fn()
          }
        },
        provideMockStore()
      ]
    }).compileComponents()

    fixture = TestBed.createComponent(ModalComponent)
    component = fixture.componentInstance
    modalAdapter = TestBed.inject(ModalAdapter)

    jest
      .spyOn(modalAdapter, "select")
      .mockReturnValue(of({ "test-modal": { isOpen: false } }))

    component.modalId = "test-modal"
    fixture.detectChanges()
  })

  it("should create", () => {
    expect(component).toBeTruthy()
  })

  it("should initialize with default options", () => {
    expect(component.options.closeOutside).toBeUndefined()
  })

  it("should not close when clicking inside modal", () => {
    component.options.closeOutside = true
    modalAdapter.open("test-modal")

    const mockElement = {
      id: "modal",
      parentElement: { id: "modal-target-test-modal" }
    } as unknown as HTMLElement

    component.onClickOutside(mockElement)
    expect(modalAdapter.close).not.toHaveBeenCalled()
  })

  it("should close when clicking outside if closeOutside is true", () => {
    component.options.closeOutside = true
    component.isOpen.set(true)

    const mockElement = {
      id: "other-element",
      parentElement: null
    } as unknown as HTMLElement

    component.onClickOutside(mockElement)
    expect(modalAdapter.close).toHaveBeenCalledWith("test-modal")
  })

  it("should not close when clicking outside if closeOutside is false", () => {
    component.options.closeOutside = false
    component.isOpen.set(true)

    const mockEvent = {
      id: "other-element",
      parentElement: null
    } as unknown as HTMLElement

    component.onClickOutside(mockEvent)
    expect(modalAdapter.close).not.toHaveBeenCalled()
  })

  it("should not close when modal is not open", () => {
    component.options.closeOutside = true
    component.isOpen.set(false)

    const mockEvent = {
      id: "other-element",
      parentElement: null
    } as unknown as HTMLElement

    component.onClickOutside(mockEvent)
    expect(modalAdapter.close).not.toHaveBeenCalled()
  })

  it("should render with active class when open", () => {
    component.isOpen.set(true)
    fixture.detectChanges()

    const modalElement = fixture.nativeElement.querySelector(".modal")
    expect(modalElement.classList).toContain("modal_active")
  })

  it("should render without active class when closed", () => {
    component.isOpen.set(false)
    fixture.detectChanges()

    const modalElement = fixture.nativeElement.querySelector(".modal")
    expect(modalElement.classList).not.toContain("modal_active")
  })
})

describe("ModalAdapter", () => {
  let adapter: ModalAdapter
  let store: MockStore

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ModalAdapter, provideMockStore()]
    })

    adapter = TestBed.inject(ModalAdapter)
    store = TestBed.inject(Store) as MockStore
    jest.spyOn(store, "dispatch")
  })

  it("should dispatch openModal action", () => {
    adapter.open("test-modal")
    expect(store.dispatch).toHaveBeenCalledWith(
      expect.objectContaining({
        modalId: "test-modal",
        type: "[Modal] Open Modal"
      })
    )
  })

  it("should dispatch closeModal action", () => {
    adapter.close("test-modal")
    expect(store.dispatch).toHaveBeenCalledWith(
      expect.objectContaining({
        modalId: "test-modal",
        type: "[Modal] Close Modal"
      })
    )
  })

  it("should select modals state", () => {
    const mockState = { "test-modal": { isOpen: true } }
    store.overrideSelector(selectModals, mockState)

    adapter.select().subscribe(state => {
      expect(state).toEqual(mockState)
    })
  })
})
