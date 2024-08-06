

const JobCard = ({ job, onSave, onApply, onView }) => {
  return (
    <div
      className="flex items-center justify-between p-4 border-b border-grey-200 mb-2 rounded-lg shadow-md shadow-slate-200/50 cursor-pointer hover:bg-slate-100 hover:shadow-xl"
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
            {job.created_at=="1 day"  && (
              <img
                src="https://remoteok.com/assets/new2x.gif"
                alt="New"
                className="w-8 h-6 ml-3"
              />
            )}
          </h3>
          {/* <p className="text-gray-600 space-x-8">
            <span className="hover:underline cursor-pointer">{job.company}</span> • {job.city} • {job.experience_level} •{" "}
            {job.specialization} • {job.salary_range} • {job.created_at}
          </p> */}
          <div className="flex flex-wrap gap-2 pt-1">
            <span className="bg-fuchsia-50 text-fuchsia-700 px-2 py-1 rounded-lg hover:underline cursor-pointer">
              {job.company}
            </span>
            <span className="text-gray-600 bg-green-50 text-lime-600 px-2 py-1 rounded-lg">
              {job.city}
            </span>
            <span className="text-gray-600 bg-orange-50 text-orange-700 px-2 py-1 rounded-lg">
              {job.experience_level}
            </span>
            <span className="text-gray-600 bg-cyan-50 text-cyan-800 px-2 py-1 rounded-lg">
              {job.specialization}
            </span>
            <span className="text-gray-600 bg-pink-50 text-pink-700 px-2 py-1 rounded-lg">
              {job.salary_range}
            </span>
            <span className="text-gray-600 bg-purple-50 text-purple-700 px-2 py-1 rounded-lg">
              {job.created_at}
            </span>
          </div>
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
          className="px-4 py-2 bg-black hover:bg-violet-700 text-white rounded-md"
          onClick={() => onApply(job.job_id)}
        >
          Apply
        </button>
      </div>
    </div>
  );
};

export default JobCard;
