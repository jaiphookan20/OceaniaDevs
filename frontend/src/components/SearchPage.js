// import React from "react";
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
//   onFilterSearch,
//   isInSession
// }) => {
//   return (
//     <div className="max-w-6xl mx-auto">
//       <SearchPageHeader title={title} />
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
//             onSave={onSave}
//             onApply={onApply}
//             onView={onView}
//             currentPage={currentPage}
//             totalJobs={totalJobs}
//             pageSize={pageSize}
//             onPageChange={onPageChange}
//             isInSession={isInSession}
//           />
//         </div>
//       </div>
//     </div>
//   );
// };

// export default SearchPage;

import React, { useEffect } from "react";
import SearchBar from "./SearchBar";
import SearchPageHeader from "./SearchPageHeader";
import SearchPageJobSection from "./SearchPageJobSection";
import Header from "./Header";


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
  onFilterSearch,
  isInSession,
  specialization,
  onClearAll
}) => {
  useEffect(() => {
    // Trigger a search when the component mounts or when filters change
    onFilterSearch();
  }, [filters]);

  useEffect(() => {
    // Update filters when specialization changes
    if (specialization) {
      onFilterChange({ target: { name: "specialization", value: specialization } });
    }
  }, [specialization]);

  return (
    <div className="max-w-6xl mx-auto">
      <SearchPageHeader title={title} />
      <SearchBar
        searchQuery={searchQuery}
        onSearchChange={onSearchChange}
        filters={filters}
        onFilterChange={onFilterChange}
        onFilterSearch={onFilterSearch}
        onClearAll={onClearAll}  // Pass the new onClearAll prop
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
            isInSession={isInSession}
          />
        </div>
      </div>
    </div>
  );
};

export default SearchPage;
