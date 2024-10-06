import React from "react";
import { useNavigate } from "react-router-dom";
import JobCard from "../HomePage/JobCard";

const JobSection = ({ title, jobs, onSave, onApply, onView, company, isInSession, onViewAll, userData, userJobStatuses, onUnsave }) => {
  const navigate = useNavigate();

  return (
    <div className="mx-auto max-w-6xl mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-semibold pl-4 text-slate-600">{title}</h2>
        <button 
          // onClick={handleViewAll}
          onClick={onViewAll}
          className="text-teal-600 font-semibold hover:text-indigo-700 hover:underline hover:font-semibold"
          style={{fontFamily: "Avenir, san-serif"}}
        >
          View all {title}
        </button>
      </div>
      <div className="bg-white rounded-lg shadow-md">
        {jobs.map((job, index) => (
          <JobCard
            key={index}
            job={job}
            onSave={onSave}
            company={company}
            onApply={onApply}
            onView={onView}
            isInSession={isInSession}
            userData={userData}
            userJobStatuses={userJobStatuses}
            onUnsave={onUnsave}
          />
        ))}
      </div>
    </div>
  );
};

export default JobSection;