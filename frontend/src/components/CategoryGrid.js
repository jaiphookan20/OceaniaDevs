// src/components/CategoryGrid.js
import React from "react";

const categories = [
  {
    name: "Cloud & Infrastructure",
    icon_src:
      "https://img.icons8.com/?size=100&id=QoW2VGtyGuam&format=png&color=000000",
  },
  {
    name: "DevOps",
    icon_src:
      "https://img.icons8.com/?size=100&id=ZKGrw50bXqFY&format=png&color=000000",
  },
  {
    name: "Backend",
    icon_src: "https://img.icons8.com/isometric/50/database.png",
  },
  {
    name: "Frontend",
    icon_src:
      "https://img.icons8.com/?size=100&id=SV6flSJbrGas&format=png&color=000000",
  },
  {
    name: "Full-stack",
    icon_src:
      "https://img.icons8.com/?size=100&id=bvFBPhLHSd1d&format=png&color=000000",
  },
  {
    name: "Mobile",
    icon_src:
      "https://img.icons8.com/?size=100&id=HPFbJp6AxuXZ&format=png&color=000000",
  },
  {
    name: "UI/UX",
    icon_src:
      "https://img.icons8.com/?size=100&id=VUOjknEch1my&format=png&color=000000",
  },
  {
    name: "Data Science",
    icon_src:
      "https://img.icons8.com/?size=100&id=GV2zTy85vv6i&format=png&color=000000",
  },
];

const CategoryGrid = () => {
  return (
    <div>
      <div className="mb-8 rounded-lg max-w-7xl mx-auto">
        {/* <h2
          className="text-3xl font-bold"
          style={{ fontFamily: "Roobert-Regular, sans-serif" }}
        >
          Search By Job Family
        </h2> */}
      </div>
      <div
        className="grid grid-cols-4 gap-2 bg-white rounded-3xl max-w-7xl mx-auto mb-12"
        style={{ fontFamily: "HeyWow, sans-serif" }}
      >
        {categories.map((category) => (
          <a
            href="#"
            className="flex items-center p-4 bg-lime-100 border border-lime-300 rounded-3xl shadow-sm hover:shadow-md hover:bg-lime-300"
            key={category.name}
            style={{ width: "300px" }}
          >
            <img
              width="50"
              height="50"
              src={category.icon_src}
              alt={category.name}
            />
            <span className="text-lg font-medium pl-6">{category.name}</span>
          </a>
        ))}
      </div>
    </div>
  );
};

export default CategoryGrid;
