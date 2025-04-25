import { ComponentFixture, TestBed } from "@angular/core/testing"
import { ErrorComponent } from "./error.component"
import { faTriangleExclamation } from "@fortawesome/free-solid-svg-icons"
import { Component, Input } from "@angular/core"

@Component({
  selector: "fa-icon",
  template: "<span></span>"
})
class MockFaIconComponent {
  @Input() icon: unknown
}

describe("ErrorComponent", () => {
  let component: ErrorComponent
  let fixture: ComponentFixture<ErrorComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ErrorComponent, MockFaIconComponent]
    }).compileComponents()

    fixture = TestBed.createComponent(ErrorComponent)
    component = fixture.componentInstance
  })

  it("should create", () => {
    expect(component).toBeTruthy()
  })

  it("should display the correct error message", () => {
    const testMessage = "Test error message"
    component.message = testMessage
    fixture.detectChanges()

    const errorElement = fixture.nativeElement.querySelector(".error")
    expect(errorElement.textContent).toContain(testMessage)
  })

  it("should have the correct icon", () => {
    expect(component.icon).toBe(faTriangleExclamation)
  })

  it("should pass the icon to fa-icon component", () => {
    component.message = "Test"
    fixture.detectChanges()

    const faIconComponent = fixture.debugElement.query(
      el => el.name === "fa-icon"
    ).componentInstance as MockFaIconComponent
    expect(faIconComponent.icon).toBe(faTriangleExclamation)
  })
})
