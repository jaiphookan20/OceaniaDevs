import React, { useState } from 'react';
import { ChevronDown, Upload } from 'lucide-react';
import settingsIcon from "../assets/settings-icon.svg"

export default function RecruiterSettings() {
  const [employerName, setEmployerName] = useState('OceaniaDevsxxx');
  const [country, setCountry] = useState('Australia');
  const [employerSize, setEmployerSize] = useState('5001-10,000 employees');
  const [website, setWebsite] = useState('https://jal-portfolio.vercel.app/');
  const [address, setAddress] = useState('Melbourne, Victoria');
  const [description, setDescription] = useState('Hi There asfdghasghjgaighghai aggagao aofoaogaob afoaogao. agaogoagoaa. aggaga. agaga aggaaga agagialgagaigalaga agaigaig ag agi ag ag iag agi ag gig aig');
  const [agencyOrCompany, setAgencyOrCompany] = useState('Company');
  const [city, setCity] = useState('Melbourne');
  const [state, setState] = useState('Victoria');
  const [logo, setLogo] = useState(null);
  const [firstName, setFirstName] = useState('Thorgan');
  const [lastName, setLastName] = useState('Hazard');
  const [email, setEmail] = useState('jphookan@student.unimelb.edu.au');
  const [mobile, setMobile] = useState('0411687311');
  const [position, setPosition] = useState('Director');

  const handleLogoUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => setLogo(e.target.result);
      reader.readAsDataURL(file);
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
                  <p className="mt-4 max-w-2xl text-lg text-slate-400" style={{fontFamily:"Avenir, san-serif"}}>Update your personal & employer details here</p>
                </div>
              </div>
            </div>
            <img src={settingsIcon} alt="bookmark-icon" className="max-h-16" />
          </div>
        </header>
    <div className="p-6 space-y-6 bg-teal-100" style={{fontFamily: "Avenir, san-serif"}}>
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">First name</label>
            <input
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Last name</label>
            <input
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Mobile number</label>
            <input
              type="tel"
              value={mobile}
              onChange={(e) => setMobile(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Position</label>
            <input
              type="text"
              value={position}
              onChange={(e) => setPosition(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
        </div>
        <button className="mt-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
          Save profile
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Employer Settings</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Employer name</label>
            <input
              type="text"
              value={employerName}
              readOnly
              className="w-full p-2 border border-gray-300 rounded-md bg-gray-100"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Country</label>
              <div className="relative">
                <select
                  value={country}
                  onChange={(e) => setCountry(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                >
                  <option>Australia</option>
                  <option>United States</option>
                  <option>United Kingdom</option>
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Employer size</label>
              <div className="relative">
                <select
                  value={employerSize}
                  onChange={(e) => setEmployerSize(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                >
                  <option>1-50 employees</option>
                  <option>51-200 employees</option>
                  <option>201-500 employees</option>
                  <option>501-1,000 employees</option>
                  <option>1,001-5,000 employees</option>
                  <option>5001-10,000 employees</option>
                  <option>10,001+ employees</option>
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              </div>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Employer website</label>
            <input
              type="url"
              value={website}
              onChange={(e) => setWebsite(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Employer address</label>
            <input
              type="text"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Agency or Company ?</label>
            <div className="relative">
              <select
                value={agencyOrCompany}
                onChange={(e) => setAgencyOrCompany(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md appearance-none"
              >
                <option>Agency</option>
                <option>Company</option>
              </select>
              <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
              <input
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
              <input
                type="text"
                value={state}
                onChange={(e) => setState(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Employer description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md"
              rows="4"
            ></textarea>
            <p className="text-sm text-gray-500 mt-1">
              {description.length} characters | minimum 150 characters
            </p>
          </div>
        </div>
        <button className="mt-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
          Save settings
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Employer Logo</h2>
        <p className="text-sm text-gray-600 mb-4">Acceptable file types: .jpg, .jpeg, .png</p>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
          {logo ? (
            <img src={logo} alt="Employer logo" className="max-w-full h-auto mx-auto" />
          ) : (
            <div>
              <Upload className="mx-auto text-gray-400" size={48} />
              <p className="mt-2 text-sm text-gray-600">Upload Logo</p>
              <p className="text-xs text-gray-500">Simply drag and drop</p>
              <p className="text-xs text-gray-500">- or -</p>
              <label className="mt-2 inline-block px-4 py-2 bg-green-600 text-white rounded-md cursor-pointer hover:bg-green-700">
                Click to Upload
                <input type="file" className="hidden" onChange={handleLogoUpload} accept=".jpg,.jpeg,.png" />
              </label>
            </div>
          )}
        </div>
        <button className="mt-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
          Save logo
        </button>
      </div>
    </div>
        </div>
  );
}