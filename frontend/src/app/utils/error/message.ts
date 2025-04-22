import { AbstractControl } from "@angular/forms"
import { commonErrors } from "../../consts/errors/common.errors"

export const message = (
  errors: Record<string, string>,
  group: AbstractControl,
  controlName: string
) => {
  const type = Object.keys(group.get(controlName)?.errors || {}).pop()

  return type ? errors[type] : commonErrors.main
}
