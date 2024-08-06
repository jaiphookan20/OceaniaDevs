const CompanyJobCard = ({ job, onSave, onApply, onView, company }) => {
    return (
      <div
        className="flex items-center justify-between p-4 border-b border-grey-200 mb-2 rounded-lg shadow-md shadow-slate-200/50 cursor-pointer hover:bg-slate-100 hover:shadow-xl"
        // onClick={() => onView(job.job_id)}
      >
        <div className="flex items-center">
          <img src={company.logo_url} alt={company.name} className="w-14 h-14 mr-4" />
          <div>
            <h3
              className="font-semibold text-lg flex items-center hover:text-violet-500"
              onClick={() => onView(job.job_id)}
            >
              {job.title}
              {job.new && (
                <img
                  src="https://remoteok.com/assets/new2x.gif"
                  alt="New"
                  className="w-8 h-6 ml-3"
                />
              )}
            </h3>
            <p className="text-gray-600 space-x-8">
              {company.name} • {job.work_location} • {job.experience_level} •{" "}
              {job.specialization} • {job.salary_range}
            </p>
          </div>
        </div>
        <div className="flex space-x-2">
          <button
            className="px-4 py-2 border border-gray-300 hover:bg-lime-300 rounded-md"
            onClick={() => onSave(job.job_id)}
          >
            Save
          </button>
          <button
            className="px-4 py-2 bg-violet-400 hover:bg-violet-700 text-white rounded-md"
            onClick={() => onApply(job.job_id)}
          >
            Apply
          </button>
        </div>
      </div>
    );
  };
  
  export default CompanyJobCard;
  