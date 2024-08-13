import React from 'react';
import { Clock, BookmarkSimple } from 'lucide-react';

const JobPostSideBar = ({job, onSave, onApply }) => {
    return (
      <div className="w-64 bg-white rounded-lg shadow-sm border border-slate-200 p-4 font-sans">
        <button onClick={() => onApply(job.job_id)} className="w-full bg-violet-600 hover:bg-violet-900 text-white py-2 rounded-md mb-2 flex items-center justify-center">
          <span className="mr-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </svg>
          </span>
          Apply
        </button>
        <button onClick={() => onSave(job.job_id)} className="w-full bg-white hover:bg-lime-500 hover:text-white hover:font-semibold text-green-500 border border-green-500 py-2 rounded-md mb-2 flex items-center justify-center">
          <span className="mr-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
            </svg>
          </span>
          Save
        </button>
      </div>
    );
  };
  

export default JobPostSideBar;