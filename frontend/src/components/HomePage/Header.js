import React from "react";
import blueSpikesIcon from "../../assets/header-blue-spikes-icon.png";
import blueVaseIcon from "../../assets/header-blue-vase-icon.png";
import greenSpikesHollowIcon from "../../assets/header-green-spikes-hollow-icon.png";
import greenSpikesIcon from "../../assets/header-green-spikes-icon.png";
import orangeSpikesIcon from "../../assets/header-orange-spikes-icon.png";
import fuchsiaSpikesIcon from "../../assets/header-orange-spikes-icon.png";
import orangeSpikesIrregularIcon from "../../assets/header-orange-spikes-irregular-icon.png";
import orangeSunHollowIcon from "../../assets/header-orange-sun-hollow-icon.png";
import pinkStreamIcon from "../../assets/header-pink-stream-icon.png";
import purpleFlowerIcon from "../../assets/header-purple-flower-icon.png";
import yellowDaisyIcon from "../../assets/header-yellow-daisy-icon.png";
import yellowStreamIcon from "../../assets/header-yellow-stream-icon.png";
import yellowSunIcon from "../../assets/header-yellow-sun-icon.png";
import blankImage from "../../assets/header-blank-image-slate.png";

const Header = () => {
  return (
    <header className="text-center py-12 mb-2 rounded-sm max-w-6xl mx-auto bg-gradient-to-r from-purple-400 via-lime-500 to-fuchsia-400">
      {/* bg-[#c3f53c] */}
      <div className="flex justify-between items-center">
        {/* <div className="flex justify-center items-center space-x-4"> */}
        {/* <div className="grid grid-cols-3 grid-rows-2 gap-4">
          <img src={blueSpikesIcon} className="w-20 h-28" />
          <img src={face2} className="w-20 h-28" />
          <img src={blankImage} className="w-20 h-28" />
          <img src={face2} className="w-20 h-28" />
          <img src={orangeSpikesIcon} className="w-20 h-28" />
          <img src={blankImage} className="w-20 h-28" />
          <img src={purpleFlowerIcon} className="w-20 h-28" />
          <img src={face4} className="w-20 h-28" />
          <img src={blankImage} className="w-20 h-28" />
          <img src={hero5} className="w-20 h-28" />
        </div> */}
        <div className="mx-auto text-center rounded-lg">
          <div className="flex">
          <h1 className="text-7xl font-bold text-white ">
            {/* <h1 className="text-6xl font-bold text-lime-500 "> */}
              Find your next
            </h1>
            <h1 className="text-6xl font-bold text-lime-400">:</h1>
          </div>
          <p className="text-green-800 mt-5 text-1xl text-white font-semibold">
          {/* <p className="text-green-800 mt-5 text-1xl text-lime-200 font-semibold"> */}
            THE BEST TECHNOLOGY JOBS, DOWN UNDER
          </p>
        </div>
        {/* <div className="grid grid-cols-3 grid-rows-2 gap-2">
          <img src={orangeSpikesIcon} className="w-20 h-28" />
          <img src={face3} className="w-20 h-28" />
          <img src={blankImage} className="w-20 h-28" />
          <img src={blueVaseIcon} className="w-20 h-28" />
          <img src={blankImage} className="w-20 h-28" />
          <img src={pinkStreamIcon} className="w-20 h-28" />
          <img src={blankImage} className="w-20 h-28" />
          <img src={face1} className="w-20 h-28" />
        </div> */}
      </div>
    </header>
  );
};

export default Header;
