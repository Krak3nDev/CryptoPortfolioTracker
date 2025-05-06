import { Component, inject, OnInit, signal } from '@angular/core'
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
import { authFormValidators } from "./authForm.validators"
import { ErrorComponent } from "../../components/error/error.component"
import { HttpErrorResponse } from "@angular/common/http"
import { invalid } from "../../utils/error/invalid"
import { message } from "../../utils/error/message"
import { authErrors } from "../../consts/errors/auth.errors"
import { commonErrors } from "../../consts/errors/common.errors"

@Component({
  selector: "app-auth",
  imports: [ReactiveFormsModule, RouterLink, FontAwesomeModule, ErrorComponent],
  templateUrl: "./auth.component.html",
  styleUrl: "./auth.component.scss"
})
export class AuthComponent implements OnInit {
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
  submitError = signal<string | null>(null)

  ngOnInit() {
    if (this.router.url.includes(ROUTES.register)) {
      this.isRegister.set(true)
    }
  }

  onSubmit() {
    if (this.authForm.invalid) {
      this.authForm.markAsTouched()
      this.authForm.controls.username.markAsTouched()
      this.authForm.controls.email.markAsTouched()
      this.authForm.controls.password.markAsTouched()
      this.authForm.controls.confirmPassword.markAsTouched()
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
        this.submitError.set(authErrors.submitInvalid)
        return
      }

      this.submitError.set(commonErrors.main)
    }
  }

  showPassword(field: "password" | "confirmPassword") {
    const oldState = this.isPasswordVisible()

    this.isPasswordVisible.set({
      ...oldState,
      [field]: !oldState[field]
    })
  }

  protected readonly invalid = invalid
  protected readonly message = message
  protected readonly authErrors = authErrors
  protected readonly ROUTES = ROUTES
}
