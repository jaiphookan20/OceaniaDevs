// src/components/SearchBar.js
import React from "react";
import TechnologyDropdown from "./TechnologyDropdown";
import SearchPageHeader from "./SearchPageHeader";

const SearchBar = ({
  searchQuery,
  onSearchChange,
  filters,
  onFilterChange,
  onFilterSearch,
  onClearAll,
}) => {

  const handleSearch = (e) => {
    e.preventDefault(); // Prevent default form submission
    onFilterSearch(); // Call the search function without passing the event
  };

  return (
    <div>
      <div className="justify-items-center justify-center mx-auto">
        <div className="p-4 pb-8 border-b border-green-300 mb-10">
        <form onSubmit={handleSearch}>
            <div className="flex items-center space-x-4 mb-4">
              <div className="flex-1 relative">
                <input
                  type="text"
                  placeholder="Search by Title, Company, Technology ...."
                  className="w-full border border-green-400 rounded-lg py-2 px-4 pl-10 focus:outline-none focus:ring-2 focus:ring-lime-400"
                  value={searchQuery}
                  onChange={onSearchChange}
                />
                <div className="absolute top-1/2 left-3 transform -translate-y-1/2"></div>
              </div>
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
          </form>
          <div className="flex space-x-3">
          <select
            name="experience_level"
            className="border border-green-300 bg-green-50 text-green-700 font-medium rounded-lg px-4 py-2 text-gray-600 hover:bg-lime-200"
            value={filters.experience_level}
            onChange={onFilterChange}
          >
            <option value="">Experience level</option>
            <option value="Mid-Senior Level">Mid-Senior Level</option>
            <option value="Associate">Associate</option>
            <option value="Entry Level">Entry Level</option>
            <option value="Intern">Intern</option>
            <option value="Director">Director</option>
          </select>
          <select
            name="salary_range"
            className="border border-green-300 bg-green-50 text-green-700 font-medium rounded-lg px-4 py-2 text-gray-600 hover:bg-lime-200"
            value={filters.salary_range}
            onChange={onFilterChange}
          >
            <option value="">Salary range</option>
            <option value="20000 - 40000">20000 - 40000</option>
            <option value="40000 - 60000">40000 - 60000</option>
            <option value="60000 - 80000">60000 - 80000</option>
            <option value="80000 - 100000">80000 - 100000</option>
            <option value="100000 - 120000">100000 - 120000</option>
            <option value="120000 - 140000">120000 - 140000</option>
            <option value="140000 - 160000">140000 - 160000</option>
            <option value="160000 - 180000">160000 - 180000</option>
            <option value="180000 - 200000">180000 - 200000</option>
            <option value="200000 - 220000">200000 - 220000</option>
            <option value="220000 - 240000">220000 - 240000</option>
            <option value="240000 - 260000">240000 - 260000</option>
            <option value="260000+">260000+</option>
          </select>
          <select
            name="industry"
            className="border border-green-300 bg-green-50 text-green-700 font-medium rounded-lg px-4 py-2 text-gray-600 hover:bg-lime-200"
            value={filters.industry}
            onChange={onFilterChange}
          >
            <option value="">Industry</option>
            <option value="Banking & Financial Services">
              Banking & Financial Services
            </option>
            <option value="Fashion">Fashion</option>
            <option value="Mining">Mining</option>
            <option value="Healthcare">Healthcare</option>
            <option value="IT - Software Development">
              IT - Software Development
            </option>
            <option value="IT - Data Analytics">IT - Data Analytics</option>
            <option value="IT - Cybersecurity">IT - Cybersecurity</option>
            <option value="IT - Cloud Computing">IT - Cloud Computing</option>
            <option value="IT - Artificial Intelligence">
              IT - Artificial Intelligence
            </option>
            <option value="Agriculture">Agriculture</option>
            <option value="Automotive">Automotive</option>
            <option value="Construction">Construction</option>
            <option value="Education">Education</option>
            <option value="Energy & Utilities">Energy & Utilities</option>
            <option value="Entertainment">Entertainment</option>
            <option value="Hospitality & Tourism">Hospitality & Tourism</option>
            <option value="Legal">Legal</option>
            <option value="Manufacturing">Manufacturing</option>
            <option value="Marketing & Advertising">
              Marketing & Advertising
            </option>
            <option value="Media & Communications">
              Media & Communications
            </option>
            <option value="Non-Profit & NGO">Non-Profit & NGO</option>
            <option value="Pharmaceuticals">Pharmaceuticals</option>
            <option value="Real Estate">Real Estate</option>
            <option value="Retail & Consumer Goods">
              Retail & Consumer Goods
            </option>
            <option value="Telecommunications">Telecommunications</option>
            <option value="Transportation & Logistics">
              Transportation & Logistics
            </option>
          </select>
          <select
            name="specialization"
            className="border border-green-300 bg-green-50 text-green-700 font-medium  rounded-lg px-4 py-2 text-gray-600 hover:bg-lime-200"
            // value={filters.specialization}
            // onChange={onFilterChange}
            value={filters.specialization}
            onChange={onFilterChange}
          >
            <option value="">Specialization</option>
            <option value="Frontend">Frontend</option>
            <option value="Backend">Backend</option>
            <option value="DevOps">DevOps</option>
            <option value="Mobile">Mobile</option>
            <option value="Data">Data</option>
            <option value="Machine Learning & AI">Machine Learning & AI</option>
          </select>
          <TechnologyDropdown
            selectedTechnologies={filters.tech_stack || []}
            setSelectedTechnologies={(techs) =>
              onFilterChange({ target: { name: "tech_stack", value: techs } })
            }
          />
        </div>
      </div>
    </div>
    </div>
  );
};

export default SearchBar;
