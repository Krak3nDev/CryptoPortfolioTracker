import { CanActivateFn, Router } from "@angular/router"
import { inject } from "@angular/core"
import { UsersService } from "../users/users.service"
import { ROUTES } from "../../consts/routes"

export const canActivateAuth: CanActivateFn = () => {
  if (inject(UsersService).me) {
    return true
  }

  return inject(Router).createUrlTree(["/" + ROUTES.login])
}

export const canActivateUnauth: CanActivateFn = () => {
  if (!inject(UsersService).me) {
    return true
  }

  return inject(Router).createUrlTree(["/" + ROUTES.home])
}
