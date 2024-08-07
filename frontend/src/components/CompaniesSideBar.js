import React from "react";

const industries = [
  { id: "all", name: "All industries", count: 4820 },
  { id: "b2b", name: "B2B", count: 2269 },
  { id: "education", name: "Education", count: 190 },
  { id: "fintech", name: "Fintech", count: 561 },
  { id: "consumer", name: "Consumer", count: 792 },
  // Add more industries as needed
];

const IndustrySidebar = ({ selectedIndustries, onIndustryChange }) => {
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

  return (
    <div className="w-64 bg-slate-50 rounded-lg shadow-sm p-6 border border-emerald-200" style={{fontFamily: "Avenir, san-serif"}}>
      <div>
        <h2 className="text-lg font-semibold mb-4">Filters</h2>
        <div className="space-y-2">
          {industries.map((industry) => (
            <div key={industry.id} className="flex items-center">
              <input
                type="checkbox"
                id={industry.id}
                checked={selectedIndustries.includes(industry.id)}
                onChange={() => handleIndustryClick(industry.id)}
                className="mr-2"
              />
              <label htmlFor={industry.id} className="flex-grow text-sm">
                {industry.name}
              </label>
              <span className="text-xs text-gray-500">{industry.count}</span>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 className="text-lg font-semibold mb-4 mt-4">Industry</h2>
        <div className="space-y-2">
          {industries.map((industry) => (
            <div key={industry.id} className="flex items-center">
              <input
                type="checkbox"
                id={industry.id}
                checked={selectedIndustries.includes(industry.id)}
                onChange={() => handleIndustryClick(industry.id)}
                className="mr-2"
              />
              <label htmlFor={industry.id} className="flex-grow text-sm">
                {industry.name}
              </label>
              <span className="text-xs text-gray-500">{industry.count}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default IndustrySidebar;