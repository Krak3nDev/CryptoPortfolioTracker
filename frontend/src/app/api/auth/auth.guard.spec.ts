import { TestBed } from "@angular/core/testing"
import { CanActivateFn } from "@angular/router"

import { canActivateAuth, CanActivateAuthType } from "./canActivateAuth"

describe("authGuard", () => {
  const executeGuard: CanActivateFn = (...guardParameters) =>
    TestBed.runInInjectionContext(() =>
      canActivateAuth(CanActivateAuthType.AUTH)(...guardParameters)
    )

  beforeEach(() => {
    TestBed.configureTestingModule({})
  })

  it("should be created", () => {
    expect(executeGuard).toBeTruthy()
  })
})
