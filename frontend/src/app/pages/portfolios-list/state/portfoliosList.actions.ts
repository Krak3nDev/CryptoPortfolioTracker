import { createAction, props } from "@ngrx/store"
import { PortfoliosListState } from "./portfoliosList.state"

export const listUpdateAction = createAction("[Portfolios List] Update list")

export const listUpdateActionSuccess = createAction(
  "[Portfolios List] Update list success",
  props<{ list: PortfoliosListState["portfolios"]["list"]["result"] }>()
)

export const listUpdateActionFailure = createAction(
  "[Portfolios List] Update list error",
  props<{ error: PortfoliosListState["portfolios"]["list"]["error"] }>()
)

export const createPortfolioAction = createAction(
  "[Portfolios List] create portfolio"
)

export const createPortfolioActionSuccess = createAction(
  "[Portfolios List] create portfolio success"
)

export const createPortfolioActionFailure = createAction(
  "[Portfolios List] create portfolio failure",
  props<{ error: PortfoliosListState["portfolios"]["newPortfolio"]["error"] }>()
)
