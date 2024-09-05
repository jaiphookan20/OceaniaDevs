import React from "react";
import { useNavigate } from "react-router-dom";
import CompanyJobCard from "./CompanyJobCard";

const CompanyJobSection = ({ title, jobs, onSave, onApply, onView, company }) => {
  const navigate = useNavigate();

  return (
    <div className="mx-auto max-w-6xl mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-bold pl-4">{title}</h2>
      </div>
      <div className="bg-white rounded-lg shadow-md">
        {jobs.map((job, index) => (
          <CompanyJobCard
            key={index}
            job={job}
            onSave={onSave}
            company={company}
            onApply={onApply}
            onView={onView}
          />
        ))}
      </div>
    </div>
  );
};

export default CompanyJobSection;