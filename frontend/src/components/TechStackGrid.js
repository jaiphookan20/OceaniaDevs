import React from 'react';
import { icons } from '../data/tech-icons';

const techStack = [
  { name: "Node.js", logo: icons.nodejs },
  { name: "TypeScript", logo: icons.typescript },
  { name: "PostgreSQL", logo: icons.postgresql },
  { name: "Google Cloud", logo: icons.gcp },
  { name: "Spring", logo: icons.spring },
  { name: "React", logo: icons.react },
  { name: "Docker", logo: icons.docker },
  { name: "GitHub", logo:icons.github },
];

const TechStackGrid = () => {
  return (
    <div className='pb-4'>
        <div className='p-3'>
            <h3 className='text-slate-600 font-semibold text-lg'>Tech Stack</h3>
            <p className='text-slate-500 text-md'>Learn about the tools and technologies that the company uses to build, market, and sell its products.</p>
        </div>
        <div className="bg-gray-100 p-4 rounded-lg shadow-sm"
            style={{fontFamily: "HeyWow"}}
        >
        <div className="grid grid-cols-4 gap-6">
            {techStack.map((tech, index) => (
            <div key={index} className="flex items-center space-x-2 bg-white p-2 rounded-lg shadow-sm">
                <img src={tech.logo} height={50} width={50} />
                <span className="text-md text-slate-600 font-semibold">{tech.name}</span>
            </div>
        ))}
        </div>
        </div>
    </div>
  );
};

export default TechStackGrid;