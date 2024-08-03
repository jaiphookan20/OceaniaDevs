import React from 'react';

const CompanyPageHeader = ({ heading, subheading, logoSrc }) => {
  return (
    <div className='flex items-center justify-items-center mx-auto mb-1'>
      <header className="bg-teal-50 pt-8 pl-2 pb-6 pr-20 rounded-2xl border border-teal-200 shadow-sm">
        <div className="text-left flex-grow ml-8">
          <h1 className="text-5xl text-gray-800">{heading}</h1>
          <p className="text-md text-gray-500 mt-4">{subheading}</p>
        </div>
      </header>
      <div className='bg-teal-50 p-10 rounded-2xl border border-teal-200 shadow-sm ml-2'>
        <img src={logoSrc} alt={`${heading} Logo`} className="h-24 rounded-lg" />
      </div>
    </div>
  );
};

export default CompanyPageHeader;