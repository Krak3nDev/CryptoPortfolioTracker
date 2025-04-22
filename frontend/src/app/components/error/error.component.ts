import { Component, Input } from "@angular/core"
import { FaIconComponent } from "@fortawesome/angular-fontawesome"
import { faTriangleExclamation } from "@fortawesome/free-solid-svg-icons"

@Component({
  selector: "app-form-error",
  imports: [FaIconComponent],
  templateUrl: "./error.component.html",
  styleUrl: "./error.component.scss"
})
export class ErrorComponent {
  @Input({ required: true }) message!: string
  icon = faTriangleExclamation
}
