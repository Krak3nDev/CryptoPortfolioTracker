export interface Asset {
  asset_id: number
  asset_symbol: string
  total_quantity: string
  current_price: string
  change_1h: string
  change_24h: string
  change_7d: string
  total_value: string
  allocation_percentage: string
}

export interface AssetWithProfitLoss extends Asset {
  asset_name: string
  average_buy_price: string
  profit_loss_usd: string
  profit_loss_percentage: string
}

export interface PerformerData {
  symbol: string
  name: string
  change_value: string
  change_percentage: string
}

export interface PortfolioData {
  portfolio_id: number
  portfolio_name: string
  avatar: string
  total_value: string
  value_change_24h: string
  percent_change_24h: string
}

export interface PortfolioSummary {
  total_value: string
  total_value_change_24h: string
  total_value_change_24h_percentage: string
  holdings: Asset[]
}

export interface PortfolioStats {
  total_value?: string
  total_value_change_24h?: string
  total_value_change_24h_percentage?: string
  all_time_profit?: string
  cost_basis?: string
  best_performer?: PerformerData
  worst_performer?: PerformerData
  holdings: AssetWithProfitLoss[]
}

export interface CreatePortfolioRequest {
  name: string
  avatar?: string
}

export interface CreatePortfolioResponse {
  portfolio_id: string
  name: string
  avatar: string
}

export interface UpdatePortfolioRequest {
  portfolio_id: string
  name?: string
  avatar?: string
}
