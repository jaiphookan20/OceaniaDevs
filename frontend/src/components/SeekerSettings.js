import React, { useState, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';
import settingsIcon from "../assets/settings-icon.svg";
import { toast } from 'react-hot-toast';

const australianCities = [
  'Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast',
  'Newcastle', 'Canberra', 'Geelong', 'Hobart', 'Townsville', 'Cairns', 'Darwin'
];

const australianStates = ['VIC', 'NSW', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT'];

export default function SeekerSettings() {
  const [seekerInfo, setSeekerInfo] = useState({
    firstName: '',
    lastName: '',
    email: '',
    city: '',
    state: '',
    country: '',
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchSeekerData();
  }, []);

  const fetchSeekerData = async () => {
    try {
      const response = await fetch('/api/seeker_info', {
        method: 'GET',
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setSeekerInfo(data);
      } else {
        toast.error('Failed to fetch seeker data');
      }
    } catch (error) {
      console.error('Error fetching seeker data:', error);
      toast.error('An error occurred while fetching data');
    }
  };

  const handleInfoChange = (e) => {
    setSeekerInfo({ ...seekerInfo, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('/api/update_seeker', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(seekerInfo),
        credentials: 'include',
      });
      if (response.ok) {
        toast.success('Seeker information updated successfully');
      } else {
        toast.error('Failed to update seeker information');
      }
    } catch (error) {
      console.error('Error updating seeker info:', error);
      toast.error('An error occurred while updating');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='max-w-4xl mx-auto'>
      <header className="mb-8">
        <div className="flex justify-between items-center p-3 space-x-4 border-t border-b border-slate-200">
          <div className="ml-2 rounded-full">
            <div className="sm:flex sm:items-center sm:justify-between p-2">
              <div>
                <h1 className="text-6xl font-bold text-slate-600 sm:text-5xl bg-clip-text" style={{fontFamily:"Roobert-Regular, san-serif"}}>Settings & Privacy</h1>
                <p className="mt-4 max-w-2xl text-lg text-slate-400" style={{fontFamily:"Avenir, san-serif"}}>Update your personal details here</p>
              </div>
            </div>
          </div>
          <img src={settingsIcon} alt="settings-icon" className="max-h-16" />
        </div>
      </header>
      
      <div className="p-6 space-y-6 bg-teal-100" style={{fontFamily: "Avenir, san-serif"}}>
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">First name</label>
              <input
                type="text"
                name="firstName"
                value={seekerInfo.firstName}
                onChange={handleInfoChange}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Last name</label>
              <input
                type="text"
                name="lastName"
                value={seekerInfo.lastName}
                onChange={handleInfoChange}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={seekerInfo.email}
                readOnly
                className="w-full p-2 border border-gray-300 rounded-md bg-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
              <div className="relative">
                <select
                  name="city"
                  value={seekerInfo.city}
                  onChange={handleInfoChange}
                  className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                >
                  <option value="">Select a city</option>
                  {australianCities.map(city => (
                    <option key={city} value={city}>{city}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
              <div className="relative">
                <select
                  name="state"
                  value={seekerInfo.state}
                  onChange={handleInfoChange}
                  className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                >
                  <option value="">Select a state</option>
                  {australianStates.map(state => (
                    <option key={state} value={state}>{state}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Country</label>
              <div className="relative">
                <select
                  name="country"
                  value={seekerInfo.country}
                  onChange={handleInfoChange}
                  className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                >
                  <option value="Australia">Australia</option>
                  <option value="New Zealand">New Zealand</option>
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              </div>
            </div>
          </div>
          <button type="submit" disabled={loading} className="mt-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
            {loading ? 'Saving...' : 'Save profile'}
          </button>
        </form>
      </div>
    </div>
  );
}