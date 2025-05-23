import { inject, Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { ENDPOINTS } from "../../consts/endpoints"
import {
  PortfolioData,
  PortfolioStats,
  PortfolioSummary
} from "./portfolios.interface"
import { httpConfig } from "../../config/http.config"

@Injectable({
  providedIn: "root"
})
export class PortfoliosService {
  http = inject(HttpClient)

  create(payload: FormData) {
    return this.http.post(ENDPOINTS.portfolios.main, payload, httpConfig)
  }

  update(payload: FormData) {
    return this.http.patch(
      ENDPOINTS.portfolios.main,
      payload,
      httpConfig
    )
  }

  delete(id: string) {
    return this.http.delete(ENDPOINTS.portfolios.byId(id), httpConfig)
  }

  getAll() {
    return this.http.get<PortfolioData[]>(ENDPOINTS.portfolios.main, httpConfig)
  }

  getSummary() {
    return this.http.get<PortfolioSummary>(
      ENDPOINTS.portfolios.summary,
      httpConfig
    )
  }

  getById(id: string) {
    return this.http.get<PortfolioStats>(
      ENDPOINTS.portfolios.byIdSummary(id),
      httpConfig
    )
  }
}
