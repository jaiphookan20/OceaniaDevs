import React, { useState } from "react";

const companies = [
  {
    name: "Airbnb",
    logo: "https://path-to-airbnb-logo.png",
    website: "airbnb.com",
  },
  {
    name: "Amazon",
    logo: "https://path-to-amazon-logo.png",
    website: "amazon.com",
  },
  {
    name: "Google",
    logo: "https://path-to-google-logo.png",
    website: "google.com",
  },
  // Add more companies as needed
];

const FindEmployerForm = () => {
  const [selectedEmployer, setSelectedEmployer] = useState("");

  const handleEmployerChange = (e) => {
    setSelectedEmployer(e.target.value);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
        <h2 className="mb-6 text-2xl font-bold text-center">
          Find your employer
        </h2>

        <div className="mb-6">
          <label
            className="block text-sm font-medium text-gray-700"
            htmlFor="employer"
          >
            Select employer
          </label>
          <div className="relative mt-1">
            <select
              id="employer"
              value={selectedEmployer}
              onChange={handleEmployerChange}
              className="block w-full pl-3 pr-10 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            >
              <option value="" disabled>
                Select your employer
              </option>
              {companies.map((company) => (
                <option key={company.name} value={company.name}>
                  <div className="flex items-center">
                    <img
                      src={company.logo}
                      alt={company.name}
                      className="w-5 h-5 mr-2 inline"
                    />
                    {company.name} - {company.website}
                  </div>
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="mb-6">
          <label
            className="block text-sm font-medium text-gray-700"
            htmlFor="registrationCode"
          >
            Registration code
          </label>
          <input
            type="text"
            id="registrationCode"
            className="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>

        <div className="flex items-center justify-between">
          <button className="px-4 py-2 font-medium text-white bg-gray-600 rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Return
          </button>
          <button className="px-4 py-2 font-medium text-white bg-green-600 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Complete registration
          </button>
        </div>

        <div className="mt-4 text-center">
          <button className="text-green-600 hover:underline focus:outline-none">
            Didn't find your employer? Create new employer
          </button>
        </div>
      </div>
    </div>
  );
};

export default FindEmployerForm;
