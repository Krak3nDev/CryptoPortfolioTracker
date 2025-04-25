import { AbstractControl, ValidationErrors, Validators } from "@angular/forms"
import { WritableSignal } from "@angular/core"

export const authFormValidators = (isRegister: WritableSignal<boolean>) => ({
  username: [Validators.required],
  email: [
    (control: AbstractControl) =>
      isRegister() ? Validators.required(control) : null,
    Validators.email
  ],
  password: [Validators.required],
  confirmPassword: [
    (control: AbstractControl) =>
      isRegister() ? Validators.required(control) : null
  ],
  passwordMatch: [
    (group: AbstractControl) => {
      if (!isRegister()) {
        return null
      }

      if (
        group.get("password")?.value === group.get("confirmPassword")?.value
      ) {
        return null
      }

      const error: ValidationErrors = {
        mismatch: true
      }

      group.get("confirmPassword")?.setErrors(error)

      return error
    }
  ]
})
