import React from "react"
import PropTypes from "prop-types"

export function Pagination({ totalPages, currentPage, onPageChange }) {
  const getItemProps = (index) => ({
    onClick: () => onPageChange(index),
    className: `relative h-20 max-h-[50px] w-20 max-w-[50px] select-none rounded-lg text-center align-middle font-sans text-xl font-medium uppercase ${
      currentPage === index
        ? "bg-gray-900 text-white shadow-md shadow-gray-900/10 hover:shadow-lg hover:shadow-gray-900/20"
        : "text-gray-900 transition-all hover:bg-gray-900/10 active:bg-gray-900/20"
    }`,
    type: "button"
  })

  const next = () => {
    if (currentPage === totalPages) return
    onPageChange(currentPage + 1)
  }

  const prev = () => {
    if (currentPage === 1) return
    onPageChange(currentPage - 1)
  }

  return (
    <div className="flex items-center gap-4">
      <button
        className="flex items-center gap-2 px-6 py-3 font-sans text-xs font-bold text-center text-gray-900 uppercase align-middle transition-all rounded-lg select-none hover:bg-gray-900/10 active:bg-gray-900/20 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
        onClick={prev}
        disabled={currentPage === 1}
        type="button"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={2}
          stroke="currentColor"
          aria-hidden="true"
          className="w-4 h-4"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18"
          />
        </svg>
        Previous
      </button>
      <div className="flex items-center gap-2">
        {Array.from({ length: totalPages }, (_, index) => (
          <button key={index + 1} {...getItemProps(index + 1)}>
            <span className="absolute transform -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2">
              {index + 1}
            </span>
          </button>
        ))}
      </div>
      <button
        className="flex items-center gap-2 px-6 py-3 font-sans text-xs font-bold text-center text-gray-900 uppercase align-middle transition-all rounded-lg select-none hover:bg-gray-900/10 active:bg-gray-900/20 disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none"
        onClick={next}
        disabled={currentPage === totalPages}
        type="button"
      >
        Next
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={2}
          stroke="currentColor"
          aria-hidden="true"
          className="w-4 h-4"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
          />
        </svg>
      </button>
    </div>
  )
}

Pagination.propTypes = {
  totalPages: PropTypes.number.isRequired,
  currentPage: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired
}

export default Pagination
