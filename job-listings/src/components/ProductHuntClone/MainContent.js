// src/components/MainContent.js

import React from "react";
// import ProductCard from "./ProductCard";
import ProductCard from "./ProductCard";
import ShoutoutCard from "./ShoutOutCard";
import WelcomeBanner from "./WelcomeBanner";

const MainContent = ({ products, shoutouts }) => {
  return (
    <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 flex">
      {/* Main Content Area */}
      <div className="flex-1">
        <WelcomeBanner />
        <h1 className="text-2xl font-bold mb-4">
          Top Products Launching Today
        </h1>
        <ul>
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </ul>
      </div>

      {/* Sidebar */}
      <aside className="w-64 ml-6">
        <h2 className="text-xl font-bold mb-4">Recent Shoutouts</h2>
        <ul>
          {shoutouts.map((shoutout) => (
            <ShoutoutCard key={shoutout.id} shoutout={shoutout} />
          ))}
        </ul>
      </aside>
    </main>
  );
};

export default MainContent;
