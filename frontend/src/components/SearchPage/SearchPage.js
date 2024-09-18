import React, { useEffect, useRef, useState } from "react";
import SearchPageBar from "./SearchPageBar";
import SearchPageHeader from "./SearchPageHeader";
import SearchPageJobSection from "./SearchPageJobSection";
import { useLocation } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';

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
  const location = useLocation();
  // Create a ref to track if the initial fetch has been done
  const initialFetchDone = useRef(false);
  const [isSearchPerformed, setIsSearchPerformed] = useState(false);

  useEffect(() => {
    // Only run this effect if the initial fetch hasn't been done
    if (!initialFetchDone.current) {
      const searchParams = new URLSearchParams(location.search);
      const tech = searchParams.get('tech');
      
      // Check for tech parameter in URL
      if (tech) {
        onTechFilter(tech);
      } 
      // Check for specialization prop
      else if (specialization) {
        onFilterChange({ target: { name: "specialization", value: specialization } });
        onFilterSearch(1);
      } 
      // If no tech or specialization, and no jobs, fetch all jobs
      else if (!jobs || jobs.length === 0) {
        onFilterSearch(1);
      }
      
      // Mark initial fetch as done
      initialFetchDone.current = true;
    }
  }, [location, specialization, jobs, onTechFilter, onFilterChange, onFilterSearch]);

  const handleFilterSearch = (page) => {
    setIsSearchPerformed(true);
    onFilterSearch(page);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <nav className="flex items-center text-sm text-gray-500 mb-4 space-x-1">
        <Link to="/" className="hover:text-gray-700">OceaniaDevs</Link>
        <ChevronRight size={16} className="mx-2" />
        <span className="text-gray-700">Search Jobs</span>
      </nav>
      <SearchPageHeader title={title} totalJobs={totalJobs} />
      <SearchPageBar
        searchQuery={searchQuery}
        onSearchChange={onSearchChange}
        filters={filters}
        onFilterChange={(e) => {
          onFilterChange(e);
          setIsSearchPerformed(false);
        }}
        onFilterSearch={() => handleFilterSearch(1)}
        onClearAll={() => {
          onClearAll();
          setIsSearchPerformed(false);
        }}
      />
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-7">
        <div className="col-span-2">
          <SearchPageJobSection
            jobs={jobs}
            onSave={onSave}
            onApply={onApply}
            onView={onView}
            currentPage={currentPage}
            totalJobs={totalJobs}
            pageSize={pageSize}
            onPageChange={handleFilterSearch}
            isInSession={isInSession}
            filters={filters}
            searchQuery={searchQuery}
            isSearchPerformed={isSearchPerformed}
          />
        </div>
      </div>
    </div>
  );
};

export default SearchPage;