import { CanActivateFn, Router } from "@angular/router"
import { inject } from "@angular/core"
import { ROUTES } from "../../consts/routes"
import { AuthService } from './auth.service'
import { map } from 'rxjs'

export enum CanActivateAuthType {
  AUTH,
  UNAUTH
}

export const canActivateAuth: (type: CanActivateAuthType) => CanActivateFn = type => {
  return () => {
    const authService = inject(AuthService)
    const router = inject(Router)
    const redirectPath = "/" + (type === CanActivateAuthType.AUTH ? ROUTES.login : ROUTES.home)

    return authService.me$.pipe(
      map(user => {
        const isActive = type === CanActivateAuthType.AUTH ? user?.is_active : !user?.is_active

        if (isActive) {
          return true
        }

        router.createUrlTree([redirectPath])
        return false
      })
    )
  }
}
