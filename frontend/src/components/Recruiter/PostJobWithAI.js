import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";
import HashLoader from "react-spinners/HashLoader";

const PostJobWithAI = () => {

  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    specialization: "",
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
    setLoading(true);
    try {
      const response = await fetch("/api/add_job_ai", {
        // Updated URL
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        setLoading(false);
        const data = await response.json();
        toast.success(data.message || "Job successfully added!");
        navigate("/");
      } else {
        const errorData = await response.json();
        toast.error(errorData.error || "Failed to add job.");
      }
    } catch (error) {
      setLoading(false);
      console.error("Error submitting the form:", error);
      toast.error("An error occurred. Please try again.");
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <HashLoader color="#8823cf" size={120} />
      </div>
    );
}

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

export default PostJobWithAI;
