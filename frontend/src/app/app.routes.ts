import { Routes } from "@angular/router"
import { ROUTES } from "./consts/routes"
import { AuthComponent } from "./pages/auth/auth.component"
import { HeaderLayoutComponent } from "./layout/header-layout/header-layout.component"
import { ConfirmComponent } from "./pages/confirm/confirm.component"

export const routes: Routes = [
  {
    path: ROUTES.register,
    component: AuthComponent,
    title: "Registration"
  },
  {
    path: ROUTES.login,
    component: AuthComponent,
    title: "Login"
  },
  {
    path: ROUTES.confirm,
    component: ConfirmComponent,
    title: "Please confirm"
  },
  {
    path: ROUTES.confirmByToken,
    component: ConfirmComponent,
    title: "Confirmation"
  },
  {
    path: "",
    component: HeaderLayoutComponent
  }
]
