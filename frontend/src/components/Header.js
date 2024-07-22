import React from "react";
import face1 from "../assets/face-1.png";
import face2 from "../assets/face-2.png";
import face3 from "../assets/face-3.png";
import face4 from "../assets/face-4.png";
import hero2 from "../assets/hero-2-blue.png";
import hero3 from "../assets/hero-3-orange.png";
import hero5 from "../assets/hero-purple-flower.png";
import hero6 from "../assets/hero-stream-purple.png";
import hero7 from "../assets/hero-blue-stream.png";
import hero9 from "../assets/hero-yellow-daisy.png";

const Header = () => {
  return (
    <header className="text-center py-12 mb-8 rounded-lg max-w-8xl mx-auto">
      {/* bg-[#c3f53c] */}
      <div className="flex justify-between items-center bg-fuchsia-500">
        {/* <div className="flex justify-center items-center space-x-4"> */}
        <div className="grid grid-cols-3 grid-rows-2 gap-4">
          <img src={hero7} className="w-32 h-32" />
          <img src={face2} className="w-32 h-32" />
          <img src={hero3} className="w-32 h-32" />
          <img src={face4} className="w-32 h-32" />
          <img src={hero9} className="w-32 h-32" />
          <img src={hero5} className="w-32 h-32" />
        </div>
        <div className="text-center rounded-md">
          <div className="flex">
            <h1 className="text-6xl font-bold text-lime-100 ">
              Find what's next
            </h1>
            <h1 className="text-6xl font-bold text-lime-500">:</h1>
          </div>
          <p className="text-green-800 mt-5 text-1xl text-lime-200 font-semibold">
            THE BEST TECHNOLOGY JOBS, DOWN UNDER
          </p>
        </div>
        <div className="grid grid-cols-3 grid-rows-2 gap-2">
          <img src={hero6} className="w-32 h-32" />
          <img src={face3} className="w-32 h-32" />
          <img src={hero9} className="w-32 h-32" />
          <img src={hero3} className="w-32 h-32" />
          <img src={hero2} className="w-32 h-32" />
          <img src={face1} className="w-32 h-32" />
        </div>
      </div>
    </header>
  );
};

export default Header;
