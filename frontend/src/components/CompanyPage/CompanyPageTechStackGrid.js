import React from 'react';
import { icons } from '../../data/tech-icons';

const CompanyPageTechStackGrid = ({ company }) => {
  /* Filter the tech stack to only include technologies with matching icons */
  const filteredTechStack = company.total_tech_stack.filter(tech => 
    icons.hasOwnProperty(tech.toLowerCase())
  );

  return (
    <div className='pb-4'>
      <div className='p-3'>
        <h3 className='text-slate-600 font-semibold text-lg'>Tech Stack</h3>
        <p className='text-slate-500 text-md' style={{fontFamily: "Avenir, san-serif"}}>Learn about the tools and technologies that the company uses to build, market, and sell its products.</p>
      </div>
      <div className="bg-gray-100 p-4 rounded-lg shadow-sm"
        style={{fontFamily: "HeyWow"}}
      >
        <div className="grid grid-cols-4 gap-6">
          {filteredTechStack.map((tech, index) => {
            const iconKey = tech.toLowerCase();
            return icons[iconKey] ? (
              <div key={index} className="flex items-center space-x-2 bg-white p-2 rounded-lg shadow-sm">
                <img src={icons[iconKey]} alt={tech} height={50} width={50} />
                <span className="text-md text-slate-600 font-semibold text-center pl-4">{tech.charAt(0).toUpperCase() + tech.slice(1).toLowerCase()}</span>
              </div>
            ) : null;
          })}
        </div>
      </div>
    </div>
  );
};

export default CompanyPageTechStackGrid;