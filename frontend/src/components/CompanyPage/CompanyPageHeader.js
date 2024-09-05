import React from 'react';
import { Link } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';

const CompanyPageHeader = ({ heading, subheading, logoSrc, company}) => {
  return (
    <div>
      <nav className="flex items-center text-sm text-gray-500 mb-4 space-x-1">
        <Link to="/" className="hover:text-gray-700">OceaniaDevs</Link>
        <ChevronRight size={16} className="mx-2" />
        <Link to="/companies" className="hover:text-gray-700">Companies</Link>
        <ChevronRight size={16} className="mx-2" />
        <span className="text-gray-700">{company.name}</span>
      </nav>
      <div className="mx-auto border-t border-b border-gray-200">
        <div className="">
          <div className="flex items-center">
            <div className="pl-2 pt-4 pb-4 pr-6">
              <img src={logoSrc} alt={`${heading} Logo`} className="h-24 object-contain rounded-full" />
            </div>
            <div>
              <h1 className="text-4xl font-semibold text-gray-900">{heading}</h1>
              <p className="text-md text-gray-500 mt-1" style={{fontFamily:"Avenir, san-serif"}}>{subheading}</p>
            </div>
          </div>
        </div>
      </div>
    <div className="mx-auto border-t border-b border-gray-200">
      <div className="p-4 text-lg">
        <div className="flex items-center justify-between">        
          <div className="flex items-center">
              <span className="text-gray-900 font-semibold mr-2">Industry</span>
              <span className="bg-violet-100 text-violet-600 font-semibold px-2 py-1 text-sm rounded">IT-Software Development</span>
            </div>
            <div className="flex items-center">
              <span className="text-gray-900 font-semibold mr-2">Jobs</span>
              <span className="bg-lime-100 text-green-700 px-2 py-1 rounded font-semibold text-sm">{company.total_jobs}</span>
            </div>
            <div className="flex items-center">
              <span className="text-gray-900 font-semibold mr-2">HQ</span>
              <span className="bg-teal-100 text-teal-700 font-semibold px-2 py-1 rounded text-sm">{company.address}</span>
            </div>
            <div className="flex items-center">
              {/* <span className="text-gray-900 font-semibold mr-2">HQ</span>
              <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-sm">{company.location}</span> */}
            <a href={""} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline flex items-center">
            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
              <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
            </svg>
            {company.website_url}
          </a>
            </div>
        </div>
      </div>
    </div>
    </div>
  );
};

export default CompanyPageHeader;