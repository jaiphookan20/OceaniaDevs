import React, { useState, useCallback } from 'react';
import debounce from 'lodash/debounce';

const CompanySearchBar = ({ onSearchChange }) => {
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
    <div className="mb-6">
      <input
        type="text"
        placeholder="Search companies..."
        value={searchQuery}
        onChange={handleInputChange}
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
  );
};

export default CompanySearchBar;