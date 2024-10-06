import React, { useState } from "react";
import RecruiterJobCard from "./RecruiterJobCard";
import RecruiterNoActiveJobsCard from "./RecruiterNoActiveJobsCard";

const RecruiterJobSection = ({ activeJobs, expiredJobs, onEdit, onView, onRemove }) => {
  const [showActive, setShowActive] = useState(true);

  return (
    <div>
      <div className="flex justify-start mb-4">
        <button
          className={`mr-4 px-4 py-2 rounded ${
            showActive ? "bg-purple-600 text-white" : "bg-gray-200 text-gray-700"
          }`}
          onClick={() => setShowActive(true)}
        >
          Active Jobs ({activeJobs.length})
        </button>
        <button
          className={`px-4 py-2 rounded ${
            !showActive ? "bg-purple-600 text-white" : "bg-gray-200 text-gray-700"
          }`}
          onClick={() => setShowActive(false)}
        >
          Expired Jobs ({expiredJobs.length})
        </button>
      </div>

      {showActive ? (
        activeJobs.length > 0 ? (
          activeJobs.map((job) => (
            <RecruiterJobCard
              key={job.job_id}
              job={job}
              onEdit={() => onEdit(job.job_id)}
              onView={() => onView(job.job_id)}
              onRemove={() => onRemove(job.job_id)}
            />
          ))
        ) : (
          <RecruiterNoActiveJobsCard />
        )
      ) : (
        expiredJobs.map((job) => (
          <RecruiterJobCard
            key={job.job_id}
            job={job}
            onEdit={() => onEdit(job.job_id)}
            onView={() => onView(job.job_id)}
            onRemove={() => onRemove(job.job_id)}
          />
        ))
      )}
    </div>
  );
};

export default RecruiterJobSection;