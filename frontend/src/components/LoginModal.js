import React from 'react';
import { X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Logo from './Logo';

const LoginModal = ({ isOpen, onClose }) => {
  const navigate = useNavigate();

  if (!isOpen) return null;

  const handleLogin = () => {
    // navigate('/login/seeker');
    window.location.href = "/login/seeker";
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" style={{fontFamily: "Avenir, san-serif"}}>
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md">
        <div className="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 className="text-2xl font-medium text-slate-700 text-center">Log in to continue</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X size={24} />
          </button>
        </div>
        <div className="p-6">
          <p className="text-gray-600 mb-6">You need to log in or sign up to use this feature.</p>
          <div className="space-y-6">
            <div className="flex items-center">
              <div className="bg-blue-100 rounded-full p-2 mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold text-slate-700 text-lg text-md mb-1" >Your own dashboard</h3>
                <p className="text-sm text-gray-600">Keep track of your applications and save content to your dashboard.</p>
              </div>
            </div>
            <div className="flex items-center">
              <div className="bg-purple-100 rounded-full p-2 mr-4 mb-1">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold text-slate-700  text-lg" >Personalised alerts</h3>
                <p className="text-sm text-gray-600">Get instant notifications about new opportunities in your area of interest.</p>
              </div>
            </div>
            <div className="flex items-center">
              <div className="bg-green-100 rounded-full p-2 mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold text-slate-700  text-lg mb-1" >Latest advice</h3>
                <p className="text-sm text-gray-600">We'll keep you up-to-date with the latest articles and advice relevant to you.</p>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-gray-50 px-6 py-4 rounded-b-lg">
          <button
            onClick={handleLogin}
            className="w-full bg-teal-600 text-white py-2 px-4 rounded-md font-semibold hover:bg-blue-700 transition duration-300"
          >
            Log in
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginModal;