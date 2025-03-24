import { Component } from "@angular/core"
import { RouterOutlet } from "@angular/router"
import { HeaderComponent } from "../../components/header/header.component"

@Component({
  selector: "app-header-layout",
  imports: [RouterOutlet, HeaderComponent],
  templateUrl: "./header-layout.component.html",
  styleUrl: "./header-layout.component.scss"
})
export class HeaderLayoutComponent {}
