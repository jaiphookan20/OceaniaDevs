import React from 'react';
import { useNavigate } from "react-router-dom";

const RecommendedJobCard = ({ job }) => {

  const navigate = useNavigate();

  return (
    <div className="bg-white rounded-lg shadow-lg border border-slate-300 p-4" >
    <div className="flex items-center justify-between mb-2">
      <img src={job.logo_url} alt={job.company_name} className="w-10 h-10 rounded" />
      <span className="text-xs text-teal-700 bg-teal-100 border border-teal-300 px-2 py-1 rounded-full">
        {job.location}
      </span>
    </div>
    <h3 className="font-semibold text-slate-600 text-lg mb-1 hover:cursor-pointer hover:text-black" onClick={()=>navigate(`/job_post/${job.job_id}`)}>{job.title}</h3>
    <p className="text-sm text-gray-600 mb-2 hover:underline hover:cursor-pointer" onClick={()=>navigate(`/company/${job.company_id}`)}>{job.company_name}</p>
    {job.salary_range && (
      <div className="flex items-center text-sm text-gray-500 mb-2">
        {/* <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-2 mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
        </svg> */}
        {job.created_at}
      </div>
    )}
    <div className="flex items-center">
      <span className="bg-amber-100 text-amber-800 text-xs font-medium px-2.5 py-0.5 rounded mr-2">
        {job.experience_level}
      </span>
      {/* <span className="bg-lime-100 text-lime-800 text-xs font-medium px-2.5 py-0.5 rounded">
        {job.created_at} ago
      </span> */}
      <span className="ml-2 bg-rose-100 text-rose-800 text-xs font-medium px-2.5 py-0.5 rounded">
        {job.specialization}
      </span>
        {/* {job.min_experience_years && job.min_experience_years !== '' || job.min_experience_years == 0 && (
         <span className="ml-2 bg-lime-100 text-lime-800 text-xs font-medium px-2.5 py-0.5 rounded">
         {job.min_experience_years}+ Years
       </span>
        )} */}
        {/* {job.salary_range && job.salary_range !== 'Not Listed' && (
         <span className="ml-2 bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">
         ${job.salary_range}
       </span>
        )} */}

    </div>
  </div>
  )

}

const RecommendedJobs = ({ jobs }) => {

  return (
    <div className="max-w-6xl mx-auto px-4 py-24 mt-10 bg-teal-50 border-t" style={{fontFamily: "Avenir, san-serif"}}>
      <div className="flex justify-between items-center mb-4 mb-16">
        <div>
          <h2 className="text-2xl font-bold mb-1">Similar Jobs</h2>
          <p className="text-gray-600">Here are other jobs you might want to apply for.</p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {jobs.length > 0 && jobs.map((job) => (
          <RecommendedJobCard key={job.job_id} job={job} />
        ))}
      </div>
    </div>
  );
};

export default RecommendedJobs;