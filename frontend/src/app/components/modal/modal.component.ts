import { Component, HostListener, Input, signal } from "@angular/core"
import { findParentById } from "../../utils/dom/find"
import { ModalAdapter } from "./state/modal.adapter"

interface ModalOptions {
  closeOutside?: boolean
}

@Component({
  standalone: true,
  selector: "app-modal",
  imports: [],
  templateUrl: "./modal.component.html",
  styleUrl: "./modal.component.scss"
})
export class ModalComponent {
  @Input({ required: true }) modalId!: string
  @Input() options: ModalOptions = {}
  isOpen = signal(false)

  constructor(private modalAdapter: ModalAdapter) {
    this.modalAdapter.select().subscribe(res => {
      this.isOpen.set(res[this.modalId]?.isOpen)
    })
  }

  @HostListener("document:click", ["$event.target"])
  onClickOutside(target: HTMLElement) {
    if (
      this.options?.closeOutside &&
      this.isOpen() &&
      !findParentById(target, ["modal", `modal-target-${this.modalId}`])
    ) {
      this.modalAdapter.close(this.modalId)
    }
  }
}
