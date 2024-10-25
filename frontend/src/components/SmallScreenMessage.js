import React from 'react';
import Logo from './HomePage/Logo';
import doodleLaptopGuyPark from '../assets/doodles/doodle_laptop_guy_park.webp';

const SmallScreenMessage = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gradient-to-b from-purple-100 to-blue-100 text-center">
      <div className="mb-6">
        <Logo width="120px" height="120px" />
      </div>
      <h1 className="text-3xl font-bold mb-4 text-purple-600">OceaniaDevs</h1>
      <img 
        src={doodleLaptopGuyPark} 
        alt="Person using laptop" 
        className="w-64 h-auto mb-6"
      />
      <p className="mb-4 text-lg text-gray-700">
        For the best experience, please view our site on a laptop or desktop computer.
      </p>
      <p className="text-gray-600">
        We're working on making our site mobile-friendly. Thank you for your patience!
      </p>
    </div>
  );
};

export default SmallScreenMessage;
