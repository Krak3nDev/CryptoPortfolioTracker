import React, { useState } from "react"
import PropTypes from "prop-types"
import { FaArrowDown, FaArrowUp } from "react-icons/fa"

function TableCryptocurrencies({ data }) {
  const [sortConfig, setSortConfig] = useState({
    key: "name",
    direction: "ascending",
  })

  const sortedData = React.useMemo(() => {
    let sortableItems = [...data]
    sortableItems.sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) {
        return sortConfig.direction === "ascending" ? -1 : 1
      }
      if (a[sortConfig.key] > b[sortConfig.key]) {
        return sortConfig.direction === "ascending" ? 1 : -1
      }
      return 0
    })
    return sortableItems
  }, [data, sortConfig])

  const requestSort = (key) => {
    let direction = "ascending"
    if (sortConfig.key === key && sortConfig.direction === "ascending") {
      direction = "descending"
    }
    setSortConfig({ key, direction })
  }

  const getSortIcon = (key) => {
    if (sortConfig.key === key) {
      return sortConfig.direction === "ascending" ? (
        <FaArrowUp className="inline mr-1" />
      ) : (
        <FaArrowDown className="inline mr-1" />
      )
    }
    return null
  }

  return (
    <div className="w-full px-24 bg-white">
      <div className="py-0">
        <div>
          <h2 className="text-4xl font-semibold leading-tight">
            Cryptocurrency Prices
          </h2>
        </div>
        <div className="py-4 overflow-x-auto">
          <div className="inline-block min-w-full shadow-md rounded-lg overflow-hidden">
            <table className="min-w-full leading-normal">
              <thead>
                <tr>
                  <th className="px-5 py-3 border-b-2 border-gray-200 bg-white text-left text-xs font-semibold text-gray-900 tracking-wider">
                    #
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-white text-left text-xs font-semibold text-gray-900 tracking-wider cursor-pointer"
                    onClick={() => requestSort("name")}
                  >
                    {getSortIcon("name")}
                    Name
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-white text-left text-xs font-semibold text-gray-900 tracking-wider cursor-pointer"
                    onClick={() => requestSort("price")}
                  >
                    {getSortIcon("price")}
                    Price
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-white text-left text-xs font-semibold text-gray-900 tracking-wider cursor-pointer"
                    onClick={() => requestSort("change1h")}
                  >
                    {getSortIcon("change1h")}
                    1h %
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-white text-left text-xs font-semibold text-gray-900 tracking-wider cursor-pointer"
                    onClick={() => requestSort("change24h")}
                  >
                    {getSortIcon("change24h")}
                    24h %
                  </th>
                  <th
                    className="px-5 py-3 border-b-2 border-gray-200 bg-white text-left text-xs font-semibold text-gray-900 tracking-wider cursor-pointer"
                    onClick={() => requestSort("change7d")}
                  >
                    {getSortIcon("change7d")}
                    7d %
                  </th>
                </tr>
              </thead>
              <tbody className="font-bold text-gray-900">
                {sortedData.map((currency, index) => (
                  <tr key={currency.name}>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      {index + 1}
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 w-10 h-10">
                          <img
                            className="w-full h-full rounded-full"
                            src={currency.image}
                            alt={currency.name}
                          />
                        </div>
                        <div className="ml-3">
                          <p className="whitespace-no-wrap">{currency.name}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      ${currency.price.toLocaleString()}
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      <span
                        className={
                          currency.change1h > 0
                            ? "text-green-500"
                            : "text-red-500"
                        }
                      >
                        {currency.change1h}%
                      </span>
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      <span
                        className={
                          currency.change24h > 0
                            ? "text-green-500"
                            : "text-red-500"
                        }
                      >
                        {currency.change24h}%
                      </span>
                    </td>
                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                      <span
                        className={
                          currency.change7d > 0
                            ? "text-green-500"
                            : "text-red-500"
                        }
                      >
                        {currency.change7d}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

TableCryptocurrencies.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      image: PropTypes.string.isRequired,
      price: PropTypes.number.isRequired,
      change1h: PropTypes.number.isRequired,
      change24h: PropTypes.number.isRequired,
      change7d: PropTypes.number.isRequired,
    }),
  ).isRequired,
}

export default TableCryptocurrencies
