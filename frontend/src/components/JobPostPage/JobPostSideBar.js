import React, { useState } from 'react';
import LoginModal from '../HomePage/LoginModal';
import JobPostCompanySideProfile from './JobPostCompanySideProfile';

const JobPostSideBar = ({ job, onSave, onApply, isInSession, isSaved, onUnsave, isApplied }) => {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isShareMenuOpen, setIsShareMenuOpen] = useState(false);

  const handleSaveToggle = () => {
    if (isInSession) {
      if (isSaved) {
        onUnsave(job.job_id);
      } else {
        onSave(job.job_id);
      }
    } else {
      setIsLoginModalOpen(true);
    }
  };

  const handleApplyClick = async () => {
    if (isInSession) {
      if (!isApplied) {
        await onApply(job.job_id);
      }
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
      <div className="w-64 bg-stone-100 rounded-lg shadow-sm border border-slate-400 p-4 font-sans">
        <button 
          onClick={handleApplyClick} 
          className={`w-full py-2 rounded-md mb-2 flex items-center justify-center ${
            isApplied 
              ? "bg-lime-500 hover:bg-green-700 text-white" 
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
          onClick={handleSaveToggle} 
          className={`w-full py-2 rounded-md mb-2 flex items-center justify-center ${
            isSaved 
              ? "bg-fuchsia-500 text-white hover:bg-lime-600" 
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
        
        {/* Share button and menu (commented out for now) */}
        {/* ... */}
        
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