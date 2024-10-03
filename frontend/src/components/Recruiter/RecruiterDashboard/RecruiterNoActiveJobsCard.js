import React from 'react';
import { Link } from 'react-router-dom';

const RecruiterNoActiveJobsCard = () => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-8 text-center" style={{ fontFamily: 'Avenir, sans-serif' }}>
      <h2 className="text-2xl font-bold mb-4 text-gray-800">No Active Job Postings</h2>
      <p className="text-gray-600 mb-6">Ready to find your next great hire? Create a new job posting to get started!</p>
      <div className="flex justify-center space-x-4">
        <Link to="/employer/post-job" className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded transition duration-300">
          Post a Job
        </Link>
        <Link to="/employer/post-job-ai" className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded transition duration-300">
          Post with AI
        </Link>
      </div>
    </div>
  );
};

export default RecruiterNoActiveJobsCard;