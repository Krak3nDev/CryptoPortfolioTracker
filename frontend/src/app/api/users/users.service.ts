import { inject, Injectable } from "@angular/core"
import { HttpClient } from "@angular/common/http"
import { User } from "./users.interface"

@Injectable({
  providedIn: "root"
})
export class UsersService {
  http = inject(HttpClient)
  me: User | null = null

  constructor() {
    // this.getMe().subscribe(res => {
    //   this.me = res || null
    // })

    this.me = {
      id: "1"
    }
  }

  getMe() {
    return this.http.get<User>("")
  }
}
