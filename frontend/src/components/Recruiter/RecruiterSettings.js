import React, { useState, useEffect } from 'react';
import { ChevronDown, Upload } from 'lucide-react';
import settingsIcon from "../../assets/settings-icon.svg";
import { toast } from 'react-hot-toast';

const australianCities = [
  'Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast',
  'Newcastle', 'Canberra', 'Geelong', 'Hobart', 'Townsville', 'Cairns', 'Darwin'
];

export default function RecruiterSettings() {
  const [personalInfo, setPersonalInfo] = useState({
    firstName: '',
    lastName: '',
    email: '',
    mobile: '',
    position: '',
  });

  const [employerInfo, setEmployerInfo] = useState({
    employerName: '',
    country: '',
    employerSize: '',
    website: '',
    address: '',
    description: '',
    type: '',
    city: '',
    state: '',
    industry: '',
  });

  const [logo, setLogo] = useState(null);
  const [logoPreview, setLogoPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchRecruiterData();
  }, []);

  const fetchRecruiterData = async () => {
    try {
      const response = await fetch('/api/recruiter_info', {
        method: 'GET',
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setPersonalInfo(data.personal_info);
        setEmployerInfo(data.employer_info);
        if (data.employer_info.logo_url) {
          setLogoPreview(data.employer_info.logo_url);
        }
      } else {
        toast.error('Failed to fetch recruiter data');
      }
    } catch (error) {
      console.error('Error fetching recruiter data:', error);
      toast.error('An error occurred while fetching data');
    }
  };

  const handlePersonalInfoChange = (e) => {
    setPersonalInfo({ ...personalInfo, [e.target.name]: e.target.value });
  };

  const handleEmployerInfoChange = (e) => {
    const { name, value } = e.target;
    if (name === 'description' && value.length > 200) return;
    setEmployerInfo({ ...employerInfo, [name]: value });
  };

  const handleLogoUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setLogo(file);
      const reader = new FileReader();
      reader.onload = (e) => setLogoPreview(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const handleSubmitPersonalInfo = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('/api/update_recruiter_info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(personalInfo),
        credentials: 'include',
      });
      if (response.ok) {
        toast.success('Personal information updated successfully');
      } else {
        toast.error('Failed to update personal information');
      }
    } catch (error) {
      console.error('Error updating personal info:', error);
      toast.error('An error occurred while updating');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitEmployerInfo = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const formData = new FormData();
      Object.keys(employerInfo).forEach(key => {
        formData.append(key, employerInfo[key]);
      });
      if (logo) {
        formData.append('logo', logo);
      }

      const response = await fetch('/api/update_recruiter_company', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });
      if (response.ok) {
        toast.success('Employer information updated successfully');
      } else {
        toast.error('Failed to update employer information');
      }
    } catch (error) {
      console.error('Error updating employer info:', error);
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
                <p className="mt-4 max-w-2xl text-lg text-slate-400" style={{fontFamily:"Avenir, san-serif"}}>Update your personal & employer details here</p>
              </div>
            </div>
          </div>
          <img src={settingsIcon} alt="settings-icon" className="max-h-16" />
        </div>
      </header>
      
      <div className="p-6 space-y-6 bg-teal-100" style={{fontFamily: "Avenir, san-serif"}}>
        <form onSubmit={handleSubmitPersonalInfo} className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">First name</label>
              <input
                type="text"
                name="firstName"
                value={personalInfo.firstName}
                onChange={handlePersonalInfoChange}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Last name</label>
              <input
                type="text"
                name="lastName"
                value={personalInfo.lastName}
                onChange={handlePersonalInfoChange}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={personalInfo.email}
                readOnly
                className="w-full p-2 border border-gray-300 rounded-md bg-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Mobile number</label>
              <input
                type="tel"
                name="mobile"
                value={personalInfo.mobile}
                onChange={handlePersonalInfoChange}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Position</label>
              <input
                type="text"
                name="position"
                value={personalInfo.position}
                onChange={handlePersonalInfoChange}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
          </div>
          <button type="submit" disabled={loading} className="mt-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
            {loading ? 'Saving...' : 'Save profile'}
          </button>
        </form>

        <form onSubmit={handleSubmitEmployerInfo} className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Employer Settings</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Employer name</label>
              <input
                type="text"
                name="employerName"
                value={employerInfo.employerName}
                readOnly
                className="w-full p-2 border border-gray-300 rounded-md bg-gray-100"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Country</label>
                <div className="relative">
                  <select
                    name="country"
                    value={employerInfo.country}
                    onChange={handleEmployerInfoChange}
                    className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                  >
                    <option value="Australia">Australia</option>
                    <option value="New Zealand">New Zealand</option>
                  </select>
                  <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Employer size</label>
                <div className="relative">
                  <select
                    name="employerSize"
                    value={employerInfo.employerSize}
                    onChange={handleEmployerInfoChange}
                    className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                  >
                    <option value="1-50 employees">1-50 employees</option>
                    <option value="51-200 employees">51-200 employees</option>
                    <option value="201-500 employees">201-500 employees</option>
                    <option value="501-1,000 employees">501-1,000 employees</option>
                    <option value="1,001-5,000 employees">1,001-5,000 employees</option>
                    <option value="5001-10,000 employees">5001-10,000 employees</option>
                    <option value="10,001+ employees">10,001+ employees</option>
                  </select>
                  <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                </div>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Employer website</label>
              <input
                type="url"
                name="website"
                value={employerInfo.website}
                onChange={handleEmployerInfoChange}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>
            {/* <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Employer address</label>
              <input
                type="text"
                name="address"
                value={employerInfo.address}
                onChange={handleEmployerInfoChange}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div> */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Agency or Company</label>
              <div className="relative">
                <select
                  name="type"
                  value={employerInfo.type}
                  onChange={handleEmployerInfoChange}
                  className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                >
                  <option value="Agency">Agency</option>
                  <option value="Company">Company</option>
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
                <div className="relative">
                  <select
                    name="city"
                    value={employerInfo.city}
                    onChange={handleEmployerInfoChange}
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
                    value={employerInfo.state}
                    onChange={handleEmployerInfoChange}
                    className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                  >
                    <option value="VIC">VIC</option>
                    <option value="NSW">NSW</option>
                    <option value="QLD">QLD</option>
                    <option value="WA">WA</option>
                    <option value="SA">SA</option>
                    <option value="TAS">TAS</option>
                    <option value="ACT">ACT</option>
                    <option value="NT">NT</option>
                  </select>
                  <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                </div>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
              <div className="relative">
                <select
                  name="industry"
                  value={employerInfo.industry}
                  onChange={handleEmployerInfoChange}
                  className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                >
                  <option value="">Select an industry</option>
                  <option value="Government">Government</option>
                  <option value="Banking & Financial Services">Banking & Financial Services</option>
                  <option value="Fashion">Fashion</option>
                  <option value="Mining">Mining</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="IT - Software Development">IT - Software Development</option>
                  <option value="IT - Data Analytics">IT - Analytics</option>
                  <option value="IT - Cybersecurity">IT - Cybersecurity</option>
                  <option value="IT - Cloud Computing">IT - Cloud Computing</option>
                  <option value="IT - Artificial Intelligence">IT - Artificial Intelligence</option>
                  <option value="Agriculture">Agriculture</option>
                  <option value="Automotive">Automotive</option>
                  <option value="Construction">Construction</option>
                  <option value="Education">Education</option>
                  <option value="Energy & Utilities">Energy & Utilities</option>
                  <option value="Entertainment">Entertainment</option>
                  <option value="Hospitality & Tourism">Hospitality & Tourism</option>
                  <option value="Legal">Legal</option>
                  <option value="Manufacturing">Manufacturing</option>
                  <option value="Marketing & Advertising">Marketing & Advertising</option>
                  <option value="Media & Communications">Media & Communications</option>
                  <option value="Non-Profit & NGO">Non-Profit & NGO</option>
                  <option value="Pharmaceuticals">Pharmaceuticals</option>
                  <option value="Real Estate">Real Estate</option>
                  <option value="Retail & Consumer Goods">Retail & Consumer Goods</option>
                  <option value="Telecommunications">Telecommunications</option>
                  <option value="Transportation & Logistics">Transportation & Logistics</option>
                </select>
                <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Employer description</label>
              <textarea
                name="description"
                value={employerInfo.description}
                onChange={handleEmployerInfoChange}
                className="w-full p-2 border border-gray-300 rounded-md"
                rows="4"
                maxLength="200"
              ></textarea>
              <p className="text-sm text-gray-500 mt-1">
                {employerInfo.description.length} / 200 characters
              </p>
            </div>
          </div>
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-2">Employer logo</h3>
            <p className="text-sm text-gray-600 mb-4">Acceptable file types: .jpg, .jpeg, .png</p>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
              {logoPreview ? (
                <img src={logoPreview} alt="Employer logo" className="max-w-full h-auto mx-auto mb-4" />
              ) : (
                <Upload className="mx-auto text-gray-400" size={48} />
              )}
              <p className="mt-2 text-sm text-gray-600">Upload Logo</p>
              <p className="text-xs text-gray-500">Simply drag and drop</p>
              <p className="text-xs text-gray-500">- or -</p>
              <label className="mt-2 inline-block px-4 py-2 bg-green-600 text-white rounded-md cursor-pointer hover:bg-green-700">
                Click to Upload
                <input
                  type="file"
                  className="hidden"
                  onChange={handleLogoUpload}
                  accept=".jpg,.jpeg,.png"
                />
              </label>
            </div>
          </div>
          <button type="submit" disabled={loading} className="mt-6 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">
            {loading ? 'Saving...' : 'Save settings'}
          </button>
        </form>
      </div>
    </div>
  );
}
                  