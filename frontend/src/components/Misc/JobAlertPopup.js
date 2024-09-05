import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Logo from './Logo';
import TechnologyDropdown from './TechnologyDropdown';

const cities = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Newcastle', 'Canberra', 'Geelong', 'Hobart', 'Townsville', 'Cairns', 'Darwin'];
const specializations = ['Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing', 'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity'];
const experienceLevels = ['Junior', 'Mid-Level', 'Senior', 'Executive'];
const flexibilities = ['Remote', 'Hybrid', 'Office', 'Any'];

const JobAlertPopup = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [selectedTech, setSelectedTech] = useState([]);
  const [location, setLocation] = useState('');
  const [flexibility, setFlexibility] = useState('');
  const [specialization, setSpecialization] = useState([]);
  const [experience, setExperience] = useState('');

  const currentLocation = useLocation();

  useEffect(() => {
    const timer = setTimeout(() => {
      if (currentLocation.pathname === '/' || currentLocation.pathname === '/search-page') {
        setIsVisible(true);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [currentLocation]);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ name, email, selectedTech, location, flexibility, specialization, experience });
    setIsVisible(false);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center p-4">
      <div className="bg-gray-900 text-white p-8 rounded-xl shadow-2xl w-[800px] max-h-[600px] overflow-y-auto relative">
        <button
          onClick={() => setIsVisible(false)}
          className="absolute top-4 right-4 text-gray-400 hover:text-white text-xl"
        >
          ×
        </button>
        <div className="flex items-center mb-6">
          <Logo height={40} />
          <h2 className="text-2xl font-bold ml-4">Receive daily emails for new remote jobs</h2>
        </div>
        <p className="mb-6 text-gray-300">Receive daily emails whenever new remote jobs matching your criteria are posted.</p>
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-1">Your Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full p-2 bg-gray-800 rounded text-white"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 bg-gray-800 rounded text-white"
              required
            />
          </div>
          <div className="col-span-2">
            <label className="block text-sm font-medium mb-1">Tech Stack (Choose up to 5)</label>
            <TechnologyDropdown
              selectedTechnologies={selectedTech}
              setSelectedTechnologies={setSelectedTech}
              maxSelections={5}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Location</label>
            <select
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full p-2 bg-gray-800 rounded text-white"
            >
              <option value="">Select Location</option>
              {cities.map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Flexibility</label>
            <select
              value={flexibility}
              onChange={(e) => setFlexibility(e.target.value)}
              className="w-full p-2 bg-gray-800 rounded text-white"
            >
              <option value="">Select Flexibility</option>
              {flexibilities.map(flex => (
                <option key={flex} value={flex}>{flex}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Specialization</label>
            <TechnologyDropdown
              selectedTechnologies={specialization}
              setSelectedTechnologies={setSpecialization}
              options={specializations}
              placeholder="Select Specialization"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Experience</label>
            <select
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
              className="w-full p-2 bg-gray-800 rounded text-white"
            >
              <option value="">Select Experience Level</option>
              {experienceLevels.map(level => (
                <option key={level} value={level}>{level}</option>
              ))}
            </select>
          </div>
          <div className="col-span-2 flex justify-between items-center mt-6">
            <div className="flex items-center">
              <img src="/api/placeholder/40/40" alt="User avatars" className="rounded-full" />
              <span className="ml-2 text-sm text-gray-300">Join 30,000+ remote job seekers</span>
            </div>
            <div>
              <button type="button" onClick={() => setIsVisible(false)} className="px-4 py-2 bg-gray-700 rounded mr-2 text-sm">Cancel</button>
              <button type="submit" className="px-4 py-2 bg-purple-600 rounded text-sm">Create Job Alert</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default JobAlertPopup;