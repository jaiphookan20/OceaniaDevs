import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";

const RegisterNewEmployer = ({onComplete}) => {
  const [formData, setFormData] = useState({
    employerName: "",
    employerWebsite: "",
    employerSize: "",
    employerDescription: "",
    location: "",
    logo: null,
    type: "",
    industry: "",
    city: "",
    state: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { id, value } = e.target;
    if (id === 'location') {
      const [city, state] = value.split(', ');
      setFormData(prevData => ({
        ...prevData,
        location: value,
        city,
        state
      }));
    } else if (id === 'employerDescription') {
      setFormData(prevData => ({
        ...prevData,
        [id]: value.slice(0, 200)
      }));
    } else {
      setFormData(prevData => ({
        ...prevData,
        [id]: value
      }));
    }
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, logo: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.employerDescription.length < 100) {
      toast.error("Employer description must be at least 100 characters");
      return;
    }

    const formDataToSend = new FormData();
    for (const key in formData) {
      formDataToSend.append(key, formData[key]);
    }

    try {
      const response = await fetch("/api/register/employer/create_company", {
        method: "POST",
        credentials: "include",
        body: formDataToSend,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
      }

      const result = await response.json();
      console.log(result.message);
      if (result.message === "Company created and recruiter updated successfully") {
        toast.success("Updated Successfully")
        onComplete();
      } else {
        toast.error(result.error || "Unknown error occurred");
      }
    } catch (error) {
      console.error("Error creating company:", error);
      toast.error(`Error Creating Company: ${error.message}`);
    }
  };

  return (
    <div className="flex justify-center items-center p-20 bg-gray-100"  style={{fontFamily: "Avenir, san-serif"}}>
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md border border-green-400">
        <h1 className="text-3xl font-bold mb-4">New employer details</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="employerName" className="block text-gray-700">
              Employer name
            </label>
            <input
              type="text"
              id="employerName"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.employerName}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="employerWebsite" className="block text-gray-700">
              Employer website
            </label>
            <input
              type="url"
              id="employerWebsite"
              className="w-full p-2 border border-gray-300 rounded"
              value={formData.employerWebsite}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="employerSize" className="block text-gray-700">
              Employer size
            </label>
            <select
              id="employerSize"
              className="w-full p-2 border border-gray-300 rounded"
              value={formData.employerSize}
              onChange={handleChange}
            >
              <option value="">Select company size</option>
              <option value="0-9">0-9</option>
              <option value="10-49">10-49</option>
              <option value="50-249">50-249</option>
              <option value="250-999">250-999</option>
              <option value="1000+">1000+</option>
            </select>
          </div>
          <div className="mb-4">
            <label htmlFor="type" className="block text-gray-700">
              Type
            </label>
            <select
              id="type"
              className="w-full p-2 border border-gray-300 rounded"
              value={formData.type}
              onChange={handleChange}
            >
              <option value="">Select type</option>
              <option value="Agency">Agency</option>
              <option value="Company">Company</option>
            </select>
          </div>
          <div className="mb-4">
            <label htmlFor="industry" className="block text-gray-700">
              Industry
            </label>
            <select
              id="industry"
              className="w-full p-2 border border-gray-300 rounded"
              value={formData.industry}
              onChange={handleChange}
            >
              <option value="">Select industry</option>
              <option value="">Select industry</option>
                  <option value="Government">Government</option>
                  <option value="Banking & Financial Services">Banking & Financial Services</option>
                  <option value="Fashion">Fashion</option>
                  <option value="Mining">Mining</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="IT - Software Development">IT - Software Development</option>
                  <option value="IT - Data Analytics">IT - Data Analytics</option>
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
          </div>
          <div className="mb-4">
            <label htmlFor="location" className="block text-gray-700">
              Location
            </label>
            <select
              id="location"
              className="w-full p-2 border border-gray-300 rounded"
              value={formData.location}
              onChange={handleChange}
            >
              <option value="">Select location</option>
              <option value="Sydney, NSW">Sydney, NSW</option>
                  <option value="Melbourne, VIC">Melbourne, VIC</option>
                  <option value="Brisbane, QLD">Brisbane, QLD</option>
                  <option value="Perth, WA">Perth, WA</option>
                  <option value="Adelaide, SA">Adelaide, SA</option>
                  <option value="Gold Coast, QLD">Gold Coast, QLD</option>
                  <option value="Newcastle, NSW">Newcastle, NSW</option>
                  <option value="Canberra, ACT">Canberra, ACT</option>
                  <option value="Sunshine Coast, QLD">Sunshine Coast, QLD</option>
                  <option value="Wollongong, NSW">Wollongong, NSW</option>
                  <option value="Hobart, TAS">Hobart, TAS</option>
                  <option value="Geelong, VIC">Geelong, VIC</option>
                  <option value="Townsville, QLD">Townsville, QLD</option>
                  <option value="Cairns, QLD">Cairns, QLD</option>
                  <option value="Darwin, NT">Darwin, NT</option>
            </select>
          </div>
          <div className="mb-4">
            <label
              htmlFor="employerDescription"
              className="block text-gray-700"
            >
              Employer description
            </label>
            <textarea
              id="employerDescription"
              className="w-full p-2 border border-gray-300 rounded"
              minLength="100"
              maxLength="200"
              value={formData.employerDescription}
              onChange={handleChange}
            ></textarea>
            <div className={`text-sm mt-1 ${formData.employerDescription.length > 200 || formData.employerDescription.length < 100 ? 'text-red-500' : 'text-gray-500'}`}>
              {formData.employerDescription.length}/200 characters
              {formData.employerDescription.length < 100 && " (minimum 100 characters)"}
            </div>
          </div>
          <div className="mb-4">
            <label htmlFor="logo" className="block text-gray-700">
              Add a logo
            </label>
            <input
              type="file"
              id="logo"
              className="w-full p-2 border border-gray-300 rounded"
              onChange={handleFileChange}
            />
          </div>
          <button
            type="submit"
            className="w-full bg-lime-500 text-white py-2 border border-lime-600 rounded hover:bg-green-700"
            disabled={formData.employerDescription.length < 100 || formData.employerDescription.length > 200}
          >
            Complete Registration
          </button>
        </form>
      </div>
    </div>
  );
};

export default RegisterNewEmployer;