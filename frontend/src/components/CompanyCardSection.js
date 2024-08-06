// CompanyCardSection.js
import React from "react";
import CompanyCard from "./CompanyCard";

const CompanyCardSection = ({
  companies,
  currentPage,
  totalCompanies,
  pageSize,
  onPageChange,
}) => {
  return (
    <div className="mx-auto max-w-6xl">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {companies.map((company) => (
          <CompanyCard key={company.company_id} company={company} />
        ))}
      </div>
      <div className="flex justify-between items-center mt-4 mb-14">
        <button
          disabled={currentPage === 1}
          onClick={() => onPageChange(currentPage - 1)}
          className="px-4 py-2 bg-black text-white rounded"
        >
          Previous
        </button>
        <span>
          Page {currentPage} of {Math.ceil(totalCompanies / pageSize)}
        </span>
        <button
          disabled={currentPage === Math.ceil(totalCompanies / pageSize)}
          onClick={() => onPageChange(currentPage + 1)}
          className="px-4 py-2 bg-black text-white rounded"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default CompanyCardSection;