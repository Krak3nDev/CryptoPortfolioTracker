import Header from "../components/Header.jsx"
import TableCryptocurrencies from "../components/TableCryptocurrencies.jsx"
import { testData } from "../constants.js"
import React from "react"

function MainPage() {
  return (
    <div>
      <Header />
      <TableCryptocurrencies data={testData}></TableCryptocurrencies>
    </div>
  )
}

export default MainPage
