import React from 'react';
import java from "../../assets/tech-logos/java.svg";
import python from "../../assets/tech-logos/python.svg";
import aws from "../../assets/tech-logos/aws.svg";
import react from "../../assets/tech-logos/react.svg";
import csharp from "../../assets/tech-logos/csharp.svg";
import javascript from "../../assets/tech-logos/javascript.svg";
import django from "../../assets/tech-logos/django.svg";
import typescript from "../../assets/tech-logos/typescript.svg";
import nodejs from "../../assets/tech-logos/nodejs.svg";
import dotnet from "../../assets/tech-logos/dotnet.svg";

import { useNavigate } from "react-router-dom";

const Card = ({ children, className }) => (
  <div className={`bg-white rounded-lg shadow-sm overflow-hidden ${className}`}>
    {children}
  </div>
);

const Button = ({ children, className }) => (
  <button className={`px-6 py-2 rounded-full text-sm font-medium transition-colors ${className}`}>
    {children}
  </button>
);

const colleges = [
  {
    name: "Java",
    title: "java",
    logo: java,
    interviews: 525
  },
  {
    name: "Python",
    title: "python",
    logo: python,
    interviews: 919
  },
  {
    name: "AWS",
    title: "aws",
    logo: aws,
    interviews: 710
  },
  {
    name: "React",
    title: "react",
    logo: react,
    interviews: 525
  },
  {
    name: "C#",
    title: "c#",
    logo: csharp,
    interviews: 1210
  },
  {
    name: "Javascript",
    title: "Javascript",
    logo: javascript,
    interviews: 919
  },
  {
    name: "Django",
    title: "django",
    logo: django,
    interviews: 710
  },
  {
    name: "Typescript",
    title: "typescript",
    logo: typescript,
    interviews: 1210
  },
  {
    name: ".NET",
    title: ".NET",
    logo: dotnet,
    interviews: 1210
  },
  {
    name: "NodeJS",
    title: "node.js",
    logo: nodejs,
    interviews: 1210
  },
];

const TrendingTechStackGrid = () => {
  const navigate = useNavigate();
  
  const handleTechClick = (techName) => {
    console.log("Clicking Logo")
    navigate(`/search-page?tech=${encodeURIComponent(techName)}`);
  };

  return (
    <div className="w-full max-w-6xl mx-auto px-4 py-8" style={{fontFamily: "Avenir, san-serif"}}>
      <h1 className="text-3xl font-medium text-slate-700 mb-8 text-center" style={{fontFamily: "Avenir, san-serif"}}>
        Search by Technology
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 p-3 rounded-md ">
        {colleges.map((college, index) => (
          <Card 
            key={index} 
            className="hover:shadow-lg transition-shadow duration-300 rounded-xl bg-slate-300 border border-slate-300 shadow-xl cursor-pointer"
          >
            <div className="p-3">
              <div className="flex items-center space-x-4" onClick={() => handleTechClick(college.title.toLowerCase())}>
                <img src={college.logo} alt={`${college.name} logo`} className="h-16 w-16 rounded-lg object-cover" />
                <div>
                  <h2 className="font-semibold text-slate-700 text-lg">{college.name}</h2>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
      
      <div className="flex justify-center mt-12" onClick={()=>navigate("/companies")}>
        <Button className="bg-black font-bold text-white text-slate-700 border border-slate-300 hover:bg-slate-100">
          View all Technologies
        </Button>
      </div>
    </div>
  );
};

export default TrendingTechStackGrid