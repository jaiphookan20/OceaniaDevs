import React from 'react';
import { Link } from 'react-router-dom';
import doodleLaptopGuyPark from '../../assets/doodles/doodle_laptop_guy_park.webp';
import RecruiterTestimonials from './RecruiterTestimonials';
import RecruiterPostJobBox from './RecruiterPostJobBox';

const RecruiterLandingPage = () => {
  return (
    <div className="bg-white min-h-screen flex flex-col items-center">
      <div className="w-2/3 bg-teal-100 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row justify-between items-center">
            <div className="lg:w-1/2">
              <div className="text-center lg:text-left">
                <h1 className="text-4xl font-bold text-gray-900">
                  Helping you as an early careers recruiter
                </h1>
                <p className="mt-4 text-lg text-gray-600">
                  2-5x more apps generated for hirers over our nearest competitor
                </p>
              </div>
              <div className="mt-8 flex flex-col items-center lg:items-start">
                <div className="flex flex-col sm:flex-row items-center sm:space-x-4">
                  <input
                    type="email"
                    placeholder="Email address"
                    className="px-4 py-2 border border-gray-300 rounded-md w-full sm:w-auto"
                  />
                  <button className="mt-4 sm:mt-0 px-6 py-2 bg-green-500 text-white rounded-md w-full sm:w-auto">
                    Sign up
                  </button>
                </div>
                <Link to="/login" className="mt-4 text-green-500">
                  Are you an existing employer? Login
                </Link>
                <Link to="/chat" className="mt-2 text-green-500">
                  Chat with us now
                </Link>
                <p className="mt-2 text-gray-600">
                  Monday to Friday, 9am – 5pm AEST
                </p>
              </div>
            </div>
            <div className="mt-8 lg:mt-0 lg:w-1/2 flex justify-center">
              <img
                src={doodleLaptopGuyPark}
                alt="Doodle Laptop Guy Park"
                className="w-full max-w-md"
              />
            </div>
          </div>
        </div>
      </div>
      <div className="w-2/3 bg-amber-50 py-12">
        <RecruiterTestimonials />
      </div>
      <div className="w-2/3 bg-amber-50 py-12">
        <RecruiterPostJobBox />
      </div>
    </div>
  );
};

export default RecruiterLandingPage;