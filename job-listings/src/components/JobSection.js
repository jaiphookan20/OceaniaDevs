import React from "react";
import JobCard from "./JobCard";

const JobSection = ({
  title,
  jobs,
  onSave,
  onApply,
  onView,
  currentPage,
  totalJobs,
  pageSize,
  onPageChange,
}) => {
  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-bold">{title}</h2>
        <a href="#" className="text-indigo-600">
          View all {title.toLowerCase()}
        </a>
      </div>
      <div className="bg-white rounded-lg shadow-md">
        {jobs.map((job, index) => (
          <JobCard
            key={index}
            job={job}
            onSave={onSave}
            onApply={onApply}
            onView={onView}
          />
        ))}
      </div>
      {currentPage && totalJobs && pageSize && onPageChange && (
        <div className="flex justify-center mt-4">
          <button
            className="px-4 py-2 mx-1 bg-gray-200 rounded"
            disabled={currentPage === 1}
            onClick={() => onPageChange(currentPage - 1)}
          >
            Previous
          </button>
          <button
            className="px-4 py-2 mx-1 bg-gray-200 rounded"
            disabled={currentPage === Math.ceil(totalJobs / pageSize)}
            onClick={() => onPageChange(currentPage + 1)}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default JobSection;

// import React from "react";
// import JobCard from "./JobCard";

// const JobSection = ({ title, jobs, onSave, onApply, onView }) => {
//   return (
//     <div>
//       <div className="flex justify-between items-center mb-4">
//         <h2 className="text-3xl font-bold">{title}</h2>
//         <a href="#" className="text-indigo-600">
//           View all {title.toLowerCase()}
//         </a>
//       </div>
//       <div className="bg-white rounded-lg shadow-md">
//         {jobs.map((job, index) => (
//           <JobCard
//             key={index}
//             job={job}
//             onSave={onSave}
//             onApply={onApply}
//             onView={onView}
//           />
//         ))}
//       </div>
//     </div>
//   );
// };

// export default JobSection;
