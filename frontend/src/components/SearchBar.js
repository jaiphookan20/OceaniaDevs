import React from "react";
import TechnologyDropdown from "./TechnologyDropdown";

const SearchBar = ({
  searchQuery,
  onSearchChange,
  filters,
  onFilterChange,
  onFilterSearch,
  onClearAll,
}) => {
  const handleSearch = (e) => {
    e.preventDefault();
    onFilterSearch();
  };

  return (
    <div className="bg-white p-4 pb-8 rounded-lg shadow-md mb-6">
      <form onSubmit={handleSearch}>
        {/* Top row: Search input, Location filter, and buttons */}
        <div className="flex items-center space-x-4 mb-4">
          <div className="flex-grow">
            <input
              type="text"
              placeholder="Search by Title, Company, Technology ...."
              className="w-full border border-green-400 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-lime-400"
              value={searchQuery}
              onChange={onSearchChange}
            />
          </div>
          <select
            name="city"
            className="border border-green-300 bg-green-50 text-green-700 font-medium rounded-lg px-4 py-2 text-gray-600 hover:bg-lime-200"
            value={filters.city}
            onChange={onFilterChange}
          >
            <option value="">Location</option>
            <option value="Sydney">Sydney, NSW</option>
            <option value="Melbourne">Melbourne, VIC</option>
            <option value="Brisbane">Brisbane, QLD</option>
            <option value="Canberra">Canberra, ACT</option>
            <option value="Canberra">Canberra, ACT</option>
            {/* Add more cities as needed */}
          </select>
          <button
            type="button"
            className="bg-black text-white rounded-lg px-4 py-2"
            onClick={onClearAll}
          >
            Clear All
          </button>
          <button
            type="submit"
            className="bg-purple-600 text-white rounded-lg px-4 py-2"
          >
            Search
          </button>
        </div>

        {/* Bottom row: All other filters */}
        <div className="flex space-x-4">
          <select
            name="specialization"
            className="flex-grow border border-green-300 bg-green-50 text-green-700 font-medium rounded-lg px-4 py-2 text-gray-600 hover:bg-lime-200"
            value={filters.specialization}
            onChange={onFilterChange}
          >
            <option value="">Specialization</option>
            <option value="Frontend">Frontend</option>
            <option value="Backend">Backend</option>
            <option value="Full-Stack">Full-Stack</option>
            <option value="Data & ML">Data & ML</option>
            <option value="QA & Testing">QA & Testing</option>
            <option value="Cloud & Infra">Cloud & Infra</option>
            <option value="DevOps">DevOps</option>
            <option value="Project Management">Project Management</option>
            <option value="IT Consulting">IT Consulting</option>
            <option value="Cybersecurity">Cybersecurity</option>
            

          </select>
          <select
            name="experience_level"
            className="flex-grow border border-green-300 bg-green-50 text-green-700 font-medium rounded-lg px-4 py-2 text-gray-600 hover:bg-lime-200"
            value={filters.experience_level}
            onChange={onFilterChange}
          >
            <option value="">Experience</option>
            <option value="Junior">Junior</option>
            <option value="Mid-Level">Mid-Level</option>
            <option value="Senior">Senior</option>
            <option value="Executive">Executive</option>
          </select>
          <select
            name="work_location"
            className="flex-grow border border-green-300 bg-green-50 text-green-700 font-medium rounded-lg px-4 py-2 text-gray-600 hover:bg-lime-200"
            value={filters.work_location}
            onChange={onFilterChange}
          >
            <option value="">Flexibility</option>
            <option value="Remote">Any</option>
            <option value="Remote">Remote</option>
            <option value="Hybrid">Hybrid</option>
            <option value="Office">Office</option>
          </select>
          <select
            name="job_arrangement"
            className="flex-grow border border-green-300 bg-green-50 text-green-700 font-medium rounded-lg px-4 py-2 text-gray-600 hover:bg-lime-200"
            value={filters.job_arrangement}
            onChange={onFilterChange}
          >
            <option value="">Work Type</option>
            <option value="Permanent">Permanent</option>
            <option value="Contract/Temp">Contract/Temp</option>
            <option value="Internship">Internship</option>
            <option value="Part-Time">Part-Time</option>
          </select>
          <div className="flex-grow">
            <TechnologyDropdown
              selectedTechnologies={filters.tech_stack || []}
              setSelectedTechnologies={(techs) =>
                onFilterChange({ target: { name: "tech_stack", value: techs } })
              }
            />
          </div>
        </div>
      </form>
    </div>
  );
};

export default SearchBar;