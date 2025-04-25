import { ModalState } from "./components/modal/state/modal.state"
import { PortfoliosListState } from "./pages/portfolios-list/state/portfoliosList.state"

export interface AppState {
  modals: ModalState
  portfolios: PortfoliosListState
}
