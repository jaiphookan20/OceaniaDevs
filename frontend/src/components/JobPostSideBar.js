import React, { useState, useEffect } from 'react';
import LoginModal from './LoginModal';

const JobPostSideBar = ({ job, onSave, onApply, isInSession }) => {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [isApplied, setIsApplied] = useState(false);

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

  const handleSaveClick = async () => {
    if (isInSession) {
      await onSave(job.job_id);
      setIsSaved(!isSaved); 
    } else {
      setIsLoginModalOpen(true);
    }
  };

  const handleApplyClick = async () => {
    if (isInSession) {
      await onApply(job.job_id);
      setIsApplied(true);
      window.open(job.jobpost_url, '_blank');
    } else {
      setIsLoginModalOpen(true);
    }
  };

  return (
    <div className="w-64 bg-white rounded-lg shadow-sm border border-slate-200 p-4 font-sans">
      <button 
        onClick={handleApplyClick} 
        className={`w-full py-2 rounded-md mb-2 flex items-center justify-center ${
          isApplied 
            ? "bg-green-600 hover:bg-green-700 text-white" 
            : "bg-violet-600 hover:bg-violet-900 text-white"
        }`}
        disabled={isApplied}
      >
        <span className="mr-2">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </span>
        {isApplied ? "Applied" : "Apply"}
      </button>
      <button 
        onClick={handleSaveClick} 
        className={`w-full py-2 rounded-md mb-2 flex items-center justify-center ${
          isSaved 
            ? "bg-lime-500 text-white hover:bg-lime-600" 
            : "bg-white hover:bg-lime-500 hover:text-white hover:font-semibold text-green-500 border border-green-500"
        }`}
      >
        <span className="mr-2">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
          </svg>
        </span>
        {isSaved ? "Saved" : "Save"}
      </button>
      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
      />
    </div>
  );
};

export default JobPostSideBar;


// import React, { useState } from 'react';
// import { Clock, BookmarkSimple } from 'lucide-react';
// import LoginModal from './LoginModal';

// const JobPostSideBar = ({ job, onSave, onApply, isInSession }) => {
//   const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

//   const handleSaveClick = () => {
//     if (isInSession) {
//       onSave(job.job_id);
//     } else {
//       setIsLoginModalOpen(true);
//     }
//   };

//   const handleApplyClick = () => {
//     if (isInSession) {
//       onApply(job.job_id);
//     } else {
//       setIsLoginModalOpen(true);
//     }
//   };

//   return (
//     <div className="w-64 bg-white rounded-lg shadow-sm border border-slate-200 p-4 font-sans">
//       <button onClick={handleApplyClick} className="w-full bg-violet-600 hover:bg-violet-900 text-white py-2 rounded-md mb-2 flex items-center justify-center">
//         <span className="mr-2">
//           <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
//             <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
//             <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
//           </svg>
//         </span>
//         Apply
//       </button>
//       <button onClick={handleSaveClick} className="w-full bg-white hover:bg-lime-500 hover:text-white hover:font-semibold text-green-500 border border-green-500 py-2 rounded-md mb-2 flex items-center justify-center">
//         <span className="mr-2">
//           <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
//             <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
//           </svg>
//         </span>
//         Save
//       </button>
//       <LoginModal
//         isOpen={isLoginModalOpen}
//         onClose={() => setIsLoginModalOpen(false)}
//       />
//     </div>
//   );
// };

// export default JobPostSideBar;