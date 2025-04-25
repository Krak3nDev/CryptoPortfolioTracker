import { PortfolioData } from "../../../api/portfolios/portfolios.interface"
import { GrowthType } from "../../../consts/portfolios/growthTypes"

export interface PortfolioDataWithType extends PortfolioData {
  type: GrowthType
}

export interface PortfoliosListState {
  portfolios: {
    list: {
      result: PortfolioDataWithType[]
      isLoading: boolean
      error: string | null
    }
    newPortfolio: {
      isLoading: boolean
      error: string | null
    }
  }
}

export const initialPortfoliosListState: PortfoliosListState = {
  portfolios: {
    list: {
      result: [],
      isLoading: false,
      error: null
    },
    newPortfolio: {
      isLoading: false,
      error: null
    }
  }
}
