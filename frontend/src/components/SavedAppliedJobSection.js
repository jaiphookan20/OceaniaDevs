import React, { useState, useEffect } from "react";
import SavedAndAppliedJobsCard from "./SavedAndAppliedJobsCard";
import SavedAndAppliedJobsHeader from "./SavedAppliedJobsHeader";

const SavedAppliedJobSection = ({
  title,
  jobs,
  onSave,
  onApply,
  onView,
  fetchMoreJobs,
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

  return (
    <div>
      <SavedAndAppliedJobsHeader title={title} />
      <div className="bg-white rounded-lg shadow-md">
        {displayedJobs.map((job, index) => (
          <SavedAndAppliedJobsCard
            key={index}
            job={job}
            onApply={onApply}
            onSave={onSave}
            onView={onView}
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


// import React from "react";
// import SavedAndAppliedJobsCard from "./SavedAndAppliedJobsCard";
// import SavedAndAppliedJobsHeader from "./SavedAppliedJobsHeader";

// const SavedAppliedJobSection = ({
//   title,
//   jobs,
//   onSave,
//   onApply,
//   onView,
//   currentPage,
//   totalJobs,
//   pageSize,
//   onPageChange,
// }) => {
//   return (
//     <div>
//       <SavedAndAppliedJobsHeader title={title} />
//       <div className="flex justify-between items-center mb-4">
//         <h2 className="text-5xl font-bold"></h2>
//       </div>
//       <div className="bg-white rounded-lg shadow-md">
//         {jobs.map((job, index) => (
//           <SavedAndAppliedJobsCard
//             key={index}
//             job={job}
//             onApply={onApply}
//             onSave={onSave}
//             onView={onView}
//           />
//         ))}
//       </div>
//       {currentPage && totalJobs && pageSize && onPageChange && (
//         <div className="flex justify-center mt-4">
//           <button
//             className="px-4 py-2 mx-1 bg-gray-200 rounded"
//             disabled={currentPage === 1}
//             onClick={() => onPageChange(currentPage - 1)}
//           >
//             Previous
//           </button>
//           <button
//             className="px-4 py-2 mx-1 bg-gray-200 rounded"
//             disabled={currentPage === Math.ceil(totalJobs / pageSize)}
//             onClick={() => onPageChange(currentPage + 1)}
//           >
//             Next
//           </button>
//         </div>
//       )}
//     </div>
//   );
// };

// export default SavedAppliedJobSection;
