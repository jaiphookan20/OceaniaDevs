import React from "react";

const industries = [
  { id: "all", name: "All industries" },
  { id: "Government", name: "Government" },
  { id: "Banking & Financial Services", name: "Banking & Financial Services" },
  { id: "Fashion", name: "Fashion" },
  { id: "Mining", name: "Mining" },
  { id: "Healthcare", name: "Healthcare" },
  { id: "IT - Software Development", name: "IT - Software Development" },
  { id: "IT - Data Analytics", name: "IT - Data Analytics" },
  { id: "IT - Cybersecurity", name: "IT - Cybersecurity" },
  { id: "IT - Cloud Computing", name: "IT - Cloud Computing" },
  { id: "IT - Artificial Intelligence", name: "IT - Artificial Intelligence" },
  { id: "Agriculture", name: "Agriculture" },
  { id: "Automotive", name: "Automotive" },
  { id: "Construction", name: "Construction" },
  { id: "Education", name: "Education" },
  { id: "Energy & Utilities", name: "Energy & Utilities" },
  { id: "Entertainment", name: "Entertainment" },
  { id: "Hospitality & Tourism", name: "Hospitality & Tourism" },
  { id: "Legal", name: "Legal" },
  { id: "Manufacturing", name: "Manufacturing" },
  { id: "Marketing & Advertising", name: "Marketing & Advertising" },
  { id: "Media & Communications", name: "Media & Communications" },
  { id: "Non-Profit & NGO", name: "Non-Profit & NGO" },
  { id: "Pharmaceuticals", name: "Pharmaceuticals" },
  { id: "Real Estate", name: "Real Estate" },
  { id: "Retail & Consumer Goods", name: "Retail & Consumer Goods" },
  { id: "Telecommunications", name: "Telecommunications" },
  { id: "Transportation & Logistics", name: "Transportation & Logistics" },
];

const types = [
  { id: "all", name: "All types" },
  { id: "Agency", name: "Agency" },
  { id: "Company", name: "Company" },
];

const CompaniesSideBar = ({ selectedIndustries, selectedTypes, onIndustryChange, onTypeChange }) => {
  const handleIndustryClick = (industryId) => {
    let newSelectedIndustries;
    if (industryId === "all") {
      newSelectedIndustries = selectedIndustries.includes("all") ? [] : ["all"];
    } else {
      newSelectedIndustries = selectedIndustries.includes(industryId)
        ? selectedIndustries.filter((id) => id !== industryId)
        : [...selectedIndustries.filter((id) => id !== "all"), industryId];
    }
    onIndustryChange(newSelectedIndustries);
  };

  const handleTypeClick = (typeId) => {
    let newSelectedTypes;
    if (typeId === "all") {
      newSelectedTypes = selectedTypes.includes("all") ? [] : ["all"];
    } else {
      newSelectedTypes = selectedTypes.includes(typeId)
        ? selectedTypes.filter((id) => id !== typeId)
        : [...selectedTypes.filter((id) => id !== "all"), typeId];
    }
    onTypeChange(newSelectedTypes);
  };

  return (
    <div className="w-64 bg-slate-50 rounded-lg shadow-sm p-6 border border-emerald-200" style={{fontFamily: "Avenir, san-serif"}}>
      <div>
        <h2 className="text-lg font-semibold mb-4">Industry</h2>
        <div className="space-y-2">
          {industries.map((industry) => (
            <div key={industry.id} className="flex items-center">
              <input
                type="checkbox"
                id={`industry-${industry.id}`}
                checked={selectedIndustries.includes(industry.id)}
                onChange={() => handleIndustryClick(industry.id)}
                className="mr-2"
              />
              <label htmlFor={`industry-${industry.id}`} className="flex-grow text-sm">
                {industry.name}
              </label>
            </div>
          ))}
        </div>
      </div>
      <div className="mt-6">
        <h2 className="text-lg font-semibold mb-4">Type</h2>
        <div className="space-y-2">
          {types.map((type) => (
            <div key={type.id} className="flex items-center">
              <input
                type="checkbox"
                id={`type-${type.id}`}
                checked={selectedTypes.includes(type.id)}
                onChange={() => handleTypeClick(type.id)}
                className="mr-2"
              />
              <label htmlFor={`type-${type.id}`} className="flex-grow text-sm">
                {type.name}
              </label>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CompaniesSideBar;