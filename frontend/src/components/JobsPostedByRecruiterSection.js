import React from "react";
import JobsPostedByRecruiterCard from "../components/JobsPostedByRecruiterCard";
import SavedAndAppliedJobsHeader from "../components/SavedAppliedJobsHeader";

const JobsPostedByRecruiterSection = ({
  title,
  jobs,
  onEdit,
  onView,
  onRemove,
}) => {
  return (
    <div className="mb-10">
      <SavedAndAppliedJobsHeader title={title} />
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-5xl font-bold"></h2>
      </div>
      <div className="bg-white rounded-lg shadow-md">
        {jobs.map((job, index) => (
          <JobsPostedByRecruiterCard
            key={index}
            job={job}
            onEdit={onEdit}
            onView={onView}
            onRemove={onRemove}
          />
        ))}
      </div>
    </div>
  );
};

export default JobsPostedByRecruiterSection;
