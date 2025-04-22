import { Routes } from "@angular/router"
import { ROUTES } from "./consts/routes"
import { AuthComponent } from "./pages/auth/auth.component"
import { HeaderLayoutComponent } from "./layout/header-layout/header-layout.component"
import { ConfirmComponent } from "./pages/confirm/confirm.component"
import { HomeComponent } from "./pages/home/home.component"
import { canActivateAuth, canActivateUnauth } from "./api/auth/canActivateAuth"
import { PortfoliosListComponent } from "./pages/portfolios-list/portfoliosList.component"

export const routes: Routes = [
  {
    path: ROUTES.register,
    component: AuthComponent,
    title: "Registration",
    canActivate: [canActivateUnauth]
  },
  {
    path: ROUTES.login,
    component: AuthComponent,
    title: "Login",
    canActivate: [canActivateUnauth]
  },
  {
    path: ROUTES.confirm,
    component: ConfirmComponent,
    title: "Please confirm",
    canActivate: [canActivateUnauth]
  },
  {
    path: ROUTES.confirmByToken,
    component: ConfirmComponent,
    title: "Confirmation",
    canActivate: [canActivateUnauth]
  },
  {
    path: "",
    component: HeaderLayoutComponent,
    children: [
      {
        path: ROUTES.home,
        component: HomeComponent
      },
      {
        path: ROUTES.home,
        canActivate: [canActivateAuth],
        children: [
          {
            path: ROUTES.portfoliosList,
            component: PortfoliosListComponent
          }
        ]
      }
    ]
  }
]
