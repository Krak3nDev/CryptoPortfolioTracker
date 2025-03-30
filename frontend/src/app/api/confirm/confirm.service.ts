import { inject, Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { ConfirmBodyRequest } from "./confirm.interface"
import { ENDPOINTS } from "../../consts/endpoints"

@Injectable({
  providedIn: "root"
})
export class ConfirmService {
  http = inject(HttpClient)

  confirm(payload: ConfirmBodyRequest) {
    return this.http.get(ENDPOINTS.users.confirm(payload.token))
  }
}
