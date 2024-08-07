import React, { useState, useCallback } from 'react';
import debounce from 'lodash/debounce';

const CompaniesSearchBar = ({ onSearchChange }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const debouncedSearch = useCallback(
    debounce((query) => {
        onSearchChange(query);
    }, 300),
    [onSearchChange]
  );

  const handleInputChange = (event) => {
    const query = event.target.value;
    setSearchQuery(query);
    debouncedSearch(query);
  };

  return (
    <div className='border border-emerald-300 p-5 mb-4 rounded-xl'>
      <div className="">
        <input
          type="text"
          placeholder="Search..."
          value={searchQuery}
          onChange={handleInputChange}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>
  );
};

export default CompaniesSearchBar;

