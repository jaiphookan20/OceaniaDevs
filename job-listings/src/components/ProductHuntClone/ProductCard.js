// src/components/ProductCard.js

import React from "react";

const ProductCard = ({ product }) => {
  return (
    <li className="bg-white p-4 rounded-lg shadow mb-4 flex justify-between items-center">
      <div>
        <h2 className="text-xl font-bold">{product.name}</h2>
        <p className="text-gray-600">{product.description}</p>
        <p className="text-sm text-gray-500">{product.details}</p>
      </div>
      <div className="text-right">
        <span className="text-gray-600">{product.votes}</span>
        <button className="ml-2 bg-gray-200 rounded px-2 py-1">↑</button>
      </div>
    </li>
  );
};

export default ProductCard;
