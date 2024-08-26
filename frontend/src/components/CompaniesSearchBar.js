import React, { useState, useCallback } from 'react';
import debounce from 'lodash/debounce';
import { X } from 'lucide-react';

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

  const handleClearSearch = () => {
    setSearchQuery('');
    onSearchChange('');
  };

  return (
    <div className='border border-emerald-300 p-5 mb-4 rounded-xl'>
      <div className="relative flex items-center">
        <input
          type="text"
          placeholder="Search..."
          value={searchQuery}
          onChange={handleInputChange}
          className="w-full px-4 py-3 pr-10 border border-gray-300 rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleClearSearch}
          className="absolute right-3 text-gray-400 hover:text-gray-600 focus:outline-none"
          aria-label="Clear search"
        >
          <X size={18} />
        </button>
      </div>
    </div>
  );
};

export default CompaniesSearchBar;