import React from 'react';
import { Search } from 'lucide-react';
import atlassianLogo from "../assets/atlassian-Logo.png"
import canvaLogo from "../assets/canva-logo.png";
import employmentHeroLogo from "../assets/employment-hero-logo.jpeg";
import linktreeLogo from "../assets/linktree-logo.png";
import talenzaLogo from "../assets/talenza-logo.jpeg";
import buildKiteLogo from "../assets/buildkite-logo.png";
import dovetailLogo from "../assets/dovetail-logo.png";
import newRelicLogo from "../assets/new-relic-logo.png";
import wiseTechLogo from "../assets/wisetech-logo.png";
import amazonLogo from "../assets/amazon-logo.png";
import microsoftLogo from "../assets/microsoft-logo.png";


const colleges = [
    {
    name: "Buildkite",
    logo: buildKiteLogo,
    interviews: 525
    },
  {
    name: "Canva",
    logo: canvaLogo,
    interviews: 919
  },
  {
    name: "Amazon",
    logo: amazonLogo,
    interviews: 710
  },
  {
    name: "New Relic",
    logo: newRelicLogo,
    interviews: 525
  },
  {
    name: "Microsoft",
    logo: microsoftLogo,
    interviews: 1210
  },
  {
    name: "EmploymentHero",
    logo: employmentHeroLogo,
    interviews: 919
  },
  {
    name: "Dovetail",
    logo:dovetailLogo,
    interviews: 710
  },
  {
    name: "Atlassian",
    logo: atlassianLogo,
    interviews: 1210
  }
  
];

const TrendingCompanies = () => {
  return (
    <div className="flex flex-col items-center w-full max-w-6xl mx-auto mb-5">
      <h1 className="text-3xl font-semibold text-slate-500 mb-6 text-center bg-teal-50"
      style={{ fontFamily: "HeyWow, sans-serif" }}
      >
        Top Jobs
      </h1>
      
      <div className="relative w-full max-w-5xl">
        {/* <input
          type="text"
          placeholder="Search by college"
          className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        /> */}
      </div>
      
      <div className="w-full bg-white rounded-2xl shadow-sm border border-fuchsia-100 p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 grid-row-2 gap-6">
          {colleges.map((college, index) => (
            <div key={index} className="flex justify-start items-center space-x-4">
              <img src={college.logo} alt={`${college.name} logo`} className="h-20 w-30 rounded-full" />
              <div>
                <h2 className="font-semibold text-[#1e293b] text-lg">{college.name}</h2>
                <p className="text-xs text-gray-400">{college.interviews} Jobs</p>
              </div>
            </div>
          ))}
        </div>
        <div className="flex justify-center mt-6">
          <button className="px-4 py-2 bg-teal-50 text-[#64748b] text-sm border border-slate-300 font-medium rounded-full hover:bg-gray-200 transition duration-300">
            View all Companies
          </button>
        </div>
      </div>
    </div>
  );
};

export default TrendingCompanies;