// src/components/ShoutoutCard.js

import React from "react";

const ShoutoutCard = ({ shoutout }) => {
  return (
    <li className="bg-white p-4 rounded-lg shadow mb-4">
      <h3 className="font-bold">{shoutout.title}</h3>
      <p className="text-gray-600">{shoutout.description}</p>
      <p className="text-sm text-gray-500">{shoutout.details}</p>
    </li>
  );
};

export default ShoutoutCard;
