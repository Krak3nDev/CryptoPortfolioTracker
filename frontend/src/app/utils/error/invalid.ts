import { AbstractControl } from "@angular/forms"

export const invalid = (group: AbstractControl, controlName: string) =>
  group.get(controlName)?.invalid && group.get(controlName)?.touched
