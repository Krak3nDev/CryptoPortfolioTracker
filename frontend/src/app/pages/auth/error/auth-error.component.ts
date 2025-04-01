import { Component, input, signal } from '@angular/core'
import { authErrors } from "../../../consts/errors/auth.errors"
import { ValidationErrors } from "@angular/forms"
import { FaIconComponent } from "@fortawesome/angular-fontawesome"
import { faTriangleExclamation } from "@fortawesome/free-solid-svg-icons"

@Component({
  selector: "app-auth-error",
  imports: [FaIconComponent],
  templateUrl: "./auth-error.component.html",
  styleUrl: "./auth-error.component.scss"
})
export class AuthErrorComponent {
  isError = signal(false)
  error = input<string | null, ValidationErrors | null | undefined>(null, {
    transform: value => {
      const error = (value && Object.keys(value).shift()) || null

      this.updateMessage(error)

      return error
    }
  })
  message = signal("")
  icon = faTriangleExclamation

  private updateMessage(error: string | null) {
    if (!error) {
      this.message.set("")
      this.isError.set(false)
      return
    }

    if (Object.prototype.hasOwnProperty.call(authErrors, error)) {
      this.message.set(authErrors[error as keyof typeof authErrors])
      this.isError.set(true)
    } else {
      this.message.set("")
      this.isError.set(false)
    }
  }
}
