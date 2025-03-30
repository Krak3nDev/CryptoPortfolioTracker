import { Component, inject, signal } from "@angular/core"
import { Router, RouterLink } from "@angular/router"
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from "@angular/forms"
import { FontAwesomeModule } from "@fortawesome/angular-fontawesome"
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons"
import { AuthService } from "../../api/auth/auth.service"
import { ROUTES } from "../../consts/routes"
import {
  LoginBodyRequest,
  RegisterBodyRequest
} from "../../api/auth/auth.interface"

@Component({
  selector: "app-auth",
  imports: [ReactiveFormsModule, RouterLink, FontAwesomeModule],
  templateUrl: "./auth.component.html",
  styleUrl: "./auth.component.scss"
})
export class AuthComponent {
  router = inject(Router)
  authService = inject(AuthService)

  isRegister = false
  authForm = new FormGroup({
    username: new FormControl<string>("", [Validators.required]),
    email: new FormControl<string>("", [Validators.required, Validators.email]),
    password: new FormControl<string>("", [Validators.required]),
    confirmPassword: new FormControl<string>("", [Validators.required])
  })
  isPasswordVisible = signal({
    password: false,
    confirmPassword: false
  })
  icons = {
    eye: faEye,
    eyeSlash: faEyeSlash
  }

  ngOnInit() {
    if (this.router.url.includes(ROUTES.register)) {
      this.isRegister = true
    }
  }

  onSubmit() {
    if (this.authForm.invalid || !this.passwordMatch()) {
      return
    }

    if (this.isRegister) {
      const payload: RegisterBodyRequest = {
        username: this.authForm.value.username!,
        password: this.authForm.value.password!,
        email: this.authForm.value.email!
      }

      this.authService.register(payload).subscribe(() => {
        this.router.navigate([ROUTES.confirm])
      })
    } else {
      const payload: LoginBodyRequest = {
        username: this.authForm.value.username!,
        password: this.authForm.value.password!
      }

      this.authService.login(payload).subscribe(() => {
        this.router.navigate([ROUTES.home])
      })
    }
  }

  passwordMatch(): boolean {
    return (
      this.authForm.get("password")?.value ===
      this.authForm.get("confirmPassword")?.value
    )
  }

  showPassword(field: "password" | "confirmPassword") {
    const oldState = this.isPasswordVisible()

    this.isPasswordVisible.set({
      ...oldState,
      [field]: !oldState[field]
    })
  }
}
