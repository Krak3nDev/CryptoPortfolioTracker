import { createReducer, on } from "@ngrx/store"
import { initialPortfoliosListState } from "./portfoliosList.state"
import * as PortfoliosListActions from "./portfoliosList.actions"

export const portfoliosListReducer = createReducer(
  initialPortfoliosListState,
  on(PortfoliosListActions.listUpdateAction, state => ({
    ...state,
    portfolios: {
      ...state.portfolios,
      list: {
        result: [],
        error: null,
        isLoading: true
      }
    }
  })),
  on(PortfoliosListActions.listUpdateActionSuccess, (state, { list }) => ({
    ...state,
    portfolios: {
      ...state.portfolios,
      list: {
        result: list,
        error: null,
        isLoading: false
      }
    }
  })),
  on(PortfoliosListActions.listUpdateActionFailure, (state, { error }) => ({
    ...state,
    portfolios: {
      ...state.portfolios,
      list: {
        result: [],
        error,
        isLoading: false
      }
    }
  })),
  on(PortfoliosListActions.createPortfolioAction, state => ({
    ...state,
    portfolios: {
      ...state.portfolios,
      newPortfolio: {
        error: null,
        isLoading: true
      }
    }
  })),
  on(PortfoliosListActions.createPortfolioActionSuccess, state => ({
    ...state,
    portfolios: {
      ...state.portfolios,
      newPortfolio: {
        error: null,
        isLoading: false
      }
    }
  })),
  on(
    PortfoliosListActions.createPortfolioActionFailure,
    (state, { error }) => ({
      ...state,
      portfolios: {
        ...state.portfolios,
        newPortfolio: {
          error,
          isLoading: false
        }
      }
    })
  )
)
