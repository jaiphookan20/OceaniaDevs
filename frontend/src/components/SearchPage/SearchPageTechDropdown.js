//TechnologyDropdown.jsx
import React, { useState, useEffect } from "react";
import { icons } from "../data/tech-icons";

const SearchPageTechDropdown = ({ selectedTechnologies, setSelectedTechnologies }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [technologies, setTechnologies] = useState([]);

  useEffect(() => {
    const fetchTechnologies = async () => {
      try {
        const response = await fetch(`/api/technologies`);
        const data = await response.json();
        if (response.ok) {
          const techNames = data.map(tech => tech.name); // Fixed to use data from response.json()
          setTechnologies(techNames);
          console.log("Fetched Technologies:", techNames); // Log fetched data directly
        } else {
          console.error('Error fetching technologies:', data.error);
        }
      } catch (error) {
        console.error('Error fetching technologies:', error);
      }
    };

    fetchTechnologies(); // Call the fetch function once

  }, []); // Empty dependency array ensures this effect runs only once



  const filteredTechnologies = technologies.filter((tech) =>
    tech.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSelect = (tech) => {
    if (selectedTechnologies.includes(tech)) {
      setSelectedTechnologies(selectedTechnologies.filter(t => t !== tech));
    } else {
      setSelectedTechnologies([...selectedTechnologies, tech]);
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setDropdownOpen(!dropdownOpen)}
        className="rounded-lg px-16 py-2 border border-green-300 bg-green-50 text-green-700 hover:bg-lime-200"
      >
        Technologies ({selectedTechnologies.length})
      </button>
      {dropdownOpen && (
        <div className="absolute mt-1 w-60 bg-white border rounded-lg shadow-lg z-50">
          <div className="mt-1 pr-3 text-center">
            <button
              onClick={() => setSelectedTechnologies([])}
              className="text-purple-500 hover:underline"
            >
              Clear All
            </button>
          </div>
          <div className="p-2">
            <input
              type="text"
              placeholder="Search technology"
              className="w-full border rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="max-h-96 overflow-y-auto" style={{ fontFamily: "Avenir, san-serif" }}>
            {filteredTechnologies.map((tech, index) => (
              <div
                key={index}
                className={`flex items-center p-2 hover:bg-gray-100 cursor-pointer ${
                  selectedTechnologies.includes(tech) ? "bg-purple-100" : ""
                }`}
                onClick={() => handleSelect(tech)}
              >
                <img
                  src={icons[tech.toLowerCase()] || icons['default']} // Default icon if not found
                  alt={tech}
                  className="w-6 h-6 ml-4 mr-6"
                />
                <span>{tech}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchPageTechDropdown;