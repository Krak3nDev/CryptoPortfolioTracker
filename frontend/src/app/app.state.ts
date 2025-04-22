import { ModalState } from "./components/modal/state/modal.state"
import { Store } from "@ngrx/store"
import { PortfoliosListState } from "./pages/portfolios-list/state/portfoliosList.state"

export interface AppState {
  modals: ModalState
  portfolios: PortfoliosListState
}
