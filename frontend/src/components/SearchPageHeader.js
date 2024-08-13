import React from "react";
import SearchPageBar from "./SearchPage";
import starLightIcon from "../assets/star-light.png"
import starLightIcon256 from "../assets/star-light_256.png"
import databaseIcon from "../assets/database-icon.png";

const SearchPageHeader = ( {title, subheading="Discover the best jobs in the technology industry across all of Oceania."}) => {
  return (
    <div className="mx-auto border-t border-b border-gray-200 mb-5">
        <div className="p-6">
          <div className="flex justify-between">
            <div className="">
              <h1 className="text-6xl font-semibold text-slate-500">
                 <span className="text-violet-500">{title} </span> Jobs
              </h1>
              <p className="text-xl text-gray-500 mt-4" style={{fontFamily:"Avenir, san-serif"}}>{subheading}</p>
            </div>
            {/* <img src={databaseIcon} alt={`${title} Logo`} className="h-24 object-contain rounded-full" /> */}
          </div>
        </div>
    </div>
  );
};

export default SearchPageHeader;


// const SearchPageHeader = ( {title}) => {
//   return (
//     <header className="text-center py-4 rounded-lg mx-auto bg-slate-50/50">
//       <div className="flex justify-between items-center p-10 bg-violet-50 max-w-7xl mx-auto rounded-3xl">
//         <div className="text-start rounded-md">
//           <div className="flex">
//             <h1 className="text-6xl font-semibold text-violet-600 border-slate-500">
//               {title}
//               <span className="text-slate-500"> Jobs</span>
//             </h1>
//             <h1 className="text-6xl font-bold text-lime-500">:</h1>
//           </div>
//           <p className="text-green-800 mt-5 text-2xl text-slate-400 font-medium">
//           {/* <p className="text-green-800 mt-5 text-1xl text-lime-200 font-semibold"> */}
//           Discover the best technologies jobs in all of Oceania.
//           </p>
//         </div>
//       </div>
//     </header>
//   );
// };

// export default SearchPageHeader;
