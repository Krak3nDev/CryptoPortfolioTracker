import { createAction, props } from "@ngrx/store"

export const openModal = createAction(
  "[Modal] Open Modal",
  props<{ modalId: string }>()
)

export const closeModal = createAction(
  "[Modal] Close Modal",
  props<{ modalId: string }>()
)
