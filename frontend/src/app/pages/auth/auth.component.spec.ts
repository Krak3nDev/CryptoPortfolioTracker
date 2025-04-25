import {
  ComponentFixture,
  fakeAsync,
  TestBed,
  tick
} from "@angular/core/testing"
import { AuthComponent } from "./auth.component"
import { AuthService } from "../../api/auth/auth.service"
import { provideRouter, Router } from "@angular/router"
import { ReactiveFormsModule } from "@angular/forms"
import { HttpClientTestingModule } from "@angular/common/http/testing"
import { FontAwesomeModule } from "@fortawesome/angular-fontawesome"
import { ErrorComponent } from "../../components/error/error.component"
import { of, throwError } from "rxjs"
import { ROUTES } from "../../consts/routes"
import { HttpErrorResponse } from "@angular/common/http"
import { RouterTestingModule } from "@angular/router/testing"
import { routes } from "../../app.routes"

describe("AuthComponent", () => {
  let component: AuthComponent
  let fixture: ComponentFixture<AuthComponent>
  let authService: AuthService
  let router: Router

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        ReactiveFormsModule,
        HttpClientTestingModule,
        FontAwesomeModule,
        RouterTestingModule.withRoutes([]),
        AuthComponent,
        ErrorComponent
      ],
      providers: [provideRouter(routes)]
    }).compileComponents()

    fixture = TestBed.createComponent(AuthComponent)
    component = fixture.componentInstance
    authService = TestBed.inject(AuthService)
    router = TestBed.inject(Router)
    fixture.detectChanges()
  })

  it("should create", () => {
    expect(component).toBeTruthy()
  })

  describe("Initialization", () => {
    it("should initialize form with empty values", () => {
      expect(component.authForm.value).toEqual({
        username: "",
        email: "",
        password: "",
        confirmPassword: ""
      })
    })

    it("should set isRegister to true when URL contains register", fakeAsync(() => {
      ;(router as Router).navigate([ROUTES.register])
      tick()
      component.ngOnInit()
      expect(component.isRegister()).toBeTruthy()
    }))

    it("should set isRegister to false when URL contains login", fakeAsync(() => {
      ;(router as Router).navigate([ROUTES.login])
      tick()
      component.ngOnInit()
      expect(component.isRegister()).toBeFalsy()
    }))
  })

  describe("Form Validation", () => {
    it("should mark username as invalid when empty", () => {
      const username = component.authForm.controls["username"]
      username.setValue("")
      expect(username.valid).toBeFalsy()
    })

    it("should mark username as valid when not empty", () => {
      const username = component.authForm.controls["username"]
      username.setValue("testuser")
      expect(username.valid).toBeTruthy()
    })

    it("should mark email as invalid when empty in register mode", () => {
      component.isRegister.set(true)
      const email = component.authForm.controls["email"]
      email.setValue("")
      expect(email.valid).toBeFalsy()
    })

    it("should mark email as valid when proper format in register mode", () => {
      component.isRegister.set(true)
      const email = component.authForm.controls["email"]
      email.setValue("test@example.com")
      expect(email.valid).toBeTruthy()
    })

    it("should mark password as invalid when too short", () => {
      const password = component.authForm.controls["password"]
      password.setValue("123")
      expect(password.valid).toBeTruthy()
    })

    it("should mark password as valid when meets requirements", () => {
      const password = component.authForm.controls["password"]
      password.setValue("ValidPass123")
      expect(password.valid).toBeTruthy()
    })

    it("should validate password match in register mode", () => {
      component.isRegister.set(true)
      const password = component.authForm.controls["password"]
      const confirmPassword = component.authForm.controls["confirmPassword"]

      password.setValue("ValidPass123")
      confirmPassword.setValue("DifferentPass123")

      expect(component.authForm.hasError("mismatch")).toBeTruthy()

      confirmPassword.setValue("ValidPass123")
      expect(component.authForm.hasError("mismatch")).toBeFalsy()
    })
  })

  describe("Password Visibility", () => {
    it("should toggle password visibility", () => {
      expect(component.isPasswordVisible().password).toBeFalsy()
      component.showPassword("password")
      expect(component.isPasswordVisible().password).toBeTruthy()
      component.showPassword("password")
      expect(component.isPasswordVisible().password).toBeFalsy()
    })

    it("should toggle confirmPassword visibility", () => {
      expect(component.isPasswordVisible().confirmPassword).toBeFalsy()
      component.showPassword("confirmPassword")
      expect(component.isPasswordVisible().confirmPassword).toBeTruthy()
      component.showPassword("confirmPassword")
      expect(component.isPasswordVisible().confirmPassword).toBeFalsy()
    })
  })

  describe("Form Submission", () => {
    it("should not call authService when form is invalid", () => {
      jest.spyOn(authService, "login")
      component.onSubmit()
      expect(authService.login).not.toHaveBeenCalled()
    })

    describe("Login", () => {
      beforeEach(() => {
        component.authForm.controls["username"].setValue("testuser")
        component.authForm.controls["password"].setValue("ValidPass123")
      })

      it("should call login when form is valid and isRegister is false", () => {
        jest.spyOn(authService, "login").mockReturnValue(of({}))
        component.onSubmit()
        expect(authService.login).toHaveBeenCalledWith({
          username: "testuser",
          password: "ValidPass123"
        })
      })

      it("should navigate to home on successful login", fakeAsync(() => {
        jest.spyOn(authService, "login").mockReturnValue(of({}))
        component.onSubmit()
        tick()
        expect(router.navigate).toHaveBeenCalledWith([ROUTES.home])
      }))

      it("should set submitError on 404 error", fakeAsync(() => {
        const error = new HttpErrorResponse({ status: 404 })
        jest
          .spyOn(authService, "login")
          .mockReturnValue(throwError(() => error))
        component.onSubmit()
        tick()
        expect(component.submitError()).toEqual({ submitInvalid: true })
      }))

      it("should set common error on other errors", fakeAsync(() => {
        const error = new HttpErrorResponse({ status: 500 })
        jest
          .spyOn(authService, "login")
          .mockReturnValue(throwError(() => error))
        component.onSubmit()
        tick()
        expect(component.submitError()).toEqual({ common: true })
      }))
    })

    describe("Register", () => {
      beforeEach(() => {
        component.isRegister.set(true)
        component.authForm.controls["username"].setValue("testuser")
        component.authForm.controls["email"].setValue("test@example.com")
        component.authForm.controls["password"].setValue("ValidPass123")
        component.authForm.controls["confirmPassword"].setValue("ValidPass123")
      })

      it("should call register when form is valid and isRegister is true", () => {
        jest.spyOn(authService, "register").mockReturnValue(of({}))
        component.onSubmit()
        expect(authService.register).toHaveBeenCalledWith({
          username: "testuser",
          email: "test@example.com",
          password: "ValidPass123"
        })
      })

      it("should navigate to confirm on successful registration", fakeAsync(() => {
        jest.spyOn(authService, "register").mockReturnValue(of({}))
        component.onSubmit()
        tick()
        expect(router.navigate).toHaveBeenCalledWith([ROUTES.confirm])
      }))

      it("should set submitError on 404 error", fakeAsync(() => {
        const error = new HttpErrorResponse({ status: 404 })
        jest
          .spyOn(authService, "register")
          .mockReturnValue(throwError(() => error))
        component.onSubmit()
        tick()
        expect(component.submitError()).toEqual({ submitInvalid: true })
      }))

      it("should set common error on other errors", fakeAsync(() => {
        const error = new HttpErrorResponse({ status: 500 })
        jest
          .spyOn(authService, "register")
          .mockReturnValue(throwError(() => error))
        component.onSubmit()
        tick()
        expect(component.submitError()).toEqual({ common: true })
      }))
    })
  })
})
