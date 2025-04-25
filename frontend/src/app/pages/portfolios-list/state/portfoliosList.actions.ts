import { createAction, props } from "@ngrx/store"
import { PortfoliosListState } from "./portfoliosList.state"

export const listUpdateAction = createAction("[Portfolios List] Update List")

export const listUpdateActionSuccess = createAction(
  "[Portfolios List] Update List Success",
  props<{ list: PortfoliosListState["portfolios"]["list"]["result"] }>()
)

export const listUpdateActionFailure = createAction(
  "[Portfolios List] Update List Failure",
  props<{ error: PortfoliosListState["portfolios"]["list"]["error"] }>()
)

export const createPortfolioAction = createAction(
  "[Portfolios List] Create Portfolio"
)

export const createPortfolioActionSuccess = createAction(
  "[Portfolios List] Create Portfolio Success"
)

export const createPortfolioActionFailure = createAction(
  "[Portfolios List] Create Portfolio Failure",
  props<{ error: PortfoliosListState["portfolios"]["newPortfolio"]["error"] }>()
)
