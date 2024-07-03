import React from "react";
import SavedAndAppliedJobsCard from "../components/SavedAndAppliedJobsCard";
import SavedAndAppliedJobsHeader from "../components/SavedAppliedJobsHeader";

const SavedAppliedJobSection = ({
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
    <div>
      <SavedAndAppliedJobsHeader title={title} />
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-5xl font-bold"></h2>
        <a href="#" className="text-indigo-600">
          View all {title.toLowerCase()}
        </a>
      </div>
      <div className="bg-white rounded-lg shadow-md">
        {jobs.map((job, index) => (
          <SavedAndAppliedJobsCard
            key={index}
            job={job}
            onApply={onApply}
            onSave={onSave}
            onView={onView}
          />
        ))}
      </div>
      {currentPage && totalJobs && pageSize && onPageChange && (
        <div className="flex justify-center mt-4">
          <button
            className="px-4 py-2 mx-1 bg-gray-200 rounded"
            disabled={currentPage === 1}
            onClick={() => onPageChange(currentPage - 1)}
          >
            Previous
          </button>
          <button
            className="px-4 py-2 mx-1 bg-gray-200 rounded"
            disabled={currentPage === Math.ceil(totalJobs / pageSize)}
            onClick={() => onPageChange(currentPage + 1)}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default SavedAppliedJobSection;
