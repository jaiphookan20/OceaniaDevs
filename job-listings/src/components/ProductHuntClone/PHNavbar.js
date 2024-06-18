// src/components/Navbar.js

import React from "react";

const PHNavbar = () => {
  return (
    <nav className="bg-white shadow-md">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center h-16">
        <div className="flex items-center">
          <div className="text-2xl font-bold text-red-600">P</div>
          <div className="ml-10 flex items-baseline space-x-4">
            <a href="#" className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium">Launches</a>
            <a href="#" className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium">Products</a>
            <a href="#" className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium">News</a>
            <a href="#" className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium">Community</a>
            <a href="#" className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium">Advertise</a>
          </div>
        </div>
        <div>
          <a href="#" className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium">Sign In</a>
        </div>
      </div>
    </div>
  </nav>
  );
};

export default PHNavbar;
