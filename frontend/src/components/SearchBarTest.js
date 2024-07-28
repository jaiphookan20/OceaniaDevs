import React, { useState } from 'react';
import { Search, ChevronDown } from 'lucide-react';

const SearchBarTest = () => {
  const [header, setHeader] = useState("Technology Jobs");
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");

  const handleSearch = () => {
    if (jobTitle) {
      setHeader(jobTitle);
    } else {
      setHeader("Remote jobs");
    }
  };

  const filterOptions = [
    "Experience level",
    "Salary range",
    "Companies",
    "Job type",
    "Markets"
  ];

  return (
    <div className="max-w-7xl mx-auto p-10 bg-fuchsia-50 rounded-3xl border-green-300 shadow-sm">
      <div className='pl-4'>
        <h1 className="text-6xl font-bold mb-2 text-slate-600">{header}</h1>
        <p className="text-gray-600 mb-4 text-slate-500">
          2,000+ Technology Jobs across Australia & New Zealand.
        </p>
      </div>
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex mb-4 space-x-4">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Job title or skill"
              className="w-full p-3 pr-10 border border-gray-300 rounded-lg"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
            />
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          </div>
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Country or timezone"
              className="w-full p-3 pr-10 border border-gray-300 rounded-lg"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          </div>
          <button
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition duration-300"
          >
            Clear
          </button>
          <button
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition duration-300"
            onClick={handleSearch}
          >
            Search
          </button>
        </div>
        
        <div className="flex flex-wrap gap-3">
          {filterOptions.map((option, index) => (
            <button
              key={index}
              className="px-4 py-2 border border-gray-300 rounded-full text-gray-700 flex items-center space-x-2 hover:bg-gray-100 transition duration-300"
            >
              <span>{option}</span>
              <ChevronDown size={16} />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SearchBarTest;