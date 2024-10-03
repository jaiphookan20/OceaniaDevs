import React, { useState, useCallback, useRef, useEffect } from "react";
import Autosuggest from 'react-autosuggest';
import SearchPageTechDropdown from "./SearchPageTechDropdown";
import searchIcon from "../../assets/search-icon.svg";
import debounce from 'lodash/debounce';

const SearchPageBar = ({
  searchQuery,
  onSearchChange,
  filters,
  onFilterChange,
  onFilterSearch,
  onClearAll,
}) => {
  const [suggestions, setSuggestions] = useState([]);

  // Add refs for each select element
  const cityRef = useRef(null);
  const specializationRef = useRef(null);
  const experienceLevelRef = useRef(null);
  const workLocationRef = useRef(null);
  const jobArrangementRef = useRef(null);

  // Highlight: Updated function to fetch suggestions
  const fetchSuggestions = useCallback(
    debounce(async (value) => {
      if (value.length < 2) {
        setSuggestions([]);
        return;
      }
      try {
        const response = await fetch(`/api/search_suggestions?query=${value}`);
        const data = await response.json();
        setSuggestions(data);
      } catch (error) {
        console.error('Error fetching suggestions:', error);
      }
    }, 300),
    []
  );

  // Highlight: Updated Autosuggest input props
  const inputProps = {
    placeholder: "Search by Title, Company, Technology ....",
    value: searchQuery,
    onChange: (_, { newValue }) => onSearchChange({ target: { value: newValue } }),
    className: "w-full border border-green-400 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-lime-400",
  };

  // Highlight: Updated Autosuggest theme
  const theme = {
    container: 'relative',
    suggestionsContainerOpen: 'absolute z-10 w-full bg-white shadow-lg rounded-b-lg mt-1 border border-gray-200',
    suggestionsList: 'list-none m-0 p-0 max-h-60 overflow-y-auto',
    suggestion: 'px-4 py-3 cursor-pointer hover:bg-gray-50 transition duration-150 ease-in-out',
    suggestionHighlighted: 'bg-purple-50',
  };

  // Highlight: New function to render suggestions
  const renderSuggestion = (suggestion) => (
    <div className="flex items-center">
      {suggestion.type === 'Company' && suggestion.logo && (
        <img src={suggestion.logo} alt={suggestion.name} className="w-6 h-6 mr-3 rounded-full object-cover" />
      )}
      <div style={{fontFamily: 'Avenir'}}>
        <div className="font-medium text-gray-800">{suggestion.name}</div>
        <div className="text-xs text-gray-500">{suggestion.type}</div>
      </div>
    </div>
  );

  const handleSearch = (e) => {
    e.preventDefault();
    onFilterSearch();
  };

  const getSelectClass = (filterName) => {
    const baseClass = "border rounded-lg px-4 py-2 text-gray-600 hover:bg-lime-200";
    const defaultClass = `${baseClass} border-green-300 bg-green-50 text-green-700 font-medium`;
    const selectedClass = `${baseClass} border-lime-500 bg-lime-100 text-lime-700 border-2 font-semibold`;
    
    return filters[filterName] ? selectedClass : defaultClass;
  };

  // Add this useEffect to reset select elements when filters change
  useEffect(() => {
    cityRef.current.value = filters.city || "";
    specializationRef.current.value = filters.specialization || "";
    experienceLevelRef.current.value = filters.experience_level || "";
    workLocationRef.current.value = filters.work_location || "";
    jobArrangementRef.current.value = filters.job_arrangement || "";
  }, [filters]);

  // Modify the onClearAll function to reset select elements
  const handleClearAll = () => {
    onClearAll();
    cityRef.current.value = "";
    specializationRef.current.value = "";
    experienceLevelRef.current.value = "";
    workLocationRef.current.value = "";
    jobArrangementRef.current.value = "";
  };

  return (
    <div className="bg-white p-4 pb-8 rounded-lg shadow-md mb-6">
      <form onSubmit={handleSearch}>
        {/* Top row: Search input, Location filter, and buttons */}
        <div className="flex items-center space-x-4 mb-4">
          <div className="flex-grow relative">
            <Autosuggest
              suggestions={suggestions}
              onSuggestionsFetchRequested={({ value }) => fetchSuggestions(value)}
              onSuggestionsClearRequested={() => setSuggestions([])}
              getSuggestionValue={(suggestion) => suggestion.name}
              renderSuggestion={renderSuggestion}
              inputProps={inputProps}
              theme={theme}
            />
          </div>
          <select
            ref={cityRef}
            name="city"
            className={`${getSelectClass('city')} w-40`}
            value={filters.city}
            onChange={onFilterChange}
          >
            <option value="">Location</option>
            <option value="Sydney">Sydney, NSW</option>
            <option value="Melbourne">Melbourne, VIC</option>
            <option value="Brisbane">Brisbane, QLD</option>
            <option value="Canberra">Canberra, ACT</option>
            <option value="Perth">Perth, WA</option>
            <option value="Adelaide">Adelaide, SA</option>
            <option value="Gold Coast">Gold Coast, QLD</option>
            <option value="Newcastle">Newcastle, NSW</option>
            <option value="Wollongong">Wollongong, NSW</option>
            <option value="Sunshine Coast">Sunshine Coast, QLD</option>
            <option value="Gold Coast">Gold Coast, QLD</option>
            <option value="Newcastle">Newcastle, NSW</option>
            <option value="Cairns">Cairns, QLD</option>
            <option value="Darwin">Darwin, NT</option>
            <option value="Hobart">Hobart, TAS</option>
            <option value="Launceston">Launceston, TAS</option>
            <option value="Mackay">Mackay, QLD</option>
            <option value="Rockhampton">Rockhampton, QLD</option>
            <option value="Townsville">Townsville, QLD</option>
            <option value="Toowoomba">Toowoomba, QLD</option>
            <option value="Townsville">Townsville, QLD</option>
          </select>
          <button
            type="button"
            className="bg-black text-white rounded-lg px-4 py-2"
            onClick={handleClearAll}
          >
            Clear All
          </button>
          <button
            type="submit"
            className="flex bg-purple-600 text-white rounded-lg px-4 py-2"
          >
            Search
            <img src={searchIcon} className="ml-2" alt="Search" />
          </button>
        </div>

        {/* Bottom row: All other filters */}
        <div className="flex space-x-4">
          <select
            ref={specializationRef}
            name="specialization"
            className={`${getSelectClass('specialization')} flex-grow`}
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
            ref={experienceLevelRef}
            name="experience_level"
            className={`${getSelectClass('experience_level')} flex-grow`}
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
            ref={workLocationRef}
            name="work_location"
            className={`${getSelectClass('work_location')} flex-grow`}
            value={filters.work_location}
            onChange={onFilterChange}
          >
            <option value="">Flexibility</option>
            <option value="Remote">Remote</option>
            <option value="Hybrid">Hybrid</option>
            <option value="Office">Office</option>
          </select>
          <select
            ref={jobArrangementRef}
            name="job_arrangement"
            className={`${getSelectClass('job_arrangement')} flex-grow`}
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
            <SearchPageTechDropdown
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

export default SearchPageBar;