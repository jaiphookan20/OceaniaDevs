import React from "react";
import bookmarkIcon from "../assets/bookmark.svg"
import appliedJobsIcon from "../assets/appliedjobs.svg"
import { Link } from "react-router-dom";
import leftArrowIcon from "../assets/left-arrow.svg"
import mailboxIcon from "../assets/mailbox.svg"

const RecruiterDashboardHeader = ({ title }) => {
  return (
    <header className="mb-4">
    {/* <Link  to="/applied-jobs" className="text-teal-700 flex items-center mb-6 text-sm" role="menuitem">
        <img src={leftArrowIcon} className="max-h-4 mr-1"/>
        Applied Jobs
    </Link> */}
    <div className="flex justify-between items-center p-3 space-x-4 border-t border-b border-teal-200">
      <div className="ml-2 rounded-full">
        <div className="sm:flex sm:items-center sm:justify-between p-2">
          <div>
            <h1 className="text-6xl font-bold text-slate-600 sm:text-5xl bg-clip-text" style={{fontFamily:"Roobert-Regular, san-serif"}}>{title}</h1>
            <p className="mt-4 max-w-2xl text-lg text-slate-400" style={{fontFamily:"Avenir, san-serif"}}>Track and manage all your applications in one place</p>
          </div>
        </div>
      </div>
      <img src={mailboxIcon} alt="bookmark-icon" className="max-h-16" />
    </div>
  </header>
  );
};

export default RecruiterDashboardHeader;