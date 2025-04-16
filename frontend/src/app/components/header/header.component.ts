import { Component, HostListener, inject, signal } from '@angular/core'
import { UsersService } from "../../api/users/users.service"
import { RouterLink } from '@angular/router'
import { findParentById } from '../../utils/dom/find'

@Component({
  selector: "app-header",
  imports: [RouterLink],
  templateUrl: "./header.component.html",
  styleUrl: "./header.component.scss"
})
export class HeaderComponent {
  usersService = inject(UsersService)
  isOpenDropdown = signal(false)

  dropdownToggle() {
    this.isOpenDropdown.set(!this.isOpenDropdown())
  }

  @HostListener("document:click", ["$event.target"])
  onClickOutside(target: HTMLElement) {
    if (this.isOpenDropdown() && !findParentById(target, ["spoiler-dropdown", "spoiler-button"])) {
      this.isOpenDropdown.set(false)
    }
  }
}
