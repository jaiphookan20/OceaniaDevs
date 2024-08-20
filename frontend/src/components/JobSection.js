import React from "react";
import { useNavigate } from "react-router-dom";
import JobCard from "./JobCard";

const JobSection = ({ title, jobs, onSave, onApply, onView, company, isInSession, onViewAll }) => {
  const navigate = useNavigate();

/* We added a handleViewAll function that extracts the specialization from the title and navigates to the search page with the specialization as a query parameter.
   We changed the "View all" link to a button that calls this function when clicked.
   We updated the route to /search-page to match your existing route structure. */
  const handleViewAll = () => {
    const specialization = title.replace(" Roles", "");
    navigate(`/search-page?specialization=${encodeURIComponent(specialization)}`);
  };

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
          />
        ))}
      </div>
    </div>
  );
};

export default JobSection;