import { useNavigate } from "react-router-dom";
import { FaMapMarkerAlt, FaBriefcase } from 'react-icons/fa';

const CompanyCard = ({ company }) => {
  const navigate = useNavigate();
  
  const handleClick = () => {
    navigate(`/company/${company.company_id}`);
  };
  
  return (
    <div 
      className="bg-white rounded-xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 cursor-pointer transform hover:-translate-y-1"
      onClick={handleClick}
    >
      <div className="flex items-center mb-6">
        <div className="w-20 h-20 mr-4 overflow-hidden rounded-lg bg-gray-100 flex items-center justify-center">
          <img src={company.logo_url} alt={company.name} className="w-16 h-16 object-contain" />
        </div>
        <h3 className="text-2xl font-semibold text-slate-600 hover:text-indigo-600 transition-colors duration-300" 
        >{company.name}</h3>
      </div>
      <p className="text-gray-600 mb-6 line-clamp-3 text-sm leading-relaxed">{company.description}</p>
      <div className="flex justify-between items-center text-sm">
        <div className="flex items-center text-gray-500">
          <FaMapMarkerAlt className="mr-2 text-indigo-500" />
          <span>{company.location} HQ</span>
        </div>
        <div className="flex items-center font-medium text-indigo-600">
          <FaBriefcase className="mr-2" />
          <span>{company.job_count} jobs</span>
        </div>
      </div>
      <div className="mt-6 pt-4 border-t border-gray-200">
        <button className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors duration-300 font-medium">
          View Company
        </button>
      </div>
    </div>
  );
};

export default CompanyCard;