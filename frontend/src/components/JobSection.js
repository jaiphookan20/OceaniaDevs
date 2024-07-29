import React from "react";
import JobCard from "./JobCard";

const JobSection = ({
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
  return (
    <div className="mx-auto max-w-6xl">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-bold">{title}</h2>
        <a href="#" className="text-indigo-600">
          View all {title.toLowerCase()}
        </a>
      </div>
      <div className="bg-white rounded-lg shadow-md">
        {jobs.map((job, index) => (
          <JobCard
            key={index}
            job={job}
            onSave={onSave}
            onApply={onApply}
            onView={onView}
          />
        ))}
      </div>
      <div className="flex justify-between items-center mt-4 mb-14">
        <button
          disabled={currentPage === 1}
          onClick={() => onPageChange(currentPage - 1)}
          className="px-4 py-2 bg-black text-white rounded"
        >
          Previous
        </button>
        <span>
          Page {currentPage} of {Math.ceil(totalJobs / pageSize)}
        </span>
        <button
          disabled={currentPage === Math.ceil(totalJobs / pageSize)}
          onClick={() => onPageChange(currentPage + 1)}
          className="px-4 py-2 bg-black text-white rounded"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default JobSection;
