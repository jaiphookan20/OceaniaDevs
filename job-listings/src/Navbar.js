import React from "react";
import Logo from "./Logo";

const Navbar = () => {
  return (
    <nav className="flex justify-between items-center py-7 px-8 bg-white shadow-md">
      <div className="flex items-center ">
        {/* <img src="" alt="Logo" className="w-36" /> */}
        <Logo className="h-24 w-auto" alt="Logo" />
        <div className="">
          <a
            href="#"
            className="text-gray-600 font-bold text-2xl hover:text-gray-800 mr-10"
          >
            OceaniaDevs
          </a>
        </div>
        <div className="flex items-center space-x-8">
          <a href="#" className="text-gray-600 hover:text-gray-800">
            Overview
          </a>
          <a href="#" className="text-gray-600 hover:text-gray-800">
            Jobs
          </a>
          <a href="#" className="text-gray-600 hover:text-gray-800">
            Featured
          </a>
          <a href="#" className="text-gray-600 hover:text-gray-800">
            Remote
          </a>
          <a href="#" className="text-gray-600 hover:text-gray-800">
            For companies
          </a>
        </div>
      </div>
      <div className="flex items-center space-x-4">
        <button className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-100">
          Log In
        </button>
        <button className="px-4 py-2 text-white bg-black rounded-md hover:bg-violet-400">
          Sign Up
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
