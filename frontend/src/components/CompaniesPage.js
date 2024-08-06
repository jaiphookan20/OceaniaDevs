// CompaniesPage.js
import React, { useState, useEffect, useCallback } from "react";
import CompaniesPageHeader from "./CompaniesPageHeader";
import CompanySearchBar from "./CompanySearchBar";
import CompanyCardSection from "./CompanyCardSection";

const CompaniesPage = () => {
    const [companies, setCompanies] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [totalCompanies, setTotalCompanies] = useState(0);
    const pageSize = 10;
  
    useEffect(() => {
      fetchCompanies();
    }, [currentPage, searchQuery]);

    const fetchCompanies = useCallback(async () => {
        try {
          const response = await fetch(`/api/companies?page=${currentPage}&page_size=${pageSize}&search=${searchQuery}`);
          const data = await response.json();
          console.log(data);
          setCompanies(data);
          setTotalCompanies(data.total_companies);
        } catch (error) {
          console.error("Error fetching companies:", error);
        }
      }, [currentPage, searchQuery, pageSize]);

      useEffect(() => {
        fetchCompanies();
      }, [fetchCompanies]);
    
      const handleSearchChange = (query) => {
        setSearchQuery(query);
        setCurrentPage(1);
      };
    
      const handlePageChange = (newPage) => {
        setCurrentPage(newPage);
      };

  return (
    <div className="max-w-6xl mx-auto">
      <CompaniesPageHeader />
      {/* <CompanySearchBar
        searchQuery={searchQuery}
        onSearchChange={handleSearchChange}
      /> */}
      <CompanySearchBar onSearchChange={handleSearchChange} />
      <CompanyCardSection
        companies={companies}
        currentPage={currentPage}
        totalCompanies={totalCompanies}
        pageSize={pageSize}
        onPageChange={handlePageChange}
      />
    </div>
  );
};

export default CompaniesPage;

// import React, { useEffect } from "react";
// import JobSection from "./JobSection";
// import SearchBar from "./SearchBar";
// import SearchPageHeader from "./SearchPageHeader";
// import SearchPageJobSection from "./SearchPageJobSection";
// import CompanyPageHeader from "./CompanyPageHeader";
// import CompaniesPageHeader from "./CompaniesPageHeader";

// const CompaniesPage = ({
//   title,
//   jobs,
//   onSave,
//   onApply,
//   onView,
//   currentPage,
//   totalJobs,
//   pageSize,
//   onPageChange,
//   searchQuery,
//   filters,
//   onSearchChange,
//   onFilterChange,
//   onFilterSearch
// }) => {
//   return (
//     <div className="max-w-6xl mx-auto">
//       <CompaniesPageHeader title={title} />
//       <SearchBar
//         searchQuery={searchQuery}
//         onSearchChange={onSearchChange}
//         filters={filters}
//         onFilterChange={onFilterChange}
//         onFilterSearch={onFilterSearch}
//       />
//       <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-7">
//         <div className="col-span-2">
//           <SearchPageJobSection
//             title={`${filters.specialization || 'All'} Roles`}
//             jobs={jobs}
//             currentPage={currentPage}
//             totalJobs={totalJobs}
//             pageSize={pageSize}
//             onPageChange={onPageChange}
//           />
//         </div>
//       </div>
//     </div>
//   );
// };

// export default CompaniesPage;
