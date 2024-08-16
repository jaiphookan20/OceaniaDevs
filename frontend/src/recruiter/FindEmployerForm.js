import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const FindEmployerForm = ({ onComplete }) => {
  const [selectedEmployer, setSelectedEmployer] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [companies, setCompanies] = useState([]);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const response = await fetch("/api/companies", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        const result = await response.json();
        setCompanies(result);
      } catch (error) {
        console.error("Error fetching companies:", error);
      }
    };

    fetchCompanies();
  }, []);

  const handleEmployerChange = (e) => {
    setSelectedEmployer(e.target.value);
  };

  const handleSelect = (company) => {
    setSelectedEmployer(company.name);
    setDropdownOpen(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("/api/register/employer/update_company", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ company: selectedEmployer }),
      });
      const result = await response.json();
      console.log(result.message);
      if (result.message === "Recruiter company updated successfully") {
        onComplete();
        // navigate("/employer/post-job");
      }
    } catch (error) {
      console.error("Error updating recruiter company info:", error);
    }
  };

  const filteredCompanies = companies.filter((company) =>
    company.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100"  style={{fontFamily: "Avenir, san-serif"}}>
      <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
        <h2 className="mb-6 text-3xl font-bold text-center">
          Find your employer
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label
              className="block text-sm font-medium text-gray-700"
              htmlFor="employer"
            >
              Select employer
            </label>
            <div className="relative mt-1">
              <button
                type="button"
                onClick={() => setDropdownOpen(!dropdownOpen)}
                className="w-full pl-3 pr-10 py-2 mt-1 bg-slate-300 border border-gray-300 rounded-md shadow-sm focus:outline-none hover:bg-violet-500 hover:text-white focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                {selectedEmployer || "Select your employer"}
              </button>
              {dropdownOpen && (
                <div className="absolute mt-1 w-full bg-white border rounded-lg shadow-lg z-10">
                  <div className="p-2">
                    <input
                      type="text"
                      placeholder="Search company"
                      className="w-full border rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                  </div>
                  <div className="max-h-60 overflow-y-auto">
                    {filteredCompanies.map((company, index) => (
                      <div
                        key={index}
                        className="flex items-center p-2 hover:bg-violet-500 hover:text-white hover:font-semibold cursor-pointer"
                        onClick={() => handleSelect(company)}
                      >
                        <img src={company.logo_url} className="h-6 w-6 mr-4 rounded-full" />
                        {company.name}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
          <div className="flex items-center justify-between">
            <button
              type="button"
              className="px-4 py-2 font-medium text-white bg-gray-600 rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              onClick={() => navigate(-1)}
            >
              Return
            </button>
            <button
              type="submit"
              className="px-4 py-2 font-medium text-white bg-green-500 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Complete registration
            </button>
          </div>
        </form>
        <div className="mt-4 text-center">
          <button
            type="button"
            className="text-emerald-700 hover:underline focus:outline-none"
            onClick={() => navigate("/employer/organization-details")}
          >
            Didn't find your employer? Create new employer
          </button>
        </div>
      </div>
    </div>
  );
};

export default FindEmployerForm;
