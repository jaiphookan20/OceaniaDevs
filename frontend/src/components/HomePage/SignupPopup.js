import React, { useState, useEffect } from 'react';

const SignupPopup = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [email, setEmail] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 10000);

    return () => clearTimeout(timer);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission logic here
    console.log('Email submitted:', email);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg max-w-md w-full relative">
        <button 
          onClick={() => setIsVisible(false)}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
        >
          ×
        </button>
        <h2 className="text-2xl font-serif mb-2">THURSDAY MORNINGS</h2>
        <h3 className="text-3xl font-serif font-bold mb-4">Sign up for How to Build a Life</h3>
        <p className="mb-6">
          Keep up with Arthur C. Brooks as he tackles questions of meaning and happiness in his weekly column.
        </p>
        <form onSubmit={handleSubmit} className="flex flex-col">
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="border border-gray-300 p-2 mb-4 rounded"
            required
          />
          <button
            type="submit"
            className="bg-gray-900 text-white py-2 px-4 rounded hover:bg-gray-800"
          >
            Sign Up
          </button>
        </form>
        <p className="text-xs mt-4 text-gray-600">
          By submitting your email, you agree to our Terms & Conditions and Privacy Policy.
        </p>
      </div>
      <div className="hidden md:block">
        {/* Placeholder for the iPhone image */}
        <div className="w-64 h-128 bg-gray-200 rounded-3xl ml-8"></div>
      </div>
    </div>
  );
};

export default SignupPopup;