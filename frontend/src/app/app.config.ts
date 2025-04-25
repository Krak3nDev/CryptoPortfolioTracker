import { ApplicationConfig, provideZoneChangeDetection } from "@angular/core"
import { provideRouter } from "@angular/router"
import { routes } from "./app.routes"
import { provideHttpClient } from "@angular/common/http"
import { provideStore } from "@ngrx/store"
import { modalReducer } from "./components/modal/state/modal.reducer"
import { portfoliosListReducer } from "./pages/portfolios-list/state/portfoliosList.reducer"

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(),
    provideStore({
      modals: modalReducer,
      portfolios: portfoliosListReducer
    })
  ]
}
