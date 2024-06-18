// src/components/ProductHuntClone.js

import React from "react";

const ProductHuntClone = () => {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* Navbar */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="text-2xl font-bold text-red-600">P</div>
              <div className="ml-10 flex items-baseline space-x-4">
                <a
                  href="#"
                  className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Launches
                </a>
                <a
                  href="#"
                  className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Products
                </a>
                <a
                  href="#"
                  className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  News
                </a>
                <a
                  href="#"
                  className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Community
                </a>
                <a
                  href="#"
                  className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Advertise
                </a>
              </div>
            </div>
            <div>
              <a
                href="#"
                className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Sign In
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 flex">
        {/* Product List */}
        <div className="flex-1">
          <h1 className="text-2xl font-bold mb-4">
            Top Products Launching Today
          </h1>
          <ul>
            <li className="bg-white p-4 rounded-lg shadow mb-4">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-xl font-bold">MARSS TTS</h2>
                  <p className="text-gray-600">
                    Open-source, insanely prosodic text-to-speech model
                  </p>
                </div>
                <div className="text-right">
                  <span className="text-gray-600">239</span>
                  <button className="ml-2 bg-gray-200 rounded px-2 py-1">
                    ↑
                  </button>
                </div>
              </div>
            </li>
            {/* Repeat the above <li> for each product */}
          </ul>
        </div>

        {/* Sidebar */}
        <aside className="w-64 ml-6">
          <h2 className="text-xl font-bold mb-4">Recent Shoutouts</h2>
          <ul>
            <li className="bg-white p-4 rounded-lg shadow mb-4">
              <h3 className="font-bold">CandiView</h3>
              <p className="text-gray-600">
                AI CV screener to efficiently find top talent
              </p>
            </li>
            {/* Repeat the above <li> for each shoutout */}
          </ul>
        </aside>
      </main>
    </div>
  );
};

export default ProductHuntClone;
