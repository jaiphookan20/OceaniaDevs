import React from "react";
import { useNavigate } from "react-router-dom";
const CompanyCard = ({ company }) => {
  const navigate = useNavigate();
  return (
    <div className="bg-slat-50 rounded-lg shadow-sm p-6 flex items-start border border-emerald-200" style={{fontFamily: "Avenir, san-serif"}} onClick={() => navigate(`/company/${company.company_id}`)}>
      <img src={company.logo_url} alt={company.name} className="w-16 h-16 mr-6 rounded-full hover:cursor-pointer" />
      <div className="flex-grow">
        <div className="flex justify-between items-start">
        <h3 className="text-xl text-slate-700 font-semibold hover:cursor-pointer">{company.name}</h3>
        <p className="text-sm text-slate-500">{company.city}, {company.state}</p>
        </div>
        <p className="text-sm mt-2 text-slate-600" >{company.description}</p>
        <div className="mt-3 space-x-2 flex">
            <div className="flex items-center">
              <span className="bg-fuchsia-100 text-fuchsia-600 font-semibold px-2 py-1 text-sm rounded">{company.industry}</span>
            </div>
            <div className="flex items-center">
              <span className="bg-teal-100 text-teal-700 font-semibold px-2 py-1 rounded text-sm">{company.address}</span>
            </div>
            <div className="flex items-center">
              <span className="bg-lime-100 text-green-700 px-2 py-1 rounded font-semibold text-sm">{company.job_count} Jobs</span>
            </div>
            <div className="flex items-center">
              <span className="bg-cyan-100 text-cyan-700 px-2 py-1 rounded font-semibold text-sm">{company.type}</span>
            </div>
        </div>
      </div>
    </div>
  );
};

export default CompanyCard;


