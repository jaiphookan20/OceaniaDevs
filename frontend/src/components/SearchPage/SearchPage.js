import React, { useEffect, useRef, useState } from "react";
import SearchPageBar from "./SearchPageBar";
import SearchPageHeader from "./SearchPageHeader";
import SearchPageJobSection from "./SearchPageJobSection";
import { useLocation, useNavigate } from 'react-router-dom';
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
  onTechFilter,
  userJobStatuses,
  onUnsave
}) => {
  const location = useLocation();
  const navigate = useNavigate();
  // Create a ref to track if the initial fetch has been done
  const initialFetchDone = useRef(false);
  const [isSearchPerformed, setIsSearchPerformed] = useState(false);

  useEffect(() => {
    if (!initialFetchDone.current) {
      const searchParams = new URLSearchParams(location.search);
      const newFilters = { ...filters };
      let newQuery = null;
      let hasChanges = false;

      ['specialization', 'experience_level', 'work_location', 'city', 'job_arrangement'].forEach(param => {
        const value = searchParams.get(param);
        if (value) {
          newFilters[param] = value;
          hasChanges = true;
        }
      });

      const tech = searchParams.get('tech_stack');
      if (tech) {
        newFilters.tech_stack = [tech];
        hasChanges = true;
      }

      newQuery = searchParams.get('query');
      if (newQuery) {
        hasChanges = true;
      }

      if (hasChanges) {
        onFilterSearch(1, newFilters, newQuery);
      } else if (!jobs || jobs.length === 0) {
        onFilterSearch(1);
      }

      initialFetchDone.current = true;
    }
  }, [location, onFilterSearch]);

  const handleFilterSearch = (page) => {
    setIsSearchPerformed(true);
    const searchParams = new URLSearchParams();

    // Add filters to URL
    Object.entries(filters).forEach(([key, value]) => {
      if (value && value !== '') {
        if (Array.isArray(value)) {
          value.forEach(v => searchParams.append(key, v));
        } else {
          searchParams.set(key, value);
        }
      }
    });

    // Add search query to URL
    if (searchQuery) {
      searchParams.set('query', searchQuery);
    }

    // Add page number to URL if not the first page
    if (page > 1) {
      searchParams.set('page', page);
    }

    // Update URL
    navigate(`/search-page?${searchParams.toString()}`);

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
          navigate('/search-page'); // Clear URL parameters
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
            userJobStatuses={userJobStatuses}
            onUnsave={onUnsave}
          />
        </div>
      </div>
    </div>
  );
};

export default SearchPage;