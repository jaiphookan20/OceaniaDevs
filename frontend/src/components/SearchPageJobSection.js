import React from "react";
import JobCard from "./JobCard";

const SearchPageJobSection = ({
  title,
  jobs,
  onSave,
  onApply,
  onView,
  currentPage,
  totalJobs,
  pageSize,
  onPageChange,
  isInSession 
}) => {
  // Add a check for jobs being undefined or empty
  if (!jobs || jobs.length === 0) {
    return (
      <div className="mx-auto max-w-6xl">
        <h2 className="text-3xl font-bold mb-4">No Jobs Found</h2>
        <p>Try adjusting your search criteria or clearing filters.</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-bold">
          {totalJobs} {totalJobs === 1 ? "Job" : "Jobs"} Found
        </h2>
      </div>
      <div className="bg-white rounded-lg shadow-md">
        {jobs.map((job, index) => (
          <JobCard
            key={index}
            job={job}
            onSave={onSave}
            onApply={onApply}
            onView={onView}
            isInSession={isInSession}
          />
        ))}
      </div>
      <div className="flex justify-between items-center mt-4 mb-14">
        <button
          disabled={currentPage === 1}
          onClick={() => onPageChange(currentPage - 1)}
          className="px-4 py-2 bg-black text-white rounded"
        >
          Previous
        </button>
        <span>
          Page {currentPage} of {Math.ceil(totalJobs / pageSize)}
        </span>
        <button
          disabled={currentPage === Math.ceil(totalJobs / pageSize)}
          onClick={() => onPageChange(currentPage + 1)}
          className="px-4 py-2 bg-black text-white rounded"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default SearchPageJobSection;

// import React from "react";
// import JobCard from "./JobCard";

// const SearchPageJobSection = ({
//   title,
//   jobs,
//   onSave,
//   onApply,
//   onView,
//   currentPage,
//   totalJobs,
//   pageSize,
//   onPageChange,
//   isInSession 
// }) => {
//   return (
//     <div className="mx-auto max-w-6xl">
//       <div className="flex justify-between items-center mb-4">
//         <h2 className="text-3xl font-bold">
//         {totalJobs} {totalJobs === 1 ? "Job" : "Jobs"} Found
//         </h2>
//         {/* <a href="#" className="text-indigo-600">
//           View all {title.toLowerCase()}
//         </a> */}
        
//       </div>
//       <div className="bg-white rounded-lg shadow-md">
//         {jobs.map((job, index) => (
//           <JobCard
//             key={index}
//             job={job}
//             onSave={onSave}
//             onApply={onApply}
//             onView={onView}
//             isInSession={isInSession}  // Pass isInSession to JobCard
//           />
//         ))}
//       </div>
//       <div className="flex justify-between items-center mt-4 mb-14">
//         <button
//           disabled={currentPage === 1}
//           onClick={() => onPageChange(currentPage - 1)}
//           className="px-4 py-2 bg-black text-white rounded"
//         >
//           Previous
//         </button>
//         <span>
//           Page {currentPage} of {Math.ceil(totalJobs / pageSize)}
//         </span>
//         <button
//           disabled={currentPage === Math.ceil(totalJobs / pageSize)}
//           onClick={() => onPageChange(currentPage + 1)}
//           className="px-4 py-2 bg-black text-white rounded"
//         >
//           Next
//         </button>
//       </div>
//     </div>
//   );
// };

// export default SearchPageJobSection;
