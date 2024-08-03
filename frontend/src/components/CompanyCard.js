import { useNavigate } from "react-router-dom";

const CompanyCard = ({ company }) => {
  const navigate = useNavigate();
  
  const handleClick = () => {
    navigate(`/company/${company.company_id}`);
  };
  
  return (
    <div 
      className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow duration-300 cursor-pointer"
      onClick={handleClick}
    >
      <div className="flex items-center mb-4">
        <img src={company.logo_url} alt={company.name} className="w-16 h-16 mr-4 object-contain" />
        <h3 className="text-xl font-semibold text-slate-700 hover:underline">{company.name}</h3>
      </div>
      <p className="text-gray-600 mb-4 line-clamp-3">{company.description}</p>
      <div className="flex justify-between items-center">
        <span className="text-sm text-gray-500">{company.location} HQ</span>
        <span className="text-sm font-medium text-indigo-600">{company.job_count} jobs</span>
      </div>
    </div>
  );
};

export default CompanyCard;
