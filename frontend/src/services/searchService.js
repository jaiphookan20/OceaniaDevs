const searchService = {
    filteredSearchJobs: async (filters) => {
      const queryParams = new URLSearchParams(filters);
      const response = await fetch(`/api/filtered_search_jobs?${queryParams}`);
      return response.json();
    },
  
    searchCompanies: async (filters) => {
      const queryParams = new URLSearchParams(filters);
      const response = await fetch(`/api/filter-companies?${queryParams}`);
      return response.json();
    },
  
    instantSearchJobs: async (query) => {
      const response = await fetch(`/api/instant_search_jobs?query=${query}`);
      return response.json();
    }
  };
  
  export default searchService;
  