import { inject, Injectable } from "@angular/core"
import { AppState } from "../../../app.state"
import { Store } from "@ngrx/store"
import { selectPortfoliosList } from "./portfoliosList.selectors"
import { PortfoliosService } from "../../../api/portfolios/portfolios.service"
import {
  createPortfolioAction,
  createPortfolioActionFailure,
  createPortfolioActionSuccess,
  listUpdateAction,
  listUpdateActionFailure,
  listUpdateActionSuccess
} from "./portfoliosList.actions"
import { map } from "rxjs"
import { growthTypes } from "../../../consts/portfolios/growthTypes"
import {
  CreatePortfolioRequest,
  PortfolioData
} from "../../../api/portfolios/portfolios.interface"
import { PortfolioDataWithType } from "./portfoliosList.state"
import { commonErrors } from "../../../consts/errors/common.errors"

@Injectable({ providedIn: "root" })
export class PortfoliosListAdapter {
  portfoliosService = inject(PortfoliosService)

  constructor(private store: Store<AppState>) {}

  select() {
    return this.store.select(selectPortfoliosList)
  }

  updateList(finallyFn?: () => void) {
    this.store.dispatch(listUpdateAction())

    this.portfoliosService
      .getAll()
      .pipe(map(list => this.mapPortfoliosDataWithType(list)))
      .subscribe(
        list => {
          this.store.dispatch(listUpdateActionSuccess({ list }))
        },
        error => {
          this.store.dispatch(
            listUpdateActionFailure({
              error: error?.message || commonErrors.main
            })
          )
        }
      )
      .add(
        // finallyFn
        () => {
          const list = new Array(5).fill(null).map((_, i) => {
            const current = Math.floor(Math.random() * 10000)
            const change = Math.floor(Math.random() * 1000) - 500

            return {
              portfolio_id: i,
              portfolio_name: `Portfolio ${i}`,
              avatar:
                "https://s3.coinmarketcap.com/static/img/portraits/63351fb59b613d345489037c.png",
              total_value: current + change + "",
              value_change_24h: change + "",
              percent_change_24h:
                Math.floor((change / current) * 10000) / 100 + "",
              type: growthTypes.get(Math.sign(change)) || "middle"
            }
          })

          this.store.dispatch(listUpdateActionSuccess({ list }))
        }
      )
  }

  createNewPortfolio(payload: CreatePortfolioRequest, finallyFn?: () => void) {
    this.store.dispatch(createPortfolioAction())

    this.portfoliosService
      .create(payload)
      .subscribe(
        () => {
          this.store.dispatch(createPortfolioActionSuccess())
        },
        error => {
          this.store.dispatch(
            createPortfolioActionFailure({
              error: error?.message || commonErrors.main
            })
          )
        }
      )
      .add(finallyFn)
  }

  private mapPortfoliosDataWithType(
    list: PortfolioData[]
  ): PortfolioDataWithType[] {
    return list.map(data => ({
      ...data,
      type:
        growthTypes.get(Math.sign(Number(data.value_change_24h))) || "middle"
    }))
  }
}
