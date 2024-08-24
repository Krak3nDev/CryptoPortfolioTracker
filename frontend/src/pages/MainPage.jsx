import React, { useEffect, useState } from "react"
import Header from "../components/Header.jsx"
import TableCryptocurrencies from "../components/TableCryptocurrencies.jsx"
import { testData } from "../constants.js"
import Pagination from "../components/Pagination.jsx"

function MainPage() {
  const [currentPage, setCurrentPage] = useState(1)
  const [data, setData] = useState([])
  const itemsPerPage = 10

  const loadData = (page) => {
    const startIndex = (page - 1) * itemsPerPage
    const paginatedData = testData.slice(startIndex, startIndex + itemsPerPage)
    setData(paginatedData)
  }

  useEffect(() => {
    loadData(currentPage)
  }, [currentPage])

  const totalPages = Math.ceil(testData.length / itemsPerPage)

  const handlePageChange = (page) => {
    setCurrentPage(page)
  }

  return (
    <div>
      <Header />
      <div className="flex flex-col items-center mb-5 ">
        <TableCryptocurrencies data={data} />
        <div className="mt-2 pb-10">
          <Pagination
            totalPages={totalPages}
            currentPage={currentPage}
            onPageChange={handlePageChange}
          />
        </div>
      </div>
    </div>
  )
}

export default MainPage
