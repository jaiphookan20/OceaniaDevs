import React from "react";

const SearchPageHeader = ({ title, subheading="Discover the best jobs in the technology industry across all of Oceania.", totalJobs }) => {
  return (
    <div className="mx-auto border-t border-b border-gray-200 mb-5">
        <div className="p-6">
          <div className="flex justify-between">
            <div className="">
              <h1 className="text-6xl font-semibold text-slate-600">
                
              <span className="text-teal-400"></span> <span className="text-slate-500">{totalJobs}</span>  <span className="text-violet-500">{title.replace(' Jobs', '')}</span> Jobs
              </h1>
              <p className="text-xl text-gray-500 mt-4" style={{fontFamily:"Avenir, san-serif"}}>{subheading}</p>
            </div>
          </div>
        </div>
    </div>
  );
};

export default SearchPageHeader;