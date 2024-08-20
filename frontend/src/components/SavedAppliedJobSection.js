import React, { useState, useEffect } from "react";
import SavedAndAppliedJobsCard from "./SavedAndAppliedJobsCard";
import SavedAndAppliedJobsHeader from "./SavedAppliedJobsHeader";

const SavedAppliedJobSection = ({
  title,
  jobs,
  onApply,
  onView,
  fetchMoreJobs,
  onRemove,
  isSavedJobs
}) => {
  const [displayedJobs, setDisplayedJobs] = useState([]);
  const [page, setPage] = useState(1);
  const pageSize = 3;

  useEffect(() => {
    setDisplayedJobs(jobs.slice(0, pageSize));
  }, [jobs]);

  const handleViewMore = async () => {
    const nextPage = page + 1;
    const newJobs = await fetchMoreJobs(nextPage, pageSize);
    setDisplayedJobs([...displayedJobs, ...newJobs]);
    setPage(nextPage);
  };

  const handleRemove = async (jobId) => {
    await onRemove(jobId);
    setDisplayedJobs(displayedJobs.filter(job => job.job_id !== jobId));
  };

  return (
    <div>
      <SavedAndAppliedJobsHeader title={title} />
      <div className="bg-white rounded-lg shadow-md">
        {displayedJobs.map((job, index) => (
          <SavedAndAppliedJobsCard
            key={index}
            job={job}
            onApply={onApply}
            onRemove={handleRemove}
            onView={onView}
            isSavedJobs={isSavedJobs}
          />
        ))}
      </div>
      {jobs.length > displayedJobs.length && (
        <div className="flex justify-center mt-4">
          <button
            className="px-4 py-2 bg-teal-600 text-white rounded hover:bg-violet-700"
            onClick={handleViewMore}
          >
            View More
          </button>
        </div>
      )}
    </div>
  );
};

export default SavedAppliedJobSection;

// import React, { useState, useEffect } from "react";
// import SavedAndAppliedJobsCard from "./SavedAndAppliedJobsCard";
// import SavedAndAppliedJobsHeader from "./SavedAppliedJobsHeader";

// const SavedAppliedJobSection = ({
//   title,
//   jobs,
//   onApply,
//   onView,
//   fetchMoreJobs,
// }) => {
//   const [displayedJobs, setDisplayedJobs] = useState([]);
//   const [page, setPage] = useState(1);
//   const pageSize = 3;

//   useEffect(() => {
//     setDisplayedJobs(jobs.slice(0, pageSize));
//   }, [jobs]);

//   const handleViewMore = async () => {
//     const nextPage = page + 1;
//     const newJobs = await fetchMoreJobs(nextPage, pageSize);
//     setDisplayedJobs([...displayedJobs, ...newJobs]);
//     setPage(nextPage);
//   };

//   const handleRemove = (jobId) => {
//     setDisplayedJobs(displayedJobs.filter(job => job.job_id !== jobId));
//   };

//   return (
//     <div>
//       <SavedAndAppliedJobsHeader title={title} />
//       <div className="bg-white rounded-lg shadow-md">
//         {displayedJobs.map((job, index) => (
//           <SavedAndAppliedJobsCard
//             key={index}
//             job={job}
//             onApply={onApply}
//             onRemove={handleRemove}
//             onView={onView}
//           />
//         ))}
//       </div>
//       {jobs.length > displayedJobs.length && (
//         <div className="flex justify-center mt-4">
//           <button
//             className="px-4 py-2 bg-teal-600 text-white rounded hover:bg-violet-700"
//             onClick={handleViewMore}
//           >
//             View More
//           </button>
//         </div>
//       )}
//     </div>
//   );
// };

// export default SavedAppliedJobSection;