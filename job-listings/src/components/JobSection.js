import React from "react";
import JobCard from "./JobCard";

const JobSection = ({ title, jobs, onSave, onApply, onView }) => {
  return (
    <div>
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
    </div>
  );
};

export default JobSection;
