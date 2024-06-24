import React from "react";
import sleekDoodle from "../assets/doodles/SleekDoodle.png";
import DancingDoodle from "../assets/doodles/DancingDoodle.png";

const BottomContainer = () => {
  return (
    <header
      className="text-center py-4 mb-4 rounded-lg shadow-lg max-w-8xl mx-auto bg-violet-400 opacity-90"
      // className="text-center py-2 mb-2"
    >
      <div className="flex justify-center items-center space-x-4">
        <div className="flex flex-col items-center">
          <img alt="" src={DancingDoodle} className="h-60 mb-2" />
        </div>
        <div className="text-center p-3 ml-10 rounded-md space-x-12">
          <div className="flex">
            <h1 className="text-5xl font-bold text-lime-300">
              Oceania's Best <br></br>Technology Talent!
            </h1>
          </div>
          <div className="mt-4 border border-green-900 rounded-3xl max-w-md items-center bg-lime-400 items-center">
            <p className="text-white pt-2 pb-2 text-xl font-bold text-green-800">
              {"-> "} EXPLORE OCEANIADEVS
            </p>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <img alt="" src={sleekDoodle} className="h-60 mb-2" />
        </div>
      </div>
    </header>
  );
};

export default BottomContainer;
