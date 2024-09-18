import React, { useState, useEffect, useCallback } from "react";
// import CompanyCardSection from ".CompanyCardSection";
import CompanyCardSection from "../CompanyPage/CompanyCardSection";
// import CompaniesSearchBar from "./CompaniesSearchBar";
import CompaniesSearchBar from "../CompaniesPage/CompaniesSearchBar";
import HashLoader from "react-spinners/HashLoader";
import CompaniesSideBar from "../CompaniesPage/CompaniesSideBar";
import { Link } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';

const CompaniesPage = () => {
    const [companies, setCompanies] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [totalCompanies, setTotalCompanies] = useState(0);
    const [selectedIndustries, setSelectedIndustries] = useState([]);
    const [selectedTypes, setSelectedTypes] = useState([]);
    const [error, setError] = useState(null);
    const [initialLoading, setInitialLoading] = useState(true);
    const [loading, setLoading] = useState(false);
    
    const pageSize = 10;

    const fetchCompanies = useCallback(async (isInitialFetch = false) => {
      if (isInitialFetch) {
        setInitialLoading(true);
      } else {
        setLoading(true);
      }
      setError(null);
      try {
        const industryQuery = selectedIndustries.length > 0 && !selectedIndustries.includes('all') 
          ? `&industries=${encodeURIComponent(selectedIndustries.join(','))}` // Use encodeURIComponent to ensure proper URL encoding
          : '';
        const typeQuery = selectedTypes.length > 0 && !selectedTypes.includes('all')
          ? `&types=${selectedTypes.join(',')}`
          : '';
        const response = await fetch(`/api/filter-companies?page=${currentPage}&page_size=${pageSize}&search=${searchQuery}${industryQuery}${typeQuery}`);        
    
        if (!response.ok) {
            throw new Error('Failed to fetch companies');
        }
        const data = await response.json();

        if (Array.isArray(data)) {
            setCompanies(data);
            setTotalCompanies(data.length);
        } else if (data && Array.isArray(data.companies)) {
            setCompanies(data.companies);
            setTotalCompanies(data.total_companies);
        }
      } 
      catch (error) {
        console.error("Error fetching companies:", error);
        setError("Failed to fetch companies. Please try again later.");
      } 
      finally {
        if (isInitialFetch) {
          setInitialLoading(false);
        } else {
          setLoading(false);
        }
      }
    }, [currentPage, searchQuery, pageSize, selectedIndustries, selectedTypes]);   

    useEffect(() => {
        fetchCompanies(true);
    }, []);

    useEffect(() => {
        if (!initialLoading) {
            fetchCompanies();
        }
    }, [fetchCompanies, currentPage, searchQuery, selectedIndustries, selectedTypes]);

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

    const handleTypeChange = (types) => {
        setSelectedTypes(types);
        setCurrentPage(1);
    };

    if (initialLoading) {
        return (
          <div className="flex justify-center items-center h-screen">
            <HashLoader color="#8823cf" size={120} />
          </div>
        );
    }

    return (
        <div className="max-w-7xl p-6 mx-auto">
          <nav className="flex items-center text-sm text-gray-500 mb-4 space-x-1">
            <Link to="/" className="hover:text-gray-700">OceaniaDevs</Link>
            <ChevronRight size={16} className="mx-2" />
            <span className="text-gray-700">Companies</span>
          </nav>
            <div className="p-4 mb-8 border-t border-b border-slate-200">
                <h1 className="text-5xl font-semibold text-slate-600 mb-2">Companies Search</h1>
                <h3 className="text-lg font-medium text-slate-400" style={{fontFamily: "Avenir, san-serif"}}>Search for technology companies across Oceania by industry, region, company size, and more</h3>
            </div>
            <div className="flex">
                <div className="w-1/5">
                    <CompaniesSideBar 
                        selectedIndustries={selectedIndustries}
                        selectedTypes={selectedTypes}
                        onIndustryChange={handleIndustryChange}
                        onTypeChange={handleTypeChange}
                    />
                </div>
                <div className="flex-grow ml-8 w-4/5">
                    <CompaniesSearchBar onSearchChange={handleSearchChange} />
                    {loading ? (
                        <div className="flex justify-center items-center h-64">
                            <HashLoader color="#8823cf" size={50} />
                        </div>
                    ) : (
                        <CompanyCardSection
                        companies={companies}
                        currentPage={currentPage}
                        totalCompanies={totalCompanies}
                        pageSize={pageSize}
                        onPageChange={handlePageChange}
                        />
                    )}
                </div>
            </div>
        </div>
    );
};

export default CompaniesPage;