import React from "react";
import { useNavigate } from "react-router-dom";
import JobCard from "./JobCard";

const JobSection = ({ title, jobs, onSave, onApply, onView }) => {
  const navigate = useNavigate();

/* We added a handleViewAll function that extracts the specialization from the title and navigates to the search page with the specialization as a query parameter.
   We changed the "View all" link to a button that calls this function when clicked.
   We updated the route to /search-page to match your existing route structure. */
  const handleViewAll = () => {
    const specialization = title.replace(" Roles", "");
    navigate(`/search-page?specialization=${encodeURIComponent(specialization)}`);
  };

  return (
    <div className="mx-auto max-w-6xl mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-bold pl-4">{title}</h2>
        <button 
          onClick={handleViewAll}
          className="text-indigo-600 hover:text-indigo-700 hover:underline hover:font-semibold"
        >
          View all {title}
        </button>
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
    </div>
  );
};

export default JobSection;

// import React from "react";
// import JobCard from "./JobCard";

// const JobSection = ({ title, jobs, onSave, onApply, onView }) => {
//   return (
//     <div className="mx-auto max-w-6xl mb-8">
//       <div className="flex justify-between items-center mb-4">
//         <h2 className="text-3xl font-bold">{title}</h2>
//         <a href="#" className="text-indigo-600 hover:text-indigo-700 hover:underline hover:font-semibold">
//           View all {title}
//       </a>
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

// import React from "react";
// import JobCard from "./JobCard";

// const JobSection = ({
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
//     <div className="mx-auto max-w-6xl">
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

// export default JobSection;
