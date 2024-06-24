import React from "react";

const SavedAndAppliedJobsHeader = ({ title }) => {
  return (
    <div>
      {title === "Saved Jobs" ? (
        <header className="text-center mb-4 rounded-lg shadow-lg max-w-8xl mx-auto bg-violet-700">
          <div className="flex justify-start items-center p-4 space-x-4">
            <div className="text-center ml-10 rounded-full space-x-12">
              <div className="border border-white shadow-md rounded-full max-w-md items-center bg-violet-700">
                <p className="text-violet-100 font-semibold p-3 text-4xl">
                  {title}
                </p>
              </div>
            </div>
          </div>
        </header>
      ) : (
        <header className="text-center mb-4 rounded-lg shadow-lg max-w-8xl mx-auto bg-lime-700">
          <div className="flex justify-start items-center p-4 space-x-4">
            <div className="text-center ml-10 rounded-full space-x-12">
              <div className="border border-lime-300 shadow-md rounded-full max-w-md items-center bg-lime-700">
                <p className="text-lime-100 font-semibold p-3 text-4xl">
                  {title}
                </p>
              </div>
            </div>
          </div>
        </header>
      )}
    </div>
  );
};

export default SavedAndAppliedJobsHeader;
