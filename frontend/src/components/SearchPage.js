import React, { useEffect } from "react";
import JobSection from "./JobSection";
import SearchBar from "./SearchBar";
import SearchPageHeader from "./SearchPageHeader";
import SearchPageJobSection from "./SearchPageJobSection";

const SearchPage = ({
  title,
  jobs,
  onSave,
  onApply,
  onView,
  currentPage,
  totalJobs,
  pageSize,
  onPageChange,
  searchQuery,
  filters,
  onSearchChange,
  onFilterChange,
  onFilterSearch
}) => {
  useEffect(() => {
    // Trigger a search when the component mounts or when filters change
    onFilterSearch();
  }, [filters]);

  return (
    <div className="max-w-6xl mx-auto">
       <SearchPageHeader title={title} />
      <SearchBar
        searchQuery={searchQuery}
        onSearchChange={onSearchChange}
        filters={filters}
        onFilterChange={onFilterChange}
        onFilterSearch={onFilterSearch}
      />
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-7">
        <div className="col-span-2">
          <SearchPageJobSection
            title={`${filters.specialization || 'All'} Roles`}
            jobs={jobs}
            onSave={onSave}
            onApply={onApply}
            onView={onView}
            currentPage={currentPage}
            totalJobs={totalJobs}
            pageSize={pageSize}
            onPageChange={onPageChange}
          />
        </div>
      </div>
    </div>
  );
};

export default SearchPage;

// import React from "react";
// import JobSection from "./JobSection";
// import SearchBar from "./SearchBar";
// import SearchPageHeader from "./SearchPageHeader";
// import SearchPageJobSection from "./SearchPageJobSection";

// const SearchPage = ({
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
//     <>
//       <SearchPageHeader />
//       <SearchBar
//         searchQuery={searchQuery}
//         onSearchChange={onSearchChange}
//         filters={filters}
//         onFilterChange={onFilterChange}
//         onFilterSearch={onFilterSearch}
//       />
//       <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-7">
//         <div className="col-span-2">
//           <SearchPageJobSection
//             title={title}
//             jobs={jobs}
//             onSave={onSave}
//             onApply={onApply}
//             onView={onView}
//             currentPage={currentPage}
//             totalJobs={totalJobs}
//             pageSize={pageSize}
//             onPageChange={onPageChange}
//           />
//         </div>
//       </div>
//     </>
//   );
// };

// export default SearchPage;