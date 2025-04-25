import { createSelector } from "@ngrx/store"
import { AppState } from "../../../app.state"

export const selectModalState = (state: AppState) => state.modals

export const selectModals = createSelector(
  selectModalState,
  state => state.modals
)
