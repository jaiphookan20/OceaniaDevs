import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";

const PostJob = () => {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    specialization: "",
    job_type: "normal",
    industry: "Government",
    salary_range: "20000 - 40000",
    salary_type: "Annual",
    work_location: "Office",
    min_experience_years: 0,
    experience_level: "Entry Level",
    city: "",
    state: "",
    country: "",
    jobpost_url: "",
    work_rights: [],
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, selectedOptions } = e.target;
    if (type === "select-multiple") {
      const values = Array.from(selectedOptions, (option) => option.value);
      setFormData({ ...formData, [name]: values });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("/api/add_job", {
        // Updated URL
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        const data = await response.json();
        toast.success(data.message || "Job successfully added!");
        navigate("/");
      } else {
        const errorData = await response.json();
        toast.error(errorData.error || "Failed to add job.");
      }
    } catch (error) {
      console.error("Error submitting the form:", error);
      toast.error("An error occurred. Please try again.");
    }
  };

  return (
    <div className="flex justify-center items-center p-20 bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md border border-green-400">
        <h1 className="text-2xl font-bold mb-4">Add Job</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="title" className="block text-gray-700">
              Title:
            </label>
            <input
              type="text"
              name="title"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.title}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="description" className="block text-gray-700">
              Description:
            </label>
            <textarea
              name="description"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.description}
              onChange={handleChange}
            ></textarea>
          </div>
          <div className="mb-4">
            <label htmlFor="specialization" className="block text-gray-700">
              Specialization:
            </label>
            <input
              type="text"
              name="specialization"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.specialization}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="job_type" className="block text-gray-700">
              Job Type:
            </label>
            <select
              name="job_type"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.job_type}
              onChange={handleChange}
            >
              <option value="normal">Normal</option>
              <option value="premium">Premium</option>
            </select>
          </div>
          <div className="mb-4">
            <label htmlFor="industry" className="block text-gray-700">
              Industry:
            </label>
            <select
              name="industry"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.industry}
              onChange={handleChange}
            >
              <option value="Government">Government</option>
              <option value="Banking & Financial Services">
                Banking & Financial Services
              </option>
              <option value="Fashion">Fashion</option>
              <option value="Mining">Mining</option>
              <option value="Healthcare">Healthcare</option>
              <option value="IT - Software Development">
                IT - Software Development
              </option>
              <option value="IT - Data Analytics">IT - Data Analytics</option>
              <option value="IT - Cybersecurity">IT - Cybersecurity</option>
              <option value="IT - Cloud Computing">IT - Cloud Computing</option>
              <option value="IT - Artificial Intelligence">
                IT - Artificial Intelligence
              </option>
              <option value="Agriculture">Agriculture</option>
              <option value="Automotive">Automotive</option>
              <option value="Construction">Construction</option>
              <option value="Education">Education</option>
              <option value="Energy & Utilities">Energy & Utilities</option>
              <option value="Entertainment">Entertainment</option>
              <option value="Hospitality & Tourism">
                Hospitality & Tourism
              </option>
              <option value="Legal">Legal</option>
              <option value="Manufacturing">Manufacturing</option>
              <option value="Marketing & Advertising">
                Marketing & Advertising
              </option>
              <option value="Media & Communications">
                Media & Communications
              </option>
              <option value="Non-Profit & NGO">Non-Profit & NGO</option>
              <option value="Pharmaceuticals">Pharmaceuticals</option>
              <option value="Real Estate">Real Estate</option>
              <option value="Retail & Consumer Goods">
                Retail & Consumer Goods
              </option>
              <option value="Telecommunications">Telecommunications</option>
              <option value="Transportation & Logistics">
                Transportation & Logistics
              </option>
            </select>
          </div>
          <div className="mb-4">
            <label htmlFor="salary_range" className="block text-gray-700">
              Salary Range:
            </label>
            <select
              name="salary_range"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.salary_range}
              onChange={handleChange}
            >
              <option value="20000 - 40000">20000 - 40000</option>
              <option value="40000 - 60000">40000 - 60000</option>
              <option value="60000 - 80000">60000 - 80000</option>
              <option value="80000 - 100000">80000 - 100000</option>
              <option value="100000 - 120000">100000 - 120000</option>
              <option value="120000 - 140000">120000 - 140000</option>
              <option value="140000 - 160000">140000 - 160000</option>
              <option value="160000 - 180000">160000 - 180000</option>
              <option value="180000 - 200000">180000 - 200000</option>
              <option value="200000 - 220000">200000 - 220000</option>
              <option value="220000 - 240000">220000 - 240000</option>
              <option value="240000 - 260000">240000 - 260000</option>
              <option value="260000+">260000+</option>
            </select>
          </div>
          <div className="mb-4">
            <label htmlFor="salary_type" className="block text-gray-700">
              Salary Type:
            </label>
            <select
              name="salary_type"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.salary_type}
              onChange={handleChange}
            >
              <option value="Annual">Annual</option>
              <option value="Hourly">Hourly</option>
            </select>
          </div>
          <div className="mb-4">
            <label htmlFor="work_location" className="block text-gray-700">
              Work Location:
            </label>
            <select
              name="work_location"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.work_location}
              onChange={handleChange}
            >
              <option value="Office">Office</option>
              <option value="Remote">Remote</option>
              <option value="Hybrid">Hybrid</option>
            </select>
          </div>
          <div className="mb-4">
            <label
              htmlFor="min_experience_years"
              className="block text-gray-700"
            >
              Minimum Experience Years:
            </label>
            <input
              type="number"
              name="min_experience_years"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.min_experience_years}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="experience_level" className="block text-gray-700">
              Experience Level:
            </label>
            <select
              name="experience_level"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.experience_level}
              onChange={handleChange}
            >
              <option value="Entry Level">Entry Level</option>
              <option value="Associate">Associate</option>
              <option value="Mid-Senior Level">Mid-Senior Level</option>
              <option value="Director">Director</option>
              <option value="Executive">Executive</option>
            </select>
          </div>
          <div className="mb-4">
            <label htmlFor="city" className="block text-gray-700">
              City:
            </label>
            <input
              type="text"
              name="city"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.city}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="state" className="block text-gray-700">
              State:
            </label>
            <input
              type="text"
              name="state"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.state}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="country" className="block text-gray-700">
              Country:
            </label>
            <input
              type="text"
              name="country"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.country}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="jobpost_url" className="block text-gray-700">
              Job Post URL:
            </label>
            <input
              type="url"
              name="jobpost_url"
              className="w-full p-2 border border-gray-300 rounded"
              required
              value={formData.jobpost_url}
              onChange={handleChange}
            />
          </div>
          <div className="mb-4">
            <label htmlFor="work_rights" className="block text-gray-700">
              Work Rights:
            </label>
            <select
              name="work_rights"
              className="w-full p-2 border border-gray-300 rounded"
              required
              multiple
              value={formData.work_rights}
              onChange={handleChange}
            >
              <option value="Australian Citizen">Australian Citizen</option>
              <option value="Australian Permanent Resident">
                Australian Permanent Resident
              </option>
              <option value="New Zealand Citizen">New Zealand Citizen</option>
              <option value="New Zealand Permanent Resident">
                New Zealand Permanent Resident
              </option>
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-lime-500 text-white py-2 border border-lime-600 rounded hover:bg-green-700"
          >
            Add Job
          </button>
        </form>
      </div>
    </div>
  );
};

export default PostJob;
