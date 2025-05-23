import { inject, Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { ENDPOINTS } from "../../consts/endpoints"
import { httpConfig } from "../../config/http.config"
import {
  CreateTransactionDto,
  TransactionsPage,
  UpdateTransactionDto
} from "./transactions.interface"

@Injectable({
  providedIn: "root"
})
export class TransactionsService {
  http = inject(HttpClient)

  getAll(portfolioId: string) {
    return this.http.get<TransactionsPage>(
      ENDPOINTS.transactions(portfolioId).main,
      httpConfig
    )
  }

  create(portfolioId: string, dto: CreateTransactionDto) {
    return this.http.post(
      ENDPOINTS.transactions(portfolioId).main,
      dto,
      httpConfig
    )
  }

  update(
    portfolioId: string,
    transactionId: string,
    dto: UpdateTransactionDto
  ) {
    return this.http.patch(
      ENDPOINTS.transactions(portfolioId).byId(transactionId),
      dto,
      httpConfig
    )
  }

  delete(portfolioId: string, transactionId: string) {
    return this.http.delete(
      ENDPOINTS.transactions(portfolioId).byId(transactionId),
      httpConfig
    )
  }
}
