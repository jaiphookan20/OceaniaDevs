import React from 'react';

const RecruiterHiringSteps = () => {
  return (
    <div className="w-full bg-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Start hiring in 3 simple steps
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            {
              number: 1,
              title: 'Register securely online',
              description: 'Create and verify an account with your email address'
            },
            {
              number: 2,
              title: 'Post your job ad',
              description: 'Our step-by-step guide helps you create a great job ad'
            },
            {
              number: 3,
              title: 'Sort applications easily',
              description: 'Our tools make it easy to identify the best people for your job'
            }
          ].map((step, index) => (
            <div key={index} className="bg-pink-50 p-6 rounded-lg flex flex-col items-center text-center">
              <div className="w-12 h-12 bg-pink-500 rounded-full flex items-center justify-center text-white font-bold text-xl mb-4">
                {step.number}
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">{step.title}</h3>
              <p className="text-gray-600">{step.description}</p>
            </div>
          ))}
        </div>
        <div className="flex justify-center mt-8">
          <button className="px-6 py-3 bg-indigo-600 text-white rounded-md font-semibold hover:bg-indigo-700 transition duration-300">
            Create account
          </button>
        </div>
      </div>
    </div>
  );
};

export default RecruiterHiringSteps;