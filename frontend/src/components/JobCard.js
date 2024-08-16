import React, { useState, useEffect } from "react";
import { toast } from "react-hot-toast";
import LoginModal from "./LoginModal";
import NotificationPopup from "./NotificationPopup";

const JobCard = ({ job, onSave, onApply, onView, isInSession }) => {
  const [isSaved, setIsSaved] = useState(false);
  const [isApplied, setIsApplied] = useState(false);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

  useEffect(() => {
    if (isInSession) {
      checkIfJobIsSaved();
      checkIfJobIsApplied();
    }
  }, [isInSession, job.job_id]);

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

  const checkIfJobIsApplied = async () => {
    try {
      const response = await fetch(`/api/is_job_applied/${job.job_id}`, {
        method: 'GET',
        credentials: 'include',
      });
      const data = await response.json();
      setIsApplied(data.is_applied);
    } catch (error) {
      console.error("Error checking if job is applied:", error);
    }
  };

  const handleSaveToggle = async () => {
    if (!isInSession) {
      setIsLoginModalOpen(true);
      return;
    }

    try {
      if (isSaved) {
        await fetch(`/api/unsave_job/${job.job_id}`, {
          method: 'DELETE',
          credentials: 'include',
        });
        setIsSaved(false);
        toast.success("Job Unsaved.");
      } else {
        await onSave(job.job_id);
        setIsSaved(true);
        toast.success("Job Saved.");
      }
    } catch (error) {
      console.error("Error toggling job save status:", error);
      toast.error("Failed to save/unsave job.");
    }
  };

  const handleApply = async () => {
    if (!isInSession) {
      setIsLoginModalOpen(true);
      return;
    }

    try {
      await onApply(job.job_id);
      setIsApplied(true);
      toast.success("Application submitted successfully!");
    } catch (error) {
      console.error("Error applying to job:", error);
      toast.error("Failed to apply to job.");
    }
  };


  return (
    <>
      <div className="flex items-center justify-between bg-zinc-50/50 p-4 border-b border-grey-200 mb-2 rounded-lg shadow-md shadow-slate-200/50 cursor-pointer hover:bg-slate-100 hover:shadow-xl">
        <div className="flex items-center">
          <img src={job.logo} alt={job.company} className="w-14 h-14 mr-4" />
          <div>
            <h3
              className="font-bold text-lg flex items-center hover:text-violet-500 text-slate-800"
              style={{fontFamily: "Avenir, san-serif"}}
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
            className={`px-4 py-2 rounded-md ${
              isApplied
                ? "bg-green-600 text-white cursor-not-allowed"
                : "bg-black hover:bg-violet-700 text-white"
            }`}
            onClick={handleApply}
            disabled={isApplied}
          >
            {isApplied ? "Applied" : "Apply"}
          </button>
        </div>
      </div>
      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
      />
    </>
  );
};

export default JobCard;



// import React, { useState, useEffect } from "react";
// import { toast } from "react-hot-toast";
// import LoginModal from "./LoginModal"; // Make sure to import the LoginModal component

// const JobCard = ({ job, onSave, onApply, onView, isInSession }) => {
//   const [isSaved, setIsSaved] = useState(false);
//   const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

//   useEffect(() => {
//     if (isInSession) {
//       checkIfJobIsSaved();
//     }
//   }, [isInSession, job.job_id]);

//   const checkIfJobIsSaved = async () => {
//     try {
//       const response = await fetch(`/api/is_job_saved/${job.job_id}`, {
//         method: 'GET',
//         credentials: 'include',
//       });
//       const data = await response.json();
//       setIsSaved(data.is_saved);
//     } catch (error) {
//       console.error("Error checking if job is saved:", error);
//     }
//   };

//   const handleSaveToggle = async () => {
//     if (!isInSession) {
//       setIsLoginModalOpen(true);
//       return;
//     }

//     try {
//       if (isSaved) {
//         await fetch(`/api/unsave_job/${job.job_id}`, {
//           method: 'DELETE',
//           credentials: 'include',
//         });
//         setIsSaved(false);
//         toast.success("Job Unsaved.");
//       } else {
//         await onSave(job.job_id);
//         setIsSaved(true);
//       }
//     } catch (error) {
//       console.error("Error toggling job save status:", error);
//     }
//   };

//   const handleApply = () => {
//     if (!isInSession) {
//       setIsLoginModalOpen(true);
//       return;
//     }
//     onApply(job.job_id);
//   };

//   return (
//     <>
//       <div className="flex items-center justify-between bg-zinc-50/50 p-4 border-b border-grey-200 mb-2 rounded-lg shadow-md shadow-slate-200/50 cursor-pointer hover:bg-slate-100 hover:shadow-xl">
//         <div className="flex items-center">
//           <img src={job.logo} alt={job.company} className="w-14 h-14 mr-4" />
//           <div>
//             <h3
//               className="font-bold text-lg flex items-center hover:text-violet-500 text-slate-800" style={{fontFamily: "Avenir, san-serif"}}
//               onClick={() => onView(job.job_id)}
//             >
//               {job.title}
//               {job.created_at === "1 day" && (
//                 <img
//                   src="https://remoteok.com/assets/new2x.gif"
//                   alt="New"
//                   className="w-8 h-6 ml-3"
//                 />
//               )}
//             </h3>
//             <div className="flex flex-wrap gap-2 pt-1">
//               <span className="bg-fuchsia-50 text-fuchsia-700 px-2 py-1 rounded-lg hover:underline cursor-pointer">
//                 {job.company}
//               </span>
//               <span className="text-gray-600 bg-lime-50 text-lime-600 px-2 py-1 rounded-lg">
//                 {job.city}
//               </span>
//               <span className="text-gray-600 bg-orange-50 text-orange-700 px-2 py-1 rounded-lg">
//                 {job.experience_level}
//               </span>
//               <span className="text-gray-600 bg-cyan-50 text-cyan-800 px-2 py-1 rounded-lg">
//                 {job.specialization}
//               </span>
//               {job.salary_range && job.salary_range !== '' && (
//                 <span className="flex items-center bg-green-50 text-emerald-700 px-2 py-1 rounded-lg">
//                   {job.salary_range}
//                 </span>
//               )}
//               {job.min_experience_years && job.min_experience_years !== '' && (
//                 <span className="bg-rose-50 text-rose-700 px-2 py-1 rounded-lg">
//                   {job.min_experience_years}+ Years
//                 </span>
//               )}
//               <span className="text-gray-600 bg-purple-50 text-purple-700 px-2 py-1 rounded-lg">
//                 {job.created_at}
//               </span>
//             </div>
//           </div>
//         </div>
//         <div className="flex space-x-2">
//           <button
//             className={`px-4 py-2 border border-gray-300 rounded-md ${
//               isSaved
//                 ? "bg-lime-200 hover:bg-lime-300 text-lime-700"
//                 : "hover:bg-lime-300"
//             }`}
//             onClick={handleSaveToggle}
//           >
//             {isSaved ? "Saved" : "Save"}
//           </button>
//           <button
//             className="px-4 py-2 bg-black hover:bg-violet-700 text-white rounded-md"
//             onClick={handleApply}
//           >
//             Apply
//           </button>
//         </div>
//       </div>
//       <LoginModal
//         isOpen={isLoginModalOpen}
//         onClose={() => setIsLoginModalOpen(false)}
//       />
//     </>
//   );
// };

// export default JobCard;

