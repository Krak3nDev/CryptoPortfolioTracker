import { Component, inject, signal } from "@angular/core"
import { CreatePortfolioRequest } from "../../api/portfolios/portfolios.interface"
import { PortfoliosService } from "../../api/portfolios/portfolios.service"
import { faTrash, faUpload } from "@fortawesome/free-solid-svg-icons"
import { FaIconComponent } from "@fortawesome/angular-fontawesome"
import { ModalComponent } from "../../components/modal/modal.component"
import { ModalAdapter } from "../../components/modal/state/modal.adapter"
import { FormControl, FormGroup, ReactiveFormsModule } from "@angular/forms"
import { createPortfolioFormValidators } from "./createPortfolioForm.validators"
import {
  initialPortfoliosListState,
  PortfoliosListState
} from "./state/portfoliosList.state"
import { PortfoliosListAdapter } from "./state/portfoliosList.adapter"
import { ErrorComponent } from "../../components/error/error.component"
import { portfoliosListErrors } from "../../consts/errors/portfoliosList.errors"
import { invalid } from "../../utils/error/invalid"
import { message } from "../../utils/error/message"

@Component({
  selector: "app-portfolios-list",
  imports: [
    FaIconComponent,
    ModalComponent,
    ReactiveFormsModule,
    ErrorComponent
  ],
  templateUrl: "./portfoliosList.component.html",
  styleUrl: "./portfoliosList.component.scss"
})
export class PortfoliosListComponent {
  portfoliosService = inject(PortfoliosService)
  portfolios = signal<PortfoliosListState["portfolios"]>(
    initialPortfoliosListState.portfolios
  )
  icons = {
    delete: faTrash,
    upload: faUpload
  }
  validators = createPortfolioFormValidators()
  createPortfolioForm = new FormGroup({
    name: new FormControl<string>("", this.validators.name),
    avatar: new FormControl<File | null>(null, this.validators.avatar)
  })

  constructor(
    protected portfoliosListAdapter: PortfoliosListAdapter,
    protected modalAdapter: ModalAdapter
  ) {
    this.portfoliosListAdapter.select().subscribe(this.portfolios.set)
  }

  ngOnInit() {
    this.portfoliosListAdapter.updateList()
  }

  uploadFile(event: Event) {
    const target = event.target! as HTMLInputElement
    const avatar = target.files && target.files[0]

    this.createPortfolioForm.patchValue({ avatar })
    this.createPortfolioForm.updateValueAndValidity()
    this.createPortfolioForm.controls.avatar.markAsTouched()
  }

  createPortfolio() {
    if (this.createPortfolioForm.invalid) {
      this.createPortfolioForm.markAsTouched()
      this.createPortfolioForm.controls.name.markAsTouched()
      this.createPortfolioForm.controls.avatar.markAsTouched()
      return
    }

    const payload: CreatePortfolioRequest = {
      name: this.createPortfolioForm.value.name!,
      avatar: this.createPortfolioForm.value.avatar!.toString()
    }

    this.portfoliosListAdapter.createNewPortfolio(payload, () => {
      console.log(this.portfolios().newPortfolio.error)
      this.modalAdapter.close("new-portfolio")
      this.portfoliosListAdapter.updateList()
    })
  }

  deletePortfolio(id: string) {
    this.modalAdapter.close(id)

    this.portfoliosService.delete(id).subscribe(() => {
      this.portfoliosListAdapter.updateList()
    })
  }

  protected readonly portfoliosListErrors = portfoliosListErrors
  protected readonly invalid = invalid
  protected readonly message = message
}
