import React, { useState, useEffect } from "react";
import { toast, Toaster } from "react-hot-toast";

const JobCard = ({ job, onSave, onApply, onView }) => {
  const [isSaved, setIsSaved] = useState(false);

  useEffect(() => {
    checkIfJobIsSaved();
  }, []);

  const checkIfJobIsSaved = async () => {
    try {
      const response = await fetch(`/api/is_job_saved/${job.job_id}`, {
        method: 'GET',
        credentials: 'include',
      });
      const data = await response.json();
      setIsSaved(data.is_saved);
    } catch (error) {
      console.error("Error checking if job is saved:", error);
    }
  };

  const handleSaveToggle = async () => {
    try {
      if (isSaved) {
        // Unsave the job
        await fetch(`/api/unsave_job/${job.job_id}`, {
          method: 'DELETE',
          credentials: 'include',
        });
        setIsSaved(false);
        toast.success("Job Unsaved.");

      } else {
        // Save the job
        await onSave(job.job_id);
        setIsSaved(true);
      }
    } catch (error) {
      console.error("Error toggling job save status:", error);
    }
  };

  return (
    <div className="flex items-center justify-between bg-zinc-50/50 p-4 border-b border-grey-200 mb-2 rounded-lg shadow-md shadow-slate-200/50 cursor-pointer hover:bg-slate-100 hover:shadow-xl">
      <div className="flex items-center">
        <img src={job.logo} alt={job.company} className="w-14 h-14 mr-4" />
        <div>
          <h3
            className="font-bold text-lg flex items-center hover:text-violet-500"
            onClick={() => onView(job.job_id)}
          >
            {job.title}
            {job.created_at === "1 day" && (
              <img
                src="https://remoteok.com/assets/new2x.gif"
                alt="New"
                className="w-8 h-6 ml-3"
              />
            )}
          </h3>
          <div className="flex flex-wrap gap-2 pt-1">
            <span className="bg-fuchsia-50 text-fuchsia-700 px-2 py-1 rounded-lg hover:underline cursor-pointer">
              {job.company}
            </span>
            <span className="text-gray-600 bg-lime-50 text-lime-600 px-2 py-1 rounded-lg">
              {job.city}
            </span>
            <span className="text-gray-600 bg-orange-50 text-orange-700 px-2 py-1 rounded-lg">
              {job.experience_level}
            </span>
            <span className="text-gray-600 bg-cyan-50 text-cyan-800 px-2 py-1 rounded-lg">
              {job.specialization}
            </span>
            {job.salary_range && job.salary_range !== '' && (
              <span className="flex items-center bg-green-50 text-emerald-700 px-2 py-1 rounded-lg">
                {job.salary_range}
              </span>
            )}
            {job.min_experience_years && job.min_experience_years !== '' && (
              <span className="bg-rose-50 text-rose-700 px-2 py-1 rounded-lg">
                {job.min_experience_years}+ Years
              </span>
            )}
            <span className="text-gray-600 bg-purple-50 text-purple-700 px-2 py-1 rounded-lg">
              {job.created_at}
            </span>
          </div>
        </div>
      </div>
      <div className="flex space-x-2">
        <button
          className={`px-4 py-2 border border-gray-300 rounded-md ${
            isSaved
              ? "bg-lime-200 hover:bg-lime-300 text-lime-700"
              : "hover:bg-lime-300"
          }`}
          onClick={handleSaveToggle}
        >
          {isSaved ? "Saved" : "Save"}
        </button>
        <button
          className="px-4 py-2 bg-black hover:bg-violet-700 text-white rounded-md"
          onClick={() => onApply(job.job_id)}
        >
          Apply
        </button>
      </div>
    </div>
  );
};

export default JobCard;



// const JobCard = ({ job, onSave, onApply, onView }) => {
//   return (
//     <div
//       className="flex items-center justify-between bg-zinc-50/50 p-4 border-b border-grey-200 mb-2 rounded-lg shadow-md shadow-slate-200/50 cursor-pointer hover:bg-slate-100 hover:shadow-xl"
//     >
//       <div className="flex items-center">
//         <img src={job.logo} alt={job.company} className="w-14 h-14 mr-4" />
//         <div>
//           <h3
//             className="font-bold text-lg flex items-center hover:text-violet-500"
//             onClick={() => onView(job.job_id)}
//           >
//             {job.title}
//             {job.created_at == "1 day" && (
//               <img
//                 src="https://remoteok.com/assets/new2x.gif"
//                 alt="New"
//                 className="w-8 h-6 ml-3"
//               />
//             )}
//           </h3>
//           <div className="flex flex-wrap gap-2 pt-1">
//             <span className="bg-fuchsia-50 text-fuchsia-700 px-2 py-1 rounded-lg hover:underline cursor-pointer">
//               {job.company}
//             </span>
//             <span className="text-gray-600 bg-lime-50 text-lime-600 px-2 py-1 rounded-lg">
//               {job.city}
//             </span>
//             <span className="text-gray-600 bg-orange-50 text-orange-700 px-2 py-1 rounded-lg">
//               {job.experience_level}
//             </span>
//             <span className="text-gray-600 bg-cyan-50 text-cyan-800 px-2 py-1 rounded-lg">
//               {job.specialization}
//             </span>
//             {job.salary_range && job.salary_range !== '' && (
//               <span className="flex items-center bg-green-50 text-emerald-700 px-2 py-1 rounded-lg">
//                 {/* <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-2 mr-1" viewBox="0 0 20 20" fill="currentColor">
//                   <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
//                 </svg> */}
//                 {job.salary_range}
//               </span>
//             )}
//             {job.min_experience_years && job.min_experience_years !== '' && (
//               <span className="bg-rose-50 text-rose-700 px-2 py-1 rounded-lg">
//                 {job.min_experience_years}+ Years
//               </span>
//             )}
//             <span className="text-gray-600 bg-purple-50 text-purple-700 px-2 py-1 rounded-lg">
//               {job.created_at}
//             </span>
//           </div>
//         </div>
//       </div>
//       <div className="flex space-x-2">
//         <button
//           className="px-4 py-2 border border-gray-300 hover:bg-lime-300 rounded-md"
//           onClick={() => onSave(job.job_id)}
//         >
//           Save
//         </button>
//         <button
//           className="px-4 py-2 bg-black hover:bg-violet-700 text-white rounded-md"
//           onClick={() => onApply(job.job_id)}
//         >
//           Apply
//         </button>
//       </div>
//     </div>
//   );
// };

// export default JobCard;