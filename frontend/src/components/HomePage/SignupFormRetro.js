import React from 'react';
import Logo from './Logo';

const SignupFormRetro = () => {
  return (
    <div className="m-8 max-w-6xl mx-auto border border-slate-500 shadow shadow-md" style={{fontFamily: "Retro, san-serif"}}>
      <div className="bg-violet-900 text-white p-3 flex justify-between items-center">
        <div className='flex justify-start items-center'>
            <Logo height={40}/>
            <span className="text-5xl">WARNING: Unfair Advantage</span>
        </div>
        <div className="flex space-x-2">
          <button className="bg-gray-400 text-black w-8 h-8 flex items-center justify-center text-4xl">-</button>
          <button className="bg-gray-400 text-black w-8 h-8 flex items-center justify-center text-4xl">□</button>
          <button className="bg-gray-400 text-black w-8 h-8 flex items-center justify-center text-4xl">X</button>
        </div>
      </div>
      <div className="bg-gray-300 p-10">
        <p className="text-center mb-8 text-5xl items-center">
          {/* A Brave New World Awaits You. */}
          Receive tailored job recommendations, directly in your inbox
        </p>
        <div className="flex">
          <input
            type="text"
            placeholder="alanturing@enigma.com"
            className="flex-grow bg-white border border-slate-700 px-8 py-4 text-4xl hover:cursor-pointer"
          />
          <button className="bg-violet-900 text-white px-8 py-4 ml-2 text-4xl hover:bg-teal-800 hover:cursor-pointer">
            JOIN US
          </button>
        </div>
      </div>
    </div>
  );
};

export default SignupFormRetro;