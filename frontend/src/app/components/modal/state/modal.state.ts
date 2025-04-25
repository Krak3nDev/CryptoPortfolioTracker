export interface ModalOptions {
  isOpen: boolean
}

export interface ModalState {
  modals: Record<string, ModalOptions>
}

export const initialModalState: ModalState = {
  modals: {}
}
