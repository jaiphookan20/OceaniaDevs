import React from "react";
import JobCard from "../JobCard";

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
  searchQuery
}) => {
  if (!jobs || jobs.length === 0) {
    return (
      <div className="mx-auto max-w-6xl">
        <h2 className="text-3xl font-bold mb-4">No Jobs Found</h2>
        <p>Try adjusting your search criteria or clearing filters.</p>
      </div>
    );
  }

  const totalPages = Math.ceil(totalJobs / pageSize);

  /* Title Slug */
  const getFilterSummary = () => {
    if (searchQuery && searchQuery.trim() !== "") {
      return `Displaying jobs matching "${searchQuery}"`;
    }

    const parts = [];
    if (filters.specialization) parts.push(filters.specialization);
    if (filters.salary_range) parts.push(`$${filters.salary_range}`);
    if (filters.tech_stack && filters.tech_stack.length > 0) {
      parts.push(filters.tech_stack.join(', '));
    }
    
    // if (parts.length === 0) return `${totalJobs} Jobs Found`;
    if (parts.length === 0) return `Displaying All Jobs`;
    
    let summary = parts.join(' • ');
    summary = "Displaying Jobs: " + summary;
    return summary.length > 60 ? summary.substring(0, 47) + '...' : summary;
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