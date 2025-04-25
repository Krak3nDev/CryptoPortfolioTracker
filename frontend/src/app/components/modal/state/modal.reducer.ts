import { createReducer, on } from "@ngrx/store"
import { initialModalState } from "./modal.state"
import * as ModalActions from "./modal.actions"

export const modalReducer = createReducer(
  initialModalState,
  on(ModalActions.openModal, (state, { modalId }) => ({
    ...state,
    modals: {
      ...state.modals,
      [modalId]: { isOpen: true }
    }
  })),
  on(ModalActions.closeModal, (state, { modalId }) => ({
    ...state,
    modals: {
      ...state.modals,
      [modalId]: { ...state.modals[modalId], isOpen: false }
    }
  }))
)
