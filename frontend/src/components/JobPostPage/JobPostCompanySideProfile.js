import React from 'react';
import { useNavigate } from "react-router-dom";

const JobPostCompanySideProfile = ({ job }) => {

    const navigate = useNavigate();

  return (
    <div className="mt-5 w-full bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden font-sans">
      <div className="bg-violet-600 text-white py-1 px-3 font-semibold text-sm text-center" style={{fontFamily: "Roobert-Regular, san-serif"}}>
        Claim this profile
      </div>
      <div className="p-4">
        <div className="mb-4">
          <img src={job.logo} alt="logo" className="w-10 h-10 mr-3" />
          <h2 className="mt-2 text-lg font-semibold text-gray-800">{job.company}</h2>
        </div>
        
        <div className="mb-3">
          <h3 className="text-sm text-gray-500" style={{fontFamily: "Roobert-Regular, san-serif"}}>Company size</h3>
          <p className="text-sm font-medium text-gray-700 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
            </svg>
            1001-5000
          </p>
        </div>
        <div className="mb-3">
          <h3 className="text-sm text-gray-500" style={{fontFamily: "Roobert-Regular, san-serif"}}>Industry</h3>
          <p className="text-sm font-medium text-gray-700">IT-Software Development</p>
        </div>
        <div className="mb-3">
          <h3 className="text-sm text-gray-500">HQ</h3>
          <p className="text-sm font-medium text-gray-700">Sydney, NSW</p>
        </div>
        <button className="mt-5 w-full bg-black hover:bg-violet-700 text-white font-md py-1 px-3 rounded" style={{fontFamily: "Roobert-Regular, san-serif"}}
        onClick={()=>navigate(`/company/${job.company_id}`)}
        >
          View company profile
        </button>
      </div>
    </div>
  );
};

export default JobPostCompanySideProfile;