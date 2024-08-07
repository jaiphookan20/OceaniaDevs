import React from "react";
import CompanyCard from "./CompanyCard";

const CompanyCardSection = ({
  companies,
  currentPage,
  totalCompanies,
  pageSize,
  onPageChange,
}) => {
  if (!Array.isArray(companies)) {
    console.error("companies is not an array:", companies);
    return <div>Error: Invalid company data</div>;
  }

  return (
    <div>
      <div className="flex justify-between">
        <div className="text-sm text-gray-600 mb-4">
          Showing {companies.length} of {totalCompanies || 0}+ companies
        </div>
        <div className="flex justify-end mb-4">
          <div className="mr-2">Sort by</div>
          <select className="border rounded px-2 py-1">
              <option>Default</option>
          </select>
        </div>
      </div>
      
      <div className="">
        {companies.map((company) => (
          <CompanyCard key={company.company_id} company={company} />
        ))}
      </div>
      {totalCompanies > pageSize && (
        <div className="flex justify-between items-center mt-8">
          <button
            disabled={currentPage === 1}
            onClick={() => onPageChange(currentPage - 1)}
            className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
          >
            Previous
          </button>
          <span>
            Page {currentPage} of {Math.ceil((totalCompanies || 0) / pageSize)}
          </span>
          <button
            disabled={currentPage === Math.ceil((totalCompanies || 0) / pageSize)}
            onClick={() => onPageChange(currentPage + 1)}
            className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default CompanyCardSection;


