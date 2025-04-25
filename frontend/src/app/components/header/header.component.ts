import { Component, inject } from "@angular/core"
import { UsersService } from "../../api/users/users.service"
import { RouterLink } from "@angular/router"
import { ModalAdapter } from "../modal/state/modal.adapter"
import { ModalComponent } from "../modal/modal.component"
import { AuthService } from "../../api/auth/auth.service"
import { ROUTES } from "../../consts/routes"

@Component({
  selector: "app-header",
  imports: [RouterLink, ModalComponent],
  templateUrl: "./header.component.html",
  styleUrl: "./header.component.scss"
})
export class HeaderComponent {
  usersService = inject(UsersService)
  authService = inject(AuthService)

  constructor(protected modalAdapter: ModalAdapter) {}

  protected readonly ROUTES = ROUTES
}
