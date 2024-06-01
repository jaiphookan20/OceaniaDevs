import React from "react";

const Header = () => {
  return (
    <header
      className="text-center py-12 mb-8 opacity-75 rounded-lg shadow-lg"
      style={{
        // backgroundImage: `url("https://images.unsplash.com/photo-1604076913837-52ab5629fba9?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")`,
        backgroundImage: `url("https://images.unsplash.com/photo-1604076913837-52ab5629fba9?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")`,
        //https://images.unsplash.com/photo-1604076913837-52ab5629fba9?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className="flex justify-center items-center space-x-4">
        <div className="flex flex-col items-center">
          {/* <img
            src="https://path.to/your/image1.png"
            alt="Image 1"
            className="w-24 h-24 mb-2"
          />
          <img
            src="https://path.to/your/image2.png"
            alt="Image 2"
            className="w-24 h-24 mb-2"
          /> */}
        </div>
        <div className="text-center text-white p-3 rounded-md">
          <h1 className="text-6xl font-bold ">Find what's next:</h1>
          <p className="text-white mt-5 text-1xl">
            OVER 130K REMOTE & LOCAL STARTUP JOBS
          </p>
        </div>
        <div className="flex flex-col items-center">
          {/* <img
            src="https://path.to/your/image3.png"
            alt="Image 3"
            className="w-24 h-24 mb-2"
          />
          <img
            src="https://path.to/your/image4.png"
            alt="Image 4"
            className="w-24 h-24 mb-2"
          /> */}
        </div>
      </div>
    </header>
  );
};

export default Header;
