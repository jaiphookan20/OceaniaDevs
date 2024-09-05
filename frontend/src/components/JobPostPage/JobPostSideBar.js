import React, { useState, useEffect } from 'react';
import LoginModal from '../HomePage/LoginModal';
import JobPostCompanySideProfile from './JobPostCompanySideProfile';

const JobPostSideBar = ({ job, onSave, onApply, isInSession }) => {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [isApplied, setIsApplied] = useState(false);
  const [isShareMenuOpen, setIsShareMenuOpen] = useState(false);


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

  const handleShareClick = () => {
    setIsShareMenuOpen(!isShareMenuOpen);
  };

  const shareOptions = [
    { label: 'Copy link', icon: 'clipboard' },
    { label: 'Share via email', icon: 'mail' },
    { label: 'Share on Facebook', icon: 'facebook' },
    { label: 'Share on Twitter', icon: 'twitter' },
    { label: 'Share on LinkedIn', icon: 'linkedin' },
  ];

  return (
    <div>
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
            : "bg-lime-100 hover:bg-lime-500 hover:text-white hover:font-semibold text-green-500 border border-green-500"
        }`}
      >
        <span className="mr-2">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
          </svg>
        </span>
        {isSaved ? "Saved" : "Save"}
      </button>
      
      {/* New Share button and menu */}
      <div className="relative mt-4">
        <button 
          onClick={handleShareClick}
          className="w-full bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow flex items-center justify-center"
        >
          <span className="mr-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f4d50b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-smile"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/></svg>
          </span>
          Share
        </button>
        <div className="text-xs text-gray-500 mt-1 text-center flex items-center justify-center">
        </div>
        {isShareMenuOpen && (
          <div className="absolute z-10 mt-2 w-full rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
            <div className="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
              {shareOptions.map((option, index) => (
                <button
                  key={index}
                  className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 w-full text-left"
                  role="menuitem"
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
      />
    </div>
    <JobPostCompanySideProfile job={job}/>
    </div>
  );
};

export default JobPostSideBar;