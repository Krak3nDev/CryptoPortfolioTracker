import { Component, inject, signal } from "@angular/core"
import { Router, RouterLink } from '@angular/router'
import { ROUTES } from "../../consts/routes"
import { ConfirmService } from "../../api/confirm/confirm.service"
import { FaIconComponent } from '@fortawesome/angular-fontawesome'
import { faTriangleExclamation } from '@fortawesome/free-solid-svg-icons'
import { authErrors } from '../../consts/errors/auth.errors'

@Component({
  selector: "app-confirm",
  imports: [FaIconComponent, RouterLink],
  templateUrl: "./confirm.component.html",
  styleUrl: "./confirm.component.scss"
})
export class ConfirmComponent {
  router = inject(Router)
  confirmService = inject(ConfirmService)

  error = signal(false)
  isToken = signal(false)
  message = signal(authErrors.common)
  icon = faTriangleExclamation

  ngOnInit() {
    const url = this.router.url.split("/")

    if (url.lastIndexOf(ROUTES.confirm) !== url.length - 1) {
      const token = url.pop()

      if (token) {
        this.isToken.set(true)

        this.confirmService.confirm({ token }).subscribe(
          _res => this.router.navigate([ROUTES.home]),
          error => {
            if (error.status === 404) {
              this.message.set(authErrors.token)
              return
            }

            this.error.set(true)
          }
        )
      }
    }
  }
}
