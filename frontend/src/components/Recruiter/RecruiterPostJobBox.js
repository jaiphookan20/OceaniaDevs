import React from 'react';

const RecruiterPostJobBox = () => {
  return (
    <div className="w-1/3 mx-auto px-4 sm:px-6 lg:px-8">
      <div className="bg-white border-2 border-teal-500 p-6 rounded-lg shadow-md flex flex-col items-center" style={{fontFamily: "HeyWow"}}>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Single Job Ad</h2>
        <h3 className="text-4xl font-bold text-teal-500 mb-4">AUD $200</h3>
        <p className="text-gray-600 mb-4 text-center text-xl">
          Live for 30 days
        </p>
        <ul className="text-gray-600 mb-4">
          <li >✔️ Live for 30 days</li>
          <li>✔️ Many job searchers</li>
          <li>✔️ Edit your post anytime</li>
          <li>✔️ Company logo included</li>
          <li>✔️ Analytics</li>
        </ul>
        <button className="px-6 py-2 bg-green-300 text-green-700 rounded-md border-green-700">
          Create Job
        </button>
      </div>
    </div>
  );
};

export default RecruiterPostJobBox;