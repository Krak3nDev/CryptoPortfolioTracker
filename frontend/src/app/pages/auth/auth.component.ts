import { Component, inject, signal } from "@angular/core"
import { Router, RouterLink } from "@angular/router"
import { FormControl, FormGroup, ReactiveFormsModule } from "@angular/forms"
import { FontAwesomeModule } from "@fortawesome/angular-fontawesome"
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons"
import { AuthService } from "../../api/auth/auth.service"
import { ROUTES } from "../../consts/routes"
import {
  LoginBodyRequest,
  RegisterBodyRequest
} from "../../api/auth/auth.interface"
import { authFormValidators } from "./form.validators"
import { AuthErrorComponent } from "./error/auth-error.component"
import { HttpErrorResponse } from "@angular/common/http"

@Component({
  selector: "app-auth",
  imports: [
    ReactiveFormsModule,
    RouterLink,
    FontAwesomeModule,
    AuthErrorComponent
  ],
  templateUrl: "./auth.component.html",
  styleUrl: "./auth.component.scss"
})
export class AuthComponent {
  router = inject(Router)
  authService = inject(AuthService)

  isRegister = signal(false)

  validators = authFormValidators(this.isRegister)
  authForm = new FormGroup(
    {
      username: new FormControl<string>("", this.validators.username),
      email: new FormControl<string>("", this.validators.email),
      password: new FormControl<string>("", this.validators.password),
      confirmPassword: new FormControl<string>(
        "",
        this.validators.confirmPassword
      )
    },
    this.validators.passwordMatch
  )
  isPasswordVisible = signal({
    password: false,
    confirmPassword: false
  })
  icons = {
    eye: faEye,
    eyeSlash: faEyeSlash
  }
  submitError = signal<object | null>(null)

  ngOnInit() {
    if (this.router.url.includes(ROUTES.register)) {
      this.isRegister.set(true)
    }
  }

  onSubmit() {
    if (this.authForm.invalid) {
      return
    }

    if (this.isRegister()) {
      const payload: RegisterBodyRequest = {
        username: this.authForm.value.username!,
        password: this.authForm.value.password!,
        email: this.authForm.value.email!
      }

      this.authService
        .register(payload)
        .subscribe(
          this.submitResponseHandlers.success,
          this.submitResponseHandlers.error
        )
    } else {
      const payload: LoginBodyRequest = {
        username: this.authForm.value.username!,
        password: this.authForm.value.password!
      }

      this.authService
        .login(payload)
        .subscribe(
          this.submitResponseHandlers.success,
          this.submitResponseHandlers.error
        )
    }
  }

  submitResponseHandlers = {
    success: (_res: object) => {
      this.router.navigate(this.isRegister() ? [ROUTES.confirm] : [ROUTES.home])
    },
    error: (error: HttpErrorResponse) => {
      if (error.status === 404) {
        this.submitError.set({
          submitInvalid: true
        })
        return
      }

      this.submitError.set({
        common: true
      })
    }
  }

  showPassword(field: "password" | "confirmPassword") {
    const oldState = this.isPasswordVisible()

    this.isPasswordVisible.set({
      ...oldState,
      [field]: !oldState[field]
    })
  }
}
