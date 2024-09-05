import React, { useState, useEffect } from 'react';
import { ChevronDown, MapPin, Mail, PenTool, Check, Upload } from 'lucide-react';

const ProfileStrengthBar = ({ strength }) => (
  <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
    <div className="bg-green-600 h-2.5 rounded-full" style={{ width: `${strength}%` }}></div>
  </div>
);

const Section = ({ title, children, isCompleted }) => (
  <div className="mb-8">
    <div className="flex items-center mb-4">
      <h2 className="text-2xl font-semibold">{title}</h2>
      {isCompleted && <Check className="ml-2 text-green-500" size={24} />}
    </div>
    {children}
  </div>
);

const EditableField = ({ value, onChange }) => (
  <div className="relative">
    <textarea
      className="w-full p-2 border rounded"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
    <PenTool className="absolute top-2 right-2 text-gray-400" size={16} />
  </div>
);

const AddButton = ({ onClick, text }) => (
  <button
    onClick={onClick}
    className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
  >
    {text}
  </button>
);

const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg w-full max-w-md">
        <h3 className="text-xl font-semibold mb-4">{title}</h3>
        {children}
      </div>
    </div>
  );
};

const AddRoleForm = ({ onClose, onSave }) => {
  const [role, setRole] = useState({
    title: '',
    company: '',
    startDate: { month: '', year: '' },
    endDate: { month: '', year: '' },
    currentlyWorking: false,
    description: ''
  });

  const handleChange = (field, value) => {
    setRole(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    onSave(role);
    onClose();
  };

  return (
    <form onSubmit={(e) => e.preventDefault()}>
      <div className="mb-4">
        <label className="block mb-2">Job title</label>
        <input
          type="text"
          className="w-full p-2 border rounded"
          value={role.title}
          onChange={(e) => handleChange('title', e.target.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block mb-2">Company name</label>
        <input
          type="text"
          className="w-full p-2 border rounded"
          value={role.company}
          onChange={(e) => handleChange('company', e.target.value)}
        />
      </div>
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block mb-2">Started</label>
          <div className="flex">
            <select
              className="w-1/2 p-2 border rounded-l"
              value={role.startDate.month}
              onChange={(e) => handleChange('startDate', { ...role.startDate, month: e.target.value })}
            >
              <option value="">Month</option>
              {/* Add month options */}
            </select>
            <select
              className="w-1/2 p-2 border rounded-r"
              value={role.startDate.year}
              onChange={(e) => handleChange('startDate', { ...role.startDate, year: e.target.value })}
            >
              <option value="">Year</option>
              {/* Add year options */}
            </select>
          </div>
        </div>
        <div>
          <label className="block mb-2">Ended</label>
          <div className="flex items-center">
            <select
              className="w-1/3 p-2 border rounded-l"
              value={role.endDate.month}
              onChange={(e) => handleChange('endDate', { ...role.endDate, month: e.target.value })}
              disabled={role.currentlyWorking}
            >
              <option value="">Month</option>
              {/* Add month options */}
            </select>
            <select
              className="w-1/3 p-2 border rounded-r"
              value={role.endDate.year}
              onChange={(e) => handleChange('endDate', { ...role.endDate, year: e.target.value })}
              disabled={role.currentlyWorking}
            >
              <option value="">Year</option>
              {/* Add year options */}
            </select>
            <label className="w-1/3 flex items-center">
              <input
                type="checkbox"
                checked={role.currentlyWorking}
                onChange={(e) => handleChange('currentlyWorking', e.target.checked)}
                className="mr-2"
              />
              Still in role
            </label>
          </div>
        </div>
      </div>
      <div className="mb-4">
        <label className="block mb-2">Description (recommended)</label>
        <textarea
          className="w-full p-2 border rounded"
          rows="4"
          value={role.description}
          onChange={(e) => handleChange('description', e.target.value)}
        ></textarea>
      </div>
      <div className="flex justify-end mt-4">
        <button onClick={onClose} className="px-4 py-2 bg-gray-200 rounded mr-2">Cancel</button>
        <button onClick={handleSave} className="px-4 py-2 bg-blue-600 text-white rounded">Save</button>
      </div>
    </form>
  );
};

const AddEducationForm = ({ onClose, onSave }) => {
  const [education, setEducation] = useState({
    degree: '',
    institution: '',
    startYear: '',
    endYear: '',
    currentlyStudying: false,
    description: ''
  });

  const handleChange = (field, value) => {
    setEducation(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    onSave(education);
    onClose();
  };

  return (
    <form onSubmit={(e) => e.preventDefault()}>
      <div className="mb-4">
        <label className="block mb-2">Degree</label>
        <input
          type="text"
          className="w-full p-2 border rounded"
          value={education.degree}
          onChange={(e) => handleChange('degree', e.target.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block mb-2">Institution</label>
        <input
          type="text"
          className="w-full p-2 border rounded"
          value={education.institution}
          onChange={(e) => handleChange('institution', e.target.value)}
        />
      </div>
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block mb-2">Started</label>
          <select
            className="w-full p-2 border rounded"
            value={education.startYear}
            onChange={(e) => handleChange('startYear', e.target.value)}
          >
            <option value="">Year</option>
            {/* Add year options */}
          </select>
        </div>
        <div>
          <label className="block mb-2">Ended</label>
          <div className="flex items-center">
            <select
              className="w-2/3 p-2 border rounded-l"
              value={education.endYear}
              onChange={(e) => handleChange('endYear', e.target.value)}
              disabled={education.currentlyStudying}
            >
              <option value="">Year</option>
              {/* Add year options */}
            </select>
            <label className="w-1/3 flex items-center ml-2">
              <input
                type="checkbox"
                checked={education.currentlyStudying}
                onChange={(e) => handleChange('currentlyStudying', e.target.checked)}
                className="mr-2"
              />
              Current
            </label>
          </div>
        </div>
      </div>
      <div className="mb-4">
        <label className="block mb-2">Description (optional)</label>
        <textarea
          className="w-full p-2 border rounded"
          rows="4"
          value={education.description}
          onChange={(e) => handleChange('description', e.target.value)}
        ></textarea>
      </div>
      <div className="flex justify-end mt-4">
        <button onClick={onClose} className="px-4 py-2 bg-gray-200 rounded mr-2">Cancel</button>
        <button onClick={handleSave} className="px-4 py-2 bg-blue-600 text-white rounded">Save</button>
      </div>
    </form>
  );
};

const AddLicenseForm = ({ onClose, onSave }) => {
  const [license, setLicense] = useState({
    name: '',
    organization: '',
    issueDate: { month: '', year: '' },
    expiryDate: { month: '', year: '' },
    noExpiry: false,
    description: ''
  });

  const handleChange = (field, value) => {
    setLicense(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    onSave(license);
    onClose();
  };

  return (
    <form onSubmit={(e) => e.preventDefault()}>
      <div className="mb-4">
        <label className="block mb-2">License name</label>
        <input
          type="text"
          className="w-full p-2 border rounded"
          placeholder="e.g. Drivers License"
          value={license.name}
          onChange={(e) => handleChange('name', e.target.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block mb-2">Issuing organization (optional)</label>
        <input
          type="text"
          className="w-full p-2 border rounded"
          value={license.organization}
          onChange={(e) => handleChange('organization', e.target.value)}
        />
      </div>
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block mb-2">Issue date (optional)</label>
          <div className="flex">
            <select
              className="w-1/2 p-2 border rounded-l"
              value={license.issueDate.month}
              onChange={(e) => handleChange('issueDate', { ...license.issueDate, month: e.target.value })}
            >
              <option value="">Month</option>
              {/* Add month options */}
            </select>
            <select
              className="w-1/2 p-2 border rounded-r"
              value={license.issueDate.year}
              onChange={(e) => handleChange('issueDate', { ...license.issueDate, year: e.target.value })}
            >
              <option value="">Year</option>
              {/* Add year options */}
            </select>
          </div>
        </div>
        <div>
          <label className="block mb-2">Expiry date (recommended)</label>
          <div className="flex items-center">
            <select
              className="w-1/3 p-2 border rounded-l"
              value={license.expiryDate.month}
              onChange={(e) => handleChange('expiryDate', { ...license.expiryDate, month: e.target.value })}
              disabled={license.noExpiry}
            >
              <option value="">Month</option>
              {/* Add month options */}
            </select>
            <select
              className="w-1/3 p-2 border"
              value={license.expiryDate.year}
              onChange={(e) => handleChange('expiryDate', { ...license.expiryDate, year: e.target.value })}
              disabled={license.noExpiry}
            >
              <option value="">Year</option>
              {/* Add year options */}
            </select>
            <label className="w-1/3 flex items-center">
              <input
                type="checkbox"
                checked={license.noExpiry}
                onChange={(e) => handleChange('noExpiry', e.target.checked)}
                className="mr-2"
              />
              No expiry
            </label>
          </div>
        </div>
      </div>
      <div className="mb-4">
        <label className="block mb-2">Description (optional)</label>
        <textarea
          className="w-full p-2 border rounded"
          rows="4"
          placeholder="Briefly describe this credential – you can also add a type or URL if applicable."
          value={license.description}
          onChange={(e) => handleChange('description', e.target.value)}
        ></textarea>
      </div>
      <div className="flex justify-end mt-4">
        <button onClick={onClose} className="px-4 py-2 bg-gray-200 rounded mr-2">Cancel</button>
        <button onClick={handleSave} className="px-4 py-2 bg-blue-600 text-white rounded">Save</button>
      </div>
    </form>
  );
};

const JobBoardProfile = () => {
  const [profileStrength, setProfileStrength] = useState(0);
  const [personalSummary, setPersonalSummary] = useState('');
  const [careerHistory, setCareerHistory] = useState([]);
  const [education, setEducation] = useState([]);
  const [licenses, setLicenses] = useState([]);
  const [resume, setResume] = useState(null);
  const [nextRole, setNextRole] = useState({
    availability: '',
    preferredWorkTypes: [],
    preferredLocations: [],
    rightToWork: '',
    salaryExpectation: '',
  });
  const [isAddRoleModalOpen, setIsAddRoleModalOpen] = useState(false);
  const [isAddEducationModalOpen, setIsAddEducationModalOpen] = useState(false);
  const [isAddLicenseModalOpen, setIsAddLicenseModalOpen] = useState(false);

  const [completedSections, setCompletedSections] = useState({
    resume: false,
    personalSummary: false,
    careerHistory: false,
    education: false,
    licenses: false,
    nextRole: false,
  });

useEffect(() => {
    // Update completed sections
    setCompletedSections({
      resume: !!resume,
      personalSummary: personalSummary.length > 0,
      careerHistory: careerHistory.length > 0,
      education: education.length > 0,
      licenses: licenses.length > 0,
      nextRole: Object.values(nextRole).some(Boolean),
    });

    // Calculate profile strength
    const completedSectionsCount = Object.values(completedSections).filter(Boolean).length;
    setProfileStrength(completedSectionsCount * (100 / 6)); // 6 is the total number of sections
  }, [resume, personalSummary, careerHistory, education, licenses, nextRole]);

  const handleAddRole = (newRole) => {
    setCareerHistory([...careerHistory, newRole]);
    setIsAddRoleModalOpen(false);
  };

  const handleAddEducation = (newEducation) => {
    setEducation([...education, newEducation]);
    setIsAddEducationModalOpen(false);
  };

  const handleAddLicense = (newLicense) => {
    setLicenses([...licenses, newLicense]);
    setIsAddLicenseModalOpen(false);
  };

  const handleResumeUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResume(file);
    } else {
      alert('Please upload a PDF file.');
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8 bg-white shadow-lg rounded-lg" style={{fontFamily: "Avenir"}}>
      <h1 className="text-3xl text-slate-700 font-semibold mb-8">Your Profile</h1>
      
      <ProfileStrengthBar strength={profileStrength} />
      
      <Section title="Resume" isCompleted={completedSections.resume}>
        {resume ? (
          <div className="p-4 border rounded">
            <p className="font-medium text-slate-700">{resume.name}</p>
            <p className="text-sm text-gray-500">Added {new Date().toLocaleString()}</p>
            <p className="mt-2">This resume is visible to employers.</p>
          </div>
        ) : (
          <div className="flex items-center justify-center w-full">
            <label className="w-full flex flex-col items-center px-4 py-6 bg-white text-blue rounded-lg shadow-lg tracking-wide uppercase border border-blue cursor-pointer hover:bg-blue hover:text-white">
              <Upload className="w-8 h-8" />
              <span className="mt-2 text-base leading-normal">Select a file</span>
              <input type='file' className="hidden" onChange={handleResumeUpload} accept=".pdf" />
            </label>
          </div>
        )}
      </Section>

      <Section title="Personal Summary" isCompleted={completedSections.personalSummary}>
        <EditableField value={personalSummary} onChange={setPersonalSummary} />
      </Section>
      
      <Section title="Career History" isCompleted={completedSections.careerHistory}>
        {careerHistory.map((job, index) => (
          <div key={index} className="mb-4 p-4 border rounded">
            <h3 className="font-semibold">{job.title}</h3>
            <p>{job.company}</p>
            <p>{job.startDate.month}/{job.startDate.year} - {job.currentlyWorking ? 'Present' : `${job.endDate.month}/${job.endDate.year}`}</p>
            <ul className="list-disc list-inside mt-2">
              {job.description.split('\n').map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
        <AddButton onClick={() => setIsAddRoleModalOpen(true)} text="Add Role" />
      </Section>
      
      <Section title="Education" isCompleted={completedSections.education}>
        {education.map((edu, index) => (
          <div key={index} className="mb-4 p-4 border rounded">
            <h3 className="font-semibold">{edu.degree}</h3>
            <p>{edu.institution}</p>
            <p>{edu.startYear} - {edu.currentlyStudying ? 'Present' : edu.endYear}</p>
            {edu.description && <p className="mt-2">{edu.description}</p>}
          </div>
        ))}
        <AddButton onClick={() => setIsAddEducationModalOpen(true)} text="Add Education" />
      </Section>

      <Section title="Licenses & Certifications" isCompleted={completedSections.licenses}>
        {licenses.map((license, index) => (
          <div key={index} className="mb-4 p-4 border rounded">
            <h3 className="font-semibold">{license.name}</h3>
            {license.organization && <p>{license.organization}</p>}
            {license.issueDate.month && license.issueDate.year && (
              <p>Issued: {license.issueDate.month}/{license.issueDate.year}</p>
            )}
            {!license.noExpiry && license.expiryDate.month && license.expiryDate.year && (
              <p>Expires: {license.expiryDate.month}/{license.expiryDate.year}</p>
            )}
            {license.noExpiry && <p>No expiration date</p>}
            {license.description && <p className="mt-2">{license.description}</p>}
          </div>
        ))}
        <AddButton onClick={() => setIsAddLicenseModalOpen(true)} text="Add License or Certification" />
      </Section>
      
      <Section title="About Your Next Role" isCompleted={completedSections.nextRole}>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block mb-2">Availability</label>
            <select 
              className="w-full p-2 border rounded"
              value={nextRole.availability}
              onChange={(e) => setNextRole({...nextRole, availability: e.target.value})}
            >
              <option value="">Select</option>
              <option value="now">Now</option>
              <option value="1month">In 1 month</option>
              <option value="3months">In 3 months</option>
            </select>
          </div>
          <div>
            <label className="block mb-2">Preferred Work Types</label>
            <select 
              className="w-full p-2 border rounded" 
              multiple
              value={nextRole.preferredWorkTypes}
              onChange={(e) => setNextRole({...nextRole, preferredWorkTypes: Array.from(e.target.selectedOptions, option => option.value)})}
            >
              <option value="fulltime">Full-time</option>
              <option value="parttime">Part-time</option>
              <option value="contract">Contract</option>
            </select>
          </div>
          <div>
            <label className="block mb-2">Preferred Locations</label>
            <select 
              className="w-full p-2 border rounded" 
              multiple
              value={nextRole.preferredLocations}
              onChange={(e) => setNextRole({...nextRole, preferredLocations: Array.from(e.target.selectedOptions, option => option.value)})}
            >
              <option value="remote">Remote</option>
              <option value="onsite">On-site</option>
              <option value="hybrid">Hybrid</option>
            </select>
          </div>
          <div>
            <label className="block mb-2">Right to Work</label>
            <select 
              className="w-full p-2 border rounded"
              value={nextRole.rightToWork}
              onChange={(e) => setNextRole({...nextRole, rightToWork: e.target.value})}
            >
              <option value="">Select</option>
              <option value="citizen">Citizen</option>
              <option value="permanent">Permanent Resident</option>
              <option value="visa">Work Visa</option>
            </select>
          </div>
          <div>
            <label className="block mb-2">Salary Expectation</label>
            <input 
              type="text" 
              className="w-full p-2 border rounded" 
              placeholder="Enter amount"
              value={nextRole.salaryExpectation}
              onChange={(e) => setNextRole({...nextRole, salaryExpectation: e.target.value})}
            />
          </div>
        </div>
      </Section>

      <Modal isOpen={isAddRoleModalOpen} onClose={() => setIsAddRoleModalOpen(false)} title="Add Role">
        <AddRoleForm onClose={() => setIsAddRoleModalOpen(false)} onSave={handleAddRole} />
      </Modal>

      <Modal isOpen={isAddEducationModalOpen} onClose={() => setIsAddEducationModalOpen(false)} title="Add Education">
        <AddEducationForm onClose={() => setIsAddEducationModalOpen(false)} onSave={handleAddEducation} />
      </Modal>

      <Modal isOpen={isAddLicenseModalOpen} onClose={() => setIsAddLicenseModalOpen(false)} title="Add License or Certification">
        <AddLicenseForm onClose={() => setIsAddLicenseModalOpen(false)} onSave={handleAddLicense} />
      </Modal>
    </div>
  );
};

export default JobBoardProfile;