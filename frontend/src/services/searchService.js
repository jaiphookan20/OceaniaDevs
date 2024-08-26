const searchService = {
  filteredSearchJobs: async (filters) => {
    try {
      const queryParams = new URLSearchParams(filters);
      console.log('Sending request to:', `/api/filtered_search_jobs?${queryParams}`);
      const response = await fetch(`/api/filtered_search_jobs?${queryParams}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('API response:', data);
      return {
        jobs: data.results,
        total_jobs: data.total
      };
    } catch (error) {
      console.error('Error in filteredSearchJobs:', error);
      throw error;
    }
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
  