import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const EmployerSignupStep2 = () => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    position: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("/api/register/employer/info", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(formData),
      });
      const result = await response.json();
      console.log(result.message);
      navigate("/employer/new/organization-details");
    } catch (error) {
      console.error("Error updating recruiter info:", error);
    }
  };

  return (
    <div className="flex justify-center items-center p-20 bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md border border-green-400">
        <h1 className="text-2xl font-bold mb-4">Tell us more about you</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="firstName" className="block text-gray-700">
              First name
            </label>
            <input
              type="text"
              id="firstName"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.firstName}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="lastName" className="block text-gray-700">
              Last name
            </label>
            <input
              type="text"
              id="lastName"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.lastName}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="position" className="block text-gray-700">
              Position
            </label>
            <input
              type="text"
              id="position"
              className="w-full p-2 border border-gray-300 rounded"
              value={formData.position}
              onChange={handleChange}
            />
          </div>
          <button
            type="submit"
            className="w-full bg-lime-500 text-white py-2 border border-lime-600 rounded hover:bg-green-700"
          >
            Continue
          </button>
        </form>
      </div>
    </div>
  );
};

export default EmployerSignupStep2;
