import { Component, inject, signal } from "@angular/core"
import { Router } from "@angular/router"
import { ROUTES } from "../../consts/routes"
import { ConfirmService } from "../../api/confirm/confirm.service"

@Component({
  selector: "app-confirm",
  imports: [],
  templateUrl: "./confirm.component.html",
  styleUrl: "./confirm.component.scss"
})
export class ConfirmComponent {
  router = inject(Router)
  confirmService = inject(ConfirmService)

  error = signal(false)

  ngOnInit() {
    const url = this.router.url.split("/")

    if (url.lastIndexOf(ROUTES.confirm) !== url.length - 1) {
      const token = url.pop()

      if (token) {
        this.confirmService.confirm({ token }).subscribe(
          _res => this.router.navigate([ROUTES.home]),
          _err => this.error.set(true)
        )
      }
    }
  }
}
