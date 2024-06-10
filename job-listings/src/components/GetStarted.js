import React from "react";
import bgGradient from "/Users/jai/Desktop/aus-job-board/job-listings/src/assets/bg-gradient.png";

const GetStarted = () => {
  return (
    <div className="flex justify-between items-center py-7 px-8 bg-white max-w-7xl mx-auto">
      <div
        className="flex justify-between bg-grey-100 shadow-md rounded-md bg-lime-200"
        style={{ height: "380px", width: "900px" }} //{ width: "900px",
      >
        <div className="flex-shrink-0">
          <img
            src={bgGradient}
            alt="Decorative"
            style={{ height: "380px", width: "360px" }}
          />
        </div>
        <div className="ml-8">
          <h2 className="text-3xl font-bold mb-4 mt-20">Get started today</h2>
          <p className="text-xl mb-6 pr-4">
            To apply to jobs with one-click and connect with founders and
            recruiters searching for your skills.
          </p>
          <button className="bg-black text-white py-2 px-6 rounded-lg">
            Create your profile
          </button>
        </div>
      </div>
    </div>
  );
};

export default GetStarted;
