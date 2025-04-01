import {
  ComponentFixture,
  TestBed,
  fakeAsync,
  tick
} from "@angular/core/testing"
import { ConfirmComponent } from "./confirm.component"
import { ConfirmService } from "../../api/confirm/confirm.service"
import { provideRouter, Router } from "@angular/router"
import { FaIconComponent } from "@fortawesome/angular-fontawesome"
import { HttpClientTestingModule } from "@angular/common/http/testing"
import { of, throwError } from "rxjs"
import { HttpErrorResponse } from "@angular/common/http"
import { ROUTES } from "../../consts/routes"
import { authErrors } from "../../consts/errors/auth.errors"
import { routes } from "../../app.routes"

describe("ConfirmComponent", () => {
  let component: ConfirmComponent
  let fixture: ComponentFixture<ConfirmComponent>
  let confirmService: ConfirmService
  let router: Router

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, FaIconComponent, ConfirmComponent],
      providers: [provideRouter(routes)]
    }).compileComponents()

    fixture = TestBed.createComponent(ConfirmComponent)
    component = fixture.componentInstance
    confirmService = TestBed.inject(ConfirmService)
    router = TestBed.inject(Router)
  })

  it("should create", () => {
    fixture.detectChanges()
    expect(component).toBeTruthy()
  })

  describe("Initialization without token", () => {
    beforeEach(() => {
      ;(router as Router).navigate([ROUTES.confirm])
      fixture.detectChanges()
    })

    it("should set isToken to false when no token in URL", () => {
      expect(component.isToken()).toBeFalsy()
    })

    it("should not call confirmService when no token", () => {
      jest.spyOn(confirmService, "confirm")
      component.ngOnInit()
      expect(confirmService.confirm).not.toHaveBeenCalled()
    })
  })

  describe("Initialization with token", () => {
    const testToken = "test-token-123"

    beforeEach(() => {
      ;(router as Router).navigate([ROUTES.confirm + "/" + testToken])
    })

    it("should set isToken to true when token in URL", () => {
      fixture.detectChanges()
      expect(component.isToken()).toBeTruthy()
    })

    it("should call confirmService with token from URL", () => {
      jest.spyOn(confirmService, "confirm").mockReturnValue(of({}))
      fixture.detectChanges()
      expect(confirmService.confirm).toHaveBeenCalledWith({ token: testToken })
    })

    it("should navigate to home on successful confirmation", fakeAsync(() => {
      jest.spyOn(confirmService, "confirm").mockReturnValue(of({}))
      fixture.detectChanges()
      tick()
      expect(router.navigate).toHaveBeenCalledWith([ROUTES.home])
    }))

    it("should set error message on 404 error", fakeAsync(() => {
      const error = new HttpErrorResponse({ status: 404 })
      jest.spyOn(confirmService, "confirm").mockReturnValue(throwError(() => error))
      fixture.detectChanges()
      tick()
      expect(component.message()).toBe(authErrors.token)
      expect(component.error()).toBeFalsy() // Only message changes for 404
    }))

    it("should set error flag on other errors", fakeAsync(() => {
      const error = new HttpErrorResponse({ status: 500 })
      jest.spyOn(confirmService, "confirm").mockReturnValue(throwError(() => error))
      fixture.detectChanges()
      tick()
      expect(component.error()).toBeTruthy()
      expect(component.message()).toBe(authErrors.common)
    }))
  })

  describe("Template", () => {
    it("should show waiting message when token exists", fakeAsync(() => {
      ;(router as Router).navigate([ROUTES.confirm + "/" + "test-token"])
      tick()
      fixture.detectChanges()
      const title = fixture.nativeElement.querySelector(".confirm__title")
      expect(title.textContent).toContain("Waiting for confirmation")
    }))

    it("should show confirm registration message when no token", fakeAsync(() => {
      ;(router as Router).navigate([ROUTES.confirm])
      tick()
      fixture.detectChanges()
      const title = fixture.nativeElement.querySelector(".confirm__title")
      const text = fixture.nativeElement.querySelector(".confirm__text")
      expect(title.textContent).toContain("Confirm registration")
      expect(text.textContent).toContain("Check your email")
    }))

    it("should show error message when error occurs", () => {
      component.error.set(true)
      fixture.detectChanges()
      const errorElement =
        fixture.nativeElement.querySelector(".confirm__error")
      expect(errorElement).toBeTruthy()
    })

    it("should show registration link when error occurs", () => {
      component.error.set(true)
      fixture.detectChanges()
      const link = fixture.nativeElement.querySelector(".confirm__link")
      expect(link.textContent).toContain("Try to register again")
      expect(link.getAttribute("href")).toBe("/register")
    })
  })
})
