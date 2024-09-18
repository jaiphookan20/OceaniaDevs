import React from "react";
import JobCard from "../HomePage/JobCard";
import HashLoader from "react-spinners/HashLoader";

const SearchPageJobSection = ({
  jobs,
  onSave,
  onApply,
  onView,
  currentPage,
  totalJobs,
  pageSize,
  onPageChange,
  isInSession,
  filters,
  searchQuery,
  isSearchPerformed // New prop to indicate if search has been performed
}) => {
  if (!jobs) {
    return (
      <div className="flex justify-center items-center h-64">
        <HashLoader color="#8823cf" size={50} />
      </div>
    );
  }

  else if (jobs.length === 0) {
    return (
      <div className="mx-auto max-w-6xl" style={{fontFamily: "Avenir"}}>
        <h2 className="text-3xl font-bold text-slate-600 mb-4">Whoops, No Jobs Found for your search</h2>
        <p>Try adjusting your search criteria or clearing filters.</p>
      </div>
    );
  }

  const totalPages = Math.ceil(totalJobs / pageSize);

  /* Title Slug */
  const getFilterSummary = () => {
    if (searchQuery && searchQuery.trim() !== "") {
      return (
        <span>
          Displaying jobs matching "
          <span className="text-purple-600 font-medium">{searchQuery}</span>"
        </span>
      );
    }

    const parts = [];
    if (filters.specialization) parts.push(filters.specialization);
    if (filters.experience_level) parts.push(filters.experience_level);
    if (filters.work_location) parts.push(filters.work_location);
    if (filters.job_arrangement) parts.push(filters.job_arrangement);
    if (filters.city) parts.push(filters.city);
    if (filters.tech_stack && filters.tech_stack.length > 0) {
      parts.push(filters.tech_stack[0]);
    }
    
    if (parts.length === 0) return "Displaying All Jobs";
    
    const highlightedParts = parts.map((part, index) => (
      <React.Fragment key={index}>
        {index > 0 && " • "}
        <span className="text-teal-600 font-medium">{part}</span>
      </React.Fragment>
    ));

    let summary;
    if (isSearchPerformed) {
      summary = <span>Displaying Jobs: {highlightedParts}</span>;
    } else {
      summary = <span>Selected: {highlightedParts}</span>;
    }

    return summary;
  };

  return (
    <div className="mx-auto max-w-6xl">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-medium text-slate-600">
          {getFilterSummary()}
        </h2>
        <h2 className="text-2xl font-medium">
          {totalJobs} Jobs Found
        </h2>
      </div>
      <div className="bg-white rounded-lg shadow-md">
        {jobs.map((job) => (
          <JobCard
            key={job.job_id}
            job={job}
            onSave={onSave}
            onApply={onApply}
            onView={onView}
            isInSession={isInSession}
          />
        ))}
      </div>
      <div className="flex justify-between items-center mt-4 mb-14">
        <button
          disabled={currentPage === 1}
          onClick={() => onPageChange(currentPage - 1)}
          className="px-4 py-2 bg-black text-white rounded disabled:bg-gray-300"
        >
          Previous
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button
          disabled={currentPage === totalPages}
          onClick={() => onPageChange(currentPage + 1)}
          className="px-4 py-2 bg-black text-white rounded disabled:bg-gray-300"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default SearchPageJobSection;