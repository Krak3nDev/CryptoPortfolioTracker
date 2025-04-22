import { AppState } from "../../../app.state"
import { createSelector } from "@ngrx/store"

export const selectPortfoliosListState = (state: AppState) => state.portfolios

export const selectPortfoliosList = createSelector(
  selectPortfoliosListState,
  state => state.portfolios
)
