// src/components/TechnologyDropdown.jsx
import React, { useState } from "react";

const icons = {
  aws: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg",
  docker:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg",
  gcp: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/googlecloud/googlecloud-original.svg",
  kubernetes:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kubernetes/kubernetes-original-wordmark.svg",
  angular:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/angularjs/angularjs-original.svg",
  terraform:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/terraform/terraform-original-wordmark.svg",
  prometheus:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prometheus/prometheus-original-wordmark.svg",
  azure:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azure/azure-original.svg",
};

const technologies = [
  "AWS",
  "Docker",
  "GCP",
  "Kubernetes",
  "Angular",
  "Terraform",
  "Prometheus",
  "Azure",
];

const TechnologyDropdown = ({ selectedTechnology, setSelectedTechnology }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const filteredTechnologies = technologies.filter((tech) =>
    tech.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSelect = (tech) => {
    setSelectedTechnology(tech);
    setDropdownOpen(false);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setDropdownOpen(!dropdownOpen)}
        className="border rounded-lg px-16 py-2 text-gray-600"
      >
        Technologies
      </button>
      {dropdownOpen && (
        <div className="absolute mt-1 w-full bg-white border rounded-lg shadow-lg">
          <div className="mt-1 pr-3 text-center">
            <button
              onClick={() => setDropdownOpen(false)}
              className="text-purple-500 hover:underline"
            >
              Clear
            </button>
          </div>
          <div className="pl-1 pr-1 pb-2">
            <input
              type="text"
              placeholder="Search technology"
              className="w-full border rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="max-h-60 overflow-y-auto">
            {filteredTechnologies.map((tech, index) => (
              <div
                key={index}
                className="flex items-center p-2 hover:bg-gray-100 cursor-pointer"
                onClick={() => handleSelect(tech)}
              >
                <img
                  src={icons[tech.toLowerCase()]}
                  alt={tech}
                  className="w-6 h-6 ml-4 mr-6"
                />
                <span>{tech}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default TechnologyDropdown;

// // src/components/TechnologyDropdown.jsx
// import React, { useState } from "react";

// const icons = {
//   aws: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg",
//   docker:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg",
//   gcp: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/googlecloud/googlecloud-original.svg",
//   kubernetes:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kubernetes/kubernetes-original-wordmark.svg",
//   angular:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/angularjs/angularjs-original.svg",
//   terraform:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/terraform/terraform-original-wordmark.svg",
//   prometheus:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prometheus/prometheus-original-wordmark.svg",
//   azure:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azure/azure-original.svg",
// };

// const technologies = [
//   "AWS",
//   "Docker",
//   "GCP",
//   "Kubernetes",
//   "Angular",
//   "Terraform",
//   "Prometheus",
//   "Azure",
// ];

// const TechnologyDropdown = () => {
//   const [searchTerm, setSearchTerm] = useState("");
//   const [dropdownOpen, setDropdownOpen] = useState(false);

//   const filteredTechnologies = technologies.filter((tech) =>
//     tech.toLowerCase().includes(searchTerm.toLowerCase())
//   );

//   return (
//     <div className="relative">
//       <button
//         onClick={() => setDropdownOpen(!dropdownOpen)}
//         className="border rounded-lg px-16 py-2 text-gray-600"
//       >
//         Technologies
//       </button>
//       {dropdownOpen && (
//         <div className="absolute mt-1 w-full bg-white border rounded-lg shadow-lg">
//           <div className="mt-1 pr-3 text-center">
//             <button
//               onClick={() => setDropdownOpen(false)}
//               className="text-purple-500 hover:underline"
//             >
//               Clear
//             </button>
//           </div>
//           <div className="pl-1 pr-1 pb-2">
//             <input
//               type="text"
//               placeholder="Search technology"
//               className="w-full border rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
//               value={searchTerm}
//               onChange={(e) => setSearchTerm(e.target.value)}
//             />
//           </div>
//           <div className="max-h-60 overflow-y-auto">
//             {filteredTechnologies.map((tech, index) => (
//               <div
//                 key={index}
//                 className="flex items-center p-2 hover:bg-gray-100 cursor-pointer"
//               >
//                 <img
//                   src={icons[tech.toLowerCase()]}
//                   alt={tech}
//                   className="w-6 h-6 ml-4 mr-6"
//                 />
//                 <span>{tech}</span>
//               </div>
//             ))}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default TechnologyDropdown;
