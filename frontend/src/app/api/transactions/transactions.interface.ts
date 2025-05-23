export enum TransactionType {
  BUY = "buy",
  SELL = "sell",
  TRANSFER_IN = "transfer_in",
  TRANSFER_OUT = "transfer_out"
}

export interface TransactionData {
  transaction_id: number
  portfolio_id: number
  transaction_type: TransactionType
  transaction_time: string
  quantity: string
  asset_id: number
  asset_symbol: string
  asset_name: string
  purchase_price: string | null
  current_price: string
  note: string | null
  fee?: string | null
}

export interface CreateTransactionDto {
  asset_id: number
  quantity: number | string
  price?: number | string | null
  transactionType: TransactionType
  note?: string | null
  fee?: number | string | null
}

export interface UpdateTransactionDto {
  quantity?: number | string | null
  price?: number | string | null
  note?: string | null
  fee?: number | string | null
}

export interface TransactionsPage {
  next_cursor: number | null
  items: TransactionData[]
}
