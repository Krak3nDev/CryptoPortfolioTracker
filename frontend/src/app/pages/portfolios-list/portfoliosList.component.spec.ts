import { ComponentFixture, TestBed } from "@angular/core/testing"

import { PortfoliosListComponent } from "./portfoliosList.component"

describe("PortfoliosListComponent", () => {
  let component: PortfoliosListComponent
  let fixture: ComponentFixture<PortfoliosListComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PortfoliosListComponent]
    }).compileComponents()

    fixture = TestBed.createComponent(PortfoliosListComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it("should create", () => {
    expect(component).toBeTruthy()
  })
})
