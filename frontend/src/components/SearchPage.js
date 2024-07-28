import React, { useState } from "react";
import { Search, ChevronDown } from "lucide-react";
import JobSection from "./JobSection";
import Header from "./Header";
import SearchPageHeader from "./SearchPageHeader";
import SearchBar from "./SearchBar";
import SearchBarTest from "./SearchBarTest";

const SearchPageBar = ({
  title,
  jobs,
  onSave,
  onApply,
  onView,
  currentPage,
  totalJobs,
  pageSize,
  onPageChange,
  searchQuery={searchQuery},
  onSearchChange={handleSearch},
  filters={filters},
  onFilterChange={handleChange},
  onFilterSearch={handleFilterSearch}
}) => {
  const [header, setHeader] = useState("Remote jobs");
  const [jobSearch, setJobSearch] = useState("");
  const [locationSearch, setLocationSearch] = useState("");

  const handleSearch = (e) => {
    e.preventDefault();
    if (jobSearch.trim()) {
      setHeader(jobSearch.trim());
    } else {
      setHeader("Software jobs!");
    }
  };

  return (
    <>
      <div
        className="max-w-8xl mx-auto p-4"
        style={{ fontFamily: "Roobert-Regular, sans-serif" }}
      >
        {/* <SearchPageHeader /> */}
        <SearchBarTest />
      </div>
      <JobSection
        title={title}
        jobs={jobs}
        onSave={onSave}
        onApply={onApply}
        onView={onView}
        currentPage={currentPage}
        totalJobs={totalJobs}
        pageSize={pageSize}
        onPageChange={onPageChange}
      />
    </>
  );
};

export default SearchPageBar;

