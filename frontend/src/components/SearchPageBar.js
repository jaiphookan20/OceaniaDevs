import React, { useState } from "react";
import { Search, ChevronDown } from "lucide-react";
import JobSection from "./JobSection";
import searchIcon from "../assets/search-icon.png";

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
}) => {
  const [header, setHeader] = useState("Remote jobs");
  const [jobSearch, setJobSearch] = useState("");
  const [locationSearch, setLocationSearch] = useState("");

  const handleSearch = (e) => {
    e.preventDefault();
    if (jobSearch.trim()) {
      setHeader(jobSearch.trim());
    } else {
      setHeader("Remote jobs!");
    }
  };

  return (
    <>
      <div
        className="max-w-6xl mx-auto pt-16 pl-12 pr-12 pb-10 bg-lime-50"
        style={{ fontFamily: "Roobert-Regular, sans-serif" }}
      >
        <div className="display-flex">
          <div>
            <h1 className="text-6xl font-bold text-gray-800 mb-2">{header}</h1>
            <p className="text-lg text-gray-600 mb-8">
              Discover the best remote and work from home jobs at top remote
              companies.
            </p>
          </div>
        </div>

        <form
          onSubmit={handleSearch}
          className="flex flex-col sm:flex-row gap-4 mb-6"
        >
          <div className="relative flex-1">
            <Search
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              size={20}
            />
            <input
              type="text"
              placeholder="Job title or skill"
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent"
              value={jobSearch}
              onChange={(e) => setJobSearch(e.target.value)}
            />
            <ChevronDown
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              size={20}
            />
          </div>
          <div className="relative flex-1">
            <Search
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              size={20}
            />
            <input
              type="text"
              placeholder="Country or timezone"
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent"
              value={locationSearch}
              onChange={(e) => setLocationSearch(e.target.value)}
            />
            <ChevronDown
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              size={20}
            />
          </div>
          <button
            type="submit"
            className="bg-purple-600 text-white py-3 px-6 rounded-md hover:bg-purple-700 transition duration-300 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:ring-opacity-50"
          >
            Search
          </button>
        </form>

        <div className="flex flex-wrap gap-3">
          {[
            "Experience level",
            "Salary range",
            "Companies",
            "Job type",
            "Employee benefits",
            "Markets",
          ].map((filter) => (
            <button
              key={filter}
              className="px-4 py-2 border border-lime-400 bg-slate-700 rounded-md text-white hover:bg-gray-50 transition duration-300 focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            >
              {filter} <ChevronDown className="inline ml-1" size={16} />
            </button>
          ))}
        </div>
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
