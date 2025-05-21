import { Component, inject } from '@angular/core'
import { RouterLink } from "@angular/router"
import { AuthService } from '../../api/auth/auth.service'
import { ROUTES } from "../../consts/routes"

@Component({
  selector: "app-home",
  imports: [RouterLink],
  templateUrl: "./home.component.html",
  styleUrl: "./home.component.scss"
})
export class HomeComponent {
  authService = inject(AuthService)

  protected readonly ROUTES = ROUTES
}
