import React from 'react';
import { Link } from 'react-router-dom';

const RecruiterOnboardingIncompleteCard = () => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-8 text-center" style={{ fontFamily: 'Avenir, sans-serif' }}>
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Onboarding Incomplete!</h2>
      <p className="text-gray-600 mb-6">Please complete your onboarding process to start posting jobs.</p>
      <Link to="/employer/new/organization-details" className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded transition duration-300">
        Complete Onboarding
      </Link>
    </div>
  );
};

export default RecruiterOnboardingIncompleteCard;