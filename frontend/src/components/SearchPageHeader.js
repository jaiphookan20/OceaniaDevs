import React from "react";
import SearchPageBar from "./SearchPage";


const SearchPageHeader = () => {
  return (
    <header className="text-center py-12 mb-8 rounded-lg max-w-8xl mx-auto bg-slate-50/50">
      <div className="flex justify-between items-center p-20 bg-violet-50 max-w-7xl mx-auto rounded-3xl">
        {/* <div className="flex justify-center items-center space-x-4"> */}
        {/* <div className="grid grid-cols-3 grid-rows-2 gap-4">
        </div> */}
        <div className="text-start rounded-md">
          <div className="flex">
            <h1 className="text-6xl font-bold text-slate-600 border-slate-500">
              Find what's next
            </h1>
            <h1 className="text-6xl font-bold text-lime-500">:</h1>
          </div>
          <p className="text-green-800 mt-5 text-1xl text-slate-400 font-semibold">
          {/* <p className="text-green-800 mt-5 text-1xl text-lime-200 font-semibold"> */}
            THE BEST TECHNOLOGY JOBS, DOWN UNDER
          </p>
        </div>
      </div>
    </header>
  );
};

export default SearchPageHeader;
