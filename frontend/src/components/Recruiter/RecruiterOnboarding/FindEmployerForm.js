import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";

const FindEmployerForm = ({ onComplete }) => {
  const [selectedEmployer, setSelectedEmployer] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [companies, setCompanies] = useState([]);
  const [step, setStep] = useState("search");
  const [workEmail, setWorkEmail] = useState("");
  const [verificationCode, setVerificationCode] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const response = await fetch("/api/companies", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        const result = await response.json();
        console.log("Fetched companies:", result);
        setCompanies(result);
      } catch (error) {
        console.error("Error fetching companies:", error);
      }
    };
  
    fetchCompanies();
  }, []);

  const handleSelect = (company) => {
    setSelectedEmployer(company);
    setDropdownOpen(false);
    setStep("email");
    console.log("Selected company domain:", company.domain);
  };

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("/api/verify_recruiter_email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ company_id: selectedEmployer.company_id, email: `${workEmail}@${selectedEmployer.domain}` }),
        credentials: "include",
      });
      const data = await response.json();
      if (response.ok) {
        setStep("verify");
        toast.success("Verification code sent to your email");
      } else {
        toast.error(data.error || "Failed to send verification code");
      }
    } catch (error) {
      console.error("Error sending verification email:", error);
      toast.error("An error occurred. Please try again.");
    }
  };

  const handleVerificationSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("/api/verify_code", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          code: verificationCode,
          company_id: selectedEmployer.company_id
        }),
        credentials: "include",
      });
      const data = await response.json();
      if (response.ok) {
        toast.success("Email verified successfully");
        onComplete();
      } else {
        toast.error(data.error || "Invalid verification code");
      }
    } catch (error) {
      console.error("Error verifying code:", error);
      toast.error("An error occurred. Please try again.");
    }
  };

  const filteredCompanies = companies.filter((company) =>
    company.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const renderStep = () => {
    switch (step) {
      case "search":
        return (
          <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
            <h2 className="mb-6 text-3xl font-bold text-center">
              Find your employer
            </h2>
            <div className="mb-6">
              <label
                className="block text-sm font-medium text-gray-700"
                htmlFor="employer"
              >
                Select employer
              </label>
              <div className="relative mt-1">
                <button
                  type="button"
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="w-full pl-3 pr-10 py-2 mt-1 bg-violet-500 text-white border border-gray-300 rounded-md shadow-sm focus:outline-none hover:bg-violet-700 hover:text-white focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                >
                  {selectedEmployer ? selectedEmployer.name : "Select your employer"}
                </button>
                {dropdownOpen && (
                  <div className="absolute mt-1 w-full bg-white border rounded-lg shadow-lg z-10">
                    <div className="p-2">
                      <input
                        type="text"
                        placeholder="Search company"
                        className="w-full border rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                      />
                    </div>
                    <div className="max-h-60 overflow-y-auto">
                      {filteredCompanies.map((company, index) => (
                        <div
                          key={index}
                          className="flex items-center p-2 hover:bg-violet-500 hover:text-white hover:font-semibold cursor-pointer"
                          onClick={() => handleSelect(company)}
                        >
                          <img src={company.logo_url} className="h-6 w-6 mr-4 rounded-full" alt={company.name} />
                          {company.name}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
            <div className="mt-4 text-center">
              <button
                type="button"
                className="text-emerald-700 hover:underline focus:outline-none"
                onClick={() => onComplete()}
              >
                Didn't find your employer? Create new employer
              </button>
            </div>
          </div>
        );
      case "email":
        return (
          <form onSubmit={handleEmailSubmit} className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
            <img src={selectedEmployer.logo_url} className="h-12 w-12 mx-auto mb-4" alt={selectedEmployer.name} />
            <h2 className="mb-6 text-3xl font-bold text-slate-500 text-center">Let's verify you work at</h2>
            <h2 className="mb-6 text-3xl font-bold text-center">{selectedEmployer.name}</h2>
            <p className="mb-4">One last step! We'll use your work email to confirm you're an employee at {selectedEmployer.name}. Please enter it below.</p>
            <div className="mb-4 flex">
              <input
                type="text"
                value={workEmail}
                onChange={(e) => setWorkEmail(e.target.value)}
                placeholder="example"
                className="w-1/2 p-2 border rounded-l"
              />
              <span className="p-2 bg-gray-100 border rounded-r">@{selectedEmployer.domain}</span>
            </div>
            <button type="submit" className="w-full bg-purple-600 text-white p-2 rounded mt-4">Continue</button>
            <button type="button" onClick={() => setStep("search")} className="w-full bg-gray-300 text-gray-700 p-2 rounded mt-2">Go Back</button>
          </form>
        );
      case "verify":
        return (
          <form onSubmit={handleVerificationSubmit} className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
            <h2 className="mb-6 text-3xl font-bold text-center">Check your work email</h2>
            <p className="mb-4">We sent a 6-digit code to {workEmail}@{selectedEmployer.domain}.</p>
            <div className="flex justify-center mb-4">
              {[...Array(6)].map((_, index) => (
                <input
                  key={index}
                  type="text"
                  maxLength={1}
                  value={verificationCode[index] || ''}
                  onChange={(e) => {
                    const newCode = verificationCode.split('');
                    newCode[index] = e.target.value;
                    setVerificationCode(newCode.join(''));
                    if (e.target.value && index < 5) {
                      e.target.nextElementSibling.focus();
                    }
                  }}
                  className="w-12 h-12 text-center text-2xl border rounded mx-1"
                />
              ))}
            </div>
            <p className="text-sm text-center mb-4">
              Didn't receive OTP? <button type="button" onClick={handleEmailSubmit} className="text-purple-600 hover:underline">Change email</button> or <button type="button" onClick={handleEmailSubmit} className="text-purple-600 hover:underline">get a new code</button>.
            </p>
            <div className="bg-gray-100 border rounded p-4 mb-4">
              <p className="text-sm"><strong>Your privacy is important</strong></p>
              <p className="text-sm">We may send you job reports, reminders and messages from us and our partners. You can tailor the emails you receive in settings.</p>
            </div>
            <p className="text-sm text-center mb-4">Access your inbox with:</p>
            <div className="flex justify-center space-x-4 mb-4">
              <a href="https://mail.google.com" target="_blank" rel="noopener noreferrer">
                <button type="button" className="bg-white border rounded px-4 py-2 flex items-center">
                  <img src='https://www.logo.wine/a/logo/Gmail/Gmail-Logo.wine.svg' alt="Gmail" className="w-6 h-6 mr-2" />
                  Gmail
                </button>
              </a>
              <a href="https://outlook.live.com" target="_blank" rel="noopener noreferrer">
                <button type="button" className="bg-white border rounded px-4 py-2 flex items-center">
                  <img src='https://www.logo.wine/a/logo/Outlook_on_the_web/Outlook_on_the_web-Logo.wine.svg' alt="Outlook" className="w-6 h-6 mr-2" />
                  Outlook
                </button>
              </a>
            </div>
            <button type="submit" className="w-full bg-purple-600 text-white p-2 rounded">Verify</button>
            <button type="button" onClick={() => setStep("email")} className="w-full bg-gray-300 text-gray-700 p-2 rounded mt-2">Go Back</button>
          </form>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100" style={{fontFamily: "Avenir, sans-serif"}}>
      {renderStep()}
    </div>
  );
};

export default FindEmployerForm;