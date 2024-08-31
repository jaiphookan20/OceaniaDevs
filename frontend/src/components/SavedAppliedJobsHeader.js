import React from "react";
import bookmarkIcon from "../assets/bookmark.svg"
import appliedJobsIcon from "../assets/appliedjobs.svg"
import { Link } from "react-router-dom";
import leftArrowIcon from "../assets/left-arrow.svg"
import { ChevronLeft, ChevronRight } from 'lucide-react';

const SavedAndAppliedJobsHeader = ({ title }) => {
  return (
    <div>
      {title === "Saved Jobs" ? (
        <header className="mb-4">
          <div className="flex justify-between">
            <nav className="flex items-center text-sm text-gray-500 mb-4 space-x-1">
              <Link to="/" className="hover:text-gray-700">OceaniaDevs</Link>
              <ChevronRight size={16} className="mx-2" />
              <Link to="/search-page" className="hover:text-gray-700">Search Jobs</Link>
              <ChevronRight size={16} className="mx-2" />
              <span className="text-gray-700">Saved Jobs</span>            
            </nav>
            <nav className="flex items-center text-sm text-gray-500 mb-4 space-x-1">
              <Link to="/applied-jobs" className="hover:text-gray-700">Applied Jobs</Link>
              <ChevronRight size={16} className="mx-2" />
            </nav>
          </div>
          <div className="flex justify-between items-center p-3 space-x-4 border-t border-b border-teal-200">
            <div className="ml-2 rounded-full">
              <div className="sm:flex sm:items-center sm:justify-between p-2">
                <div>
                  <h1 className="text-6xl font-bold text-slate-600 sm:text-5xl bg-clip-text" style={{fontFamily:"Roobert-Regular, san-serif"}}>Saved Jobs</h1>
                  <p className="mt-4 max-w-2xl text-lg text-slate-400" style={{fontFamily:"Avenir, san-serif"}}>Track and manage all your applications in one place</p>
                </div>
              </div>
            </div>
            <img src={bookmarkIcon} alt="bookmark-icon" className="max-h-16" />
          </div>
        </header>
      ) : (
        <header className="mb-4">
          <div className="flex justify-between">
            <nav className="flex items-center text-sm text-gray-500 mb-4 space-x-1">
              <Link to="/" className="hover:text-gray-700">OceaniaDevs</Link>
              <ChevronRight size={16} className="mx-2" />
              <Link to="/search-page" className="hover:text-gray-700">Search Jobs</Link>
              <ChevronRight size={16} className="mx-2" />
              <span className="text-gray-700">Applied Jobs</span>            
            </nav>
            <nav className="flex items-center text-sm text-gray-500 mb-4 space-x-1">
              <Link to="/saved-jobs" className="hover:text-gray-700">Saved Jobs</Link>
              <ChevronRight size={16} className="mx-2" />
            </nav>
          </div>
        <div className="flex justify-between items-center p-3 space-x-4 border-t border-b border-teal-200">
          <div className="ml-2 rounded-full">
            <div className="sm:flex sm:items-center sm:justify-between p-2">
              <div>
                <h1 className="text-6xl font-bold text-slate-600 sm:text-5xl bg-clip-text" style={{fontFamily:"Roobert-Regular, san-serif"}}>Applied Jobs</h1>
                <p className="mt-4 max-w-2xl text-lg text-slate-400" style={{fontFamily:"Avenir, san-serif"}}>Track and manage all your applications in one place</p>
              </div>
            </div>
          </div>
          <img src={appliedJobsIcon} alt="applied-jobs-icon" />
        </div>
        <div className="flex items-center justify-center bg-teal-200 rounded-md mt-8 text-center" style={{fontFamily: "Avenir, san-serif"}}>

          <Link to="/dashboard" className="text-teal-800 mr-2" role="menuitem">
              Click here to track your applications
          </Link>
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
              </svg>
        </div>
      </header>
      )}
    </div>
  );
};

export default SavedAndAppliedJobsHeader;