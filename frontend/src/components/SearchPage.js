import React, { useEffect } from "react";
import SearchBar from "./SearchBar";
import SearchPageHeader from "./SearchPageHeader";
import SearchPageJobSection from "./SearchPageJobSection";
import Header from "./Header";
import { useLocation } from 'react-router-dom';

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
  onClearAll,
  onTechFilter
}) => {
  
  useEffect(() => {
    // Trigger a search when the component mounts or when filters change
    // highlight-next-line
    onFilterSearch(1); // Always start from the first page when filters change
  }, [filters]);

  useEffect(() => {
    // Update filters when specialization changes
    if (specialization) {
      onFilterChange({ target: { name: "specialization", value: specialization } });
    }
  }, [specialization]);


  const location = useLocation();

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const tech = searchParams.get('tech');
    if (tech) {
      onTechFilter(tech);
    }
  }, [location]);


  return (
    <div className="max-w-6xl mx-auto">
      <SearchPageHeader title={title} totalJobs={totalJobs} />
      <SearchBar
        searchQuery={searchQuery}
        onSearchChange={onSearchChange}
        filters={filters}
        onFilterChange={onFilterChange}
        onFilterSearch={onFilterSearch}
        onClearAll={onClearAll}
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
