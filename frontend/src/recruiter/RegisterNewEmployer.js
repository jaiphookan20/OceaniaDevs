import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const RegisterNewEmployer = ({onComplete}) => {
  const [formData, setFormData] = useState({
    employerName: "",
    employerWebsite: "",
    country: "",
    employerSize: "",
    employerAddress: "",
    employerDescription: "",
    logo: null,
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, logo: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
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
      const result = await response.json();
      console.log(result.message);
      if (
        result.message === "Company created and recruiter updated successfully"
      ) {
        onComplete();
        // navigate("/employer/post-job");
      }
    } catch (error) {
      console.error("Error creating company:", error);
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
            <label htmlFor="country" className="block text-gray-700">
              Country
            </label>
            <select
              id="country"
              className="w-full p-2 border border-gray-300 rounded"
              value={formData.country}
              onChange={handleChange}
            >
              <option>Select your country</option>
              <option>Australia</option>
              <option>New Zealand</option>
              {/* Add more options as needed */}
            </select>
          </div>
          <div className="mb-4">
            <label htmlFor="employerSize" className="block text-gray-700">
              Employer size
            </label>
            <input
              type="text"
              id="employerSize"
              className="w-full p-2 border border-gray-300 rounded"
              value={formData.employerSize}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="employerAddress" className="block text-gray-700">
              Employer address
            </label>
            <input
              type="text"
              id="employerAddress"
              className="w-full p-2 border border-gray-300 rounded"
              value={formData.employerAddress}
              onChange={handleChange}
            />
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
              minLength="150"
              value={formData.employerDescription}
              onChange={handleChange}
            ></textarea>
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
          >
            Complete Registration
          </button>
        </form>
      </div>
    </div>
  );
};

export default RegisterNewEmployer;
