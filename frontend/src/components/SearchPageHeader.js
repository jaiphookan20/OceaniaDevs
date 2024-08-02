import React from "react";
import SearchPageBar from "./SearchPage";


const SearchPageHeader = ( {title}) => {
  return (
    <header className="text-center py-4 rounded-lg mx-auto bg-slate-50/50">
      <div className="flex justify-between items-center p-10 bg-violet-50 max-w-7xl mx-auto rounded-3xl">
        <div className="text-start rounded-md">
          <div className="flex">
            <h1 className="text-6xl font-bold text-slate-600 border-slate-500">
              {title}
            </h1>
            <h1 className="text-6xl font-bold text-lime-500">:</h1>
          </div>
          <p className="text-green-800 mt-5 text-2xl text-slate-400 font-medium">
          {/* <p className="text-green-800 mt-5 text-1xl text-lime-200 font-semibold"> */}
          Discover the best technologies jobs in all of Oceania.
          </p>
        </div>
      </div>
    </header>
  );
};

export default SearchPageHeader;
