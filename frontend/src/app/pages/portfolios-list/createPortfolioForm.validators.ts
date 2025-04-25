import { AbstractControl, Validators } from "@angular/forms"

export const fileExt = ["png", "jpg", "jpeg"]

export const createPortfolioFormValidators = () => ({
  name: [Validators.required],
  avatar: [
    (control: AbstractControl) => {
      const file: File = control.value

      if (file) {
        const ext = file.name.split(".").pop() || ""

        if (fileExt.includes(ext)) {
          return null
        }

        return {
          wrongExt: true
        }
      }

      return {
        required: true
      }
    }
  ]
})
