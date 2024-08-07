import React, { useState, useEffect, useCallback } from "react";
import CompanySearchBar from "./CompaniesSearchBar";
import CompanyCardSection from "./CompanyCardSection";
import IndustrySidebar from "./CompaniesSideBar";
import CompaniesSearchBar from "./CompaniesSearchBar";

const CompaniesPage = () => {
    const [companies, setCompanies] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [totalCompanies, setTotalCompanies] = useState(0);
    const [selectedIndustries, setSelectedIndustries] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    
    const pageSize = 10;

    const fetchCompanies = useCallback(async () => {
      setIsLoading(true);
      setError(null);
      try {
          const response = await fetch(`/api/companies?page=${currentPage}&page_size=${pageSize}&search=${searchQuery}`);
          if (!response.ok) {
              throw new Error('Failed to fetch companies');
          }
          const data = await response.json();
          console.log("API response:", data);
          if (Array.isArray(data)) {
              setCompanies(data);
              setTotalCompanies(data.length);
          } else if (data && Array.isArray(data.companies)) {
              setCompanies(data.companies);
              setTotalCompanies(data.total_companies);
          }
      } catch (error) {
          console.error("Error fetching companies:", error);
          setError("Failed to fetch companies. Please try again later.");
      } finally {
          setIsLoading(false);
      }
    }, [currentPage, searchQuery, pageSize, selectedIndustries]);   

    useEffect(() => {
        fetchCompanies();
    }, [fetchCompanies]);

    useEffect(() => {
        console.log("Companies state:", companies);
        console.log("Total companies:", totalCompanies);
    }, [companies, totalCompanies]);

    const handleSearchChange = (query) => {
        setSearchQuery(query);
        setCurrentPage(1);
    };

    const handlePageChange = (newPage) => {
        setCurrentPage(newPage);
    };

    const handleIndustryChange = (industries) => {
        setSelectedIndustries(industries);
        setCurrentPage(1);
    };

    return (
        <div className="max-w-7xl mx-auto">
            <div className="p-5">
                <h1 className="text-5xl font-semibold text-slate-600 mb-2">Companies Search</h1>
                <h3 className="text-lg font-medium text-slate-400" style={{fontFamily: "Avenir, san-serif"}}>Search for technology companies across Oceania by industry, region, company size, and more</h3>
            </div>
            <div className="max-w-7xl mx-auto flex">
            <div className="w-1/5">
                <IndustrySidebar 
                    selectedIndustries={selectedIndustries}
                    onIndustryChange={handleIndustryChange}
                />
            </div>
            <div className="flex-grow ml-8 w-4/5">
                <CompaniesSearchBar onSearchChange={handleSearchChange} />
                <CompanyCardSection
                    companies={companies}
                    currentPage={currentPage}
                    totalCompanies={totalCompanies}
                    pageSize={pageSize}
                    onPageChange={handlePageChange}
                />
            </div>
            </div>
        </div>
    );
};

export default CompaniesPage;