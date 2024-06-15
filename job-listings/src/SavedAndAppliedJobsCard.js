const SavedAndAppliedJobsCard = ({ job, onApply, onSave, onView }) => {
  return (
    <div
      className="flex items-center justify-between p-6 border-b border-lime-200 mb-2 rounded-lg shadow-md shadow-slate-200/50 cursor-pointer hover:bg-slate-100 hover:shadow-xl"
      // onClick={() => onView(job.job_id)}
    >
      <div className="flex items-center">
        <img src={job.logo} alt={job.company} className="w-14 h-14 mr-4" />
        <div>
          <h3
            className="font-bold text-lg flex items-center hover:text-violet-500"
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
            {job.company} • {job.city} • {job.experience_level} •{" "}
            {job.specialization} • {job.salary_range} • {job.created_at}
          </p>
        </div>
      </div>
      <div className="flex space-x-2">
        <button
          className="px-4 py-2 bg-lime-400 hover:bg-lime-600 text-black border border-green-600 rounded-md"
          onClick={() => onApply(job.job_id)}
        >
          Apply
        </button>
      </div>
    </div>
  );
};

export default SavedAndAppliedJobsCard;
