import { ComponentFixture, TestBed } from "@angular/core/testing"
import { ErrorComponent } from "./error.component"
import { FaIconComponent } from "@fortawesome/angular-fontawesome"
import { ComponentRef } from "@angular/core"

describe("AuthErrorComponent", () => {
  let component: ErrorComponent
  let componentRef: ComponentRef<ErrorComponent>
  let fixture: ComponentFixture<ErrorComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FaIconComponent, ErrorComponent]
    }).compileComponents()

    fixture = TestBed.createComponent(ErrorComponent)
    component = fixture.componentInstance
    componentRef = fixture.componentRef
    fixture.detectChanges()
  })

  it("should create", () => {
    expect(component).toBeTruthy()
  })
})
