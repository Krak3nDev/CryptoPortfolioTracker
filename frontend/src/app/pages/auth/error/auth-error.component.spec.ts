import { ComponentFixture, TestBed } from "@angular/core/testing"
import { AuthErrorComponent } from "./auth-error.component"
import { FaIconComponent } from "@fortawesome/angular-fontawesome"
import { ValidationErrors } from "@angular/forms"
import { ComponentRef } from "@angular/core"
import { authErrors } from "../../../consts/errors/auth.errors"

describe("AuthErrorComponent", () => {
  let component: AuthErrorComponent
  let componentRef: ComponentRef<AuthErrorComponent>
  let fixture: ComponentFixture<AuthErrorComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FaIconComponent, AuthErrorComponent]
    }).compileComponents()

    fixture = TestBed.createComponent(AuthErrorComponent)
    component = fixture.componentInstance
    componentRef = fixture.componentRef
    fixture.detectChanges()
  })

  it("should create", () => {
    expect(component).toBeTruthy()
  })

  it("should not show error when no input", () => {
    expect(component.isError()).toBeFalsy()
    expect(component.message()).toBe("")
  })

  it("should show error message when input is provided (required)", () => {
    const error: ValidationErrors = { required: true }
    componentRef.setInput("error", error)
    fixture.detectChanges()

    expect(component.isError()).toBeTruthy()
    expect(component.message()).toBe(authErrors.required)
  })

  it("should show error message when input is provided (email)", () => {
    const error: ValidationErrors = { email: true }
    componentRef.setInput("error", error)
    fixture.detectChanges()

    expect(component.isError()).toBeTruthy()
    expect(component.message()).toBe(authErrors.email)
  })

  it("should show error message when input is provided (mismatch)", () => {
    const error: ValidationErrors = { mismatch: true }
    componentRef.setInput("error", error)
    fixture.detectChanges()

    expect(component.isError()).toBeTruthy()
    expect(component.message()).toBe(authErrors.mismatch)
  })

  it("should not show error for unknown error types", () => {
    const error: ValidationErrors = { unknownError: true }
    componentRef.setInput("error", error)
    fixture.detectChanges()

    expect(component.isError()).toBeFalsy()
    expect(component.message()).toBe("")
  })
})
