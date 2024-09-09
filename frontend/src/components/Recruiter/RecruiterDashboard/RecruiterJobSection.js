import React, { useState } from 'react';
import RecruiterJobCard from './RecruiterJobCard';
import RecruiterDashboardHeader from './RecruiterDashboardHeader';

const RecruiterJobSection = ({ title, activeJobs, expiredJobs, onEdit, onView, onRemove }) => {
  const [activeTab, setActiveTab] = useState('active');

  return (
    <div className="mb-10">
      <RecruiterDashboardHeader title={title} />
      <div className="flex justify-start items-center mb-4 space-x-4">
        <button
          className={`px-4 py-2 rounded-lg ${
            activeTab === 'active' ? 'bg-teal-600 text-white' : 'bg-gray-200 text-gray-700'
          }`}
          onClick={() => setActiveTab('active')}
        >
          Active Jobs ({activeJobs.length})
        </button>
        <button
          className={`px-4 py-2 rounded-lg ${
            activeTab === 'expired' ? 'bg-teal-600 text-white' : 'bg-gray-200 text-gray-700'
          }`}
          onClick={() => setActiveTab('expired')}
        >
          Expired Jobs ({expiredJobs.length})
        </button>
      </div>
      <div className="bg-white rounded-lg shadow-md">
        {activeTab === 'active' &&
          activeJobs.map((job, index) => (
            <RecruiterJobCard
              key={index}
              job={job}
              onEdit={onEdit}
              onView={onView}
              onRemove={onRemove}
            />
          ))}
        {activeTab === 'expired' &&
          expiredJobs.map((job, index) => (
            <RecruiterJobCard
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

export default RecruiterJobSection;