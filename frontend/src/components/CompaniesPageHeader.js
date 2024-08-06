import React from "react";
import SearchPageBar from "./SearchPage";


const CompaniesPageHeader = ( {title}) => {
  return (
    <header className="text-center py-4 rounded-lg mx-auto bg-slate-50/50">
      <div className="flex justify-between items-center p-10 bg-lime-100 max-w-7xl mx-auto rounded-3xl border border-slate-300">
        <div className="text-start rounded-md">
          <div className="flex">
            <h1 className="text-6xl font-semibold text-emerald-600">
              Find Companies
            </h1>
            <h1 className="text-6xl font-bold text-lime-500">:</h1>
          </div>
          <p className="text-green-800 mt-5 text-2xl text-slate-400 font-medium">
          Discover the best tech jobs in all of Oceania.
          </p>
        </div>
      </div>
    </header>
  );
};

export default CompaniesPageHeader;
