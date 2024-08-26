import React from 'react';
import Logo from './Logo';

const NavbarOnboarding = ({ onNavigateAway }) => {
  return (
    <nav className="bg-white shadow-md py-4">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Logo className="h-12 w-auto cursor-pointer" alt="Logo" onClick={onNavigateAway} />
            <span className="ml-2 text-xl font-semibold text-slate-600 cursor-pointer" onClick={onNavigateAway}>OceaniaDevs</span>
          </div>
          <div className="text-sm font-medium text-gray-500">
            Recruiter Onboarding
          </div>
        </div>
      </div>
    </nav>
  );
};

export default NavbarOnboarding;