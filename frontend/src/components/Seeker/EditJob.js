import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-hot-toast";

const EditJob = () => {
  const { jobId } = useParams();
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    specialization: "",
    job_type: "normal",
    industry: "",
    salary_range: "",
    salary_type: "",
    work_location: "",
    min_experience_years: 0,
    experience_level: "",
    tech_stack: [],
    city: "",
    state: "",
    country: "",
    jobpost_url: "",
    work_rights: [],
    job_arrangement: "",
    contract_duration: "",
    hourly_range: "",
    daily_range: "",
    overview: "",
    responsibilities: "",
    requirements: "",
  });

  const navigate = useNavigate();

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const response = await fetch(`/api/job/${jobId}`, {
          method: "GET",
          credentials: "include",
        });
        if (response.ok) {
          const jobData = await response.json();
          setFormData(jobData);
          console.log(formData);
        } else {
          toast.error("Failed to fetch job details.");
        }
      } catch (error) {
        console.error("Error fetching job data:", error);
        toast.error("An error occurred. Please try again.");
      }
    };
    fetchJob();
  }, [jobId]);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    if (type === "select-multiple") {
      const values = Array.from(e.target.selectedOptions, (option) => option.value);
      setFormData({ ...formData, [name]: values });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleTechStackChange = (e) => {
    const techStack = e.target.value.split(',').map(tech => tech.trim());
    setFormData({ ...formData, tech_stack: techStack });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`/api/update_job/${jobId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        toast.success("Job successfully updated!");
        navigate("/");
      } else {
        toast.error("Failed to update job.");
      }
    } catch (error) {
      console.error("Error submitting the form:", error);
      toast.error("An error occurred. Please try again.");
    }
  };

  return (
    <div className="flex justify-center items-center p-20 bg-gray-100" style={{fontFamily: "Avenir, san-serif"}}>
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md border border-green-400">
        <h1 className="text-2xl font-bold mb-4">Edit Job</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="title" className="block text-gray-700">Title:</label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="description" className="block text-gray-700">Description:</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            ></textarea>
          </div>

          <div className="mb-4">
            <label htmlFor="specialization" className="block text-gray-700">Specialization:</label>
            <select
              name="specialization"
              value={formData.specialization}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            >
              <option value="">Select Specialization</option>
              <option value="Frontend">Frontend</option>
              <option value="Backend">Backend</option>
              <option value="Full-Stack">Full-Stack</option>
              <option value="Mobile">Mobile</option>
              <option value="Data & ML">Data & ML</option>
              <option value="QA & Testing">QA & Testing</option>
              <option value="Cloud & Infra">Cloud & Infra</option>
              <option value="DevOps">DevOps</option>
              <option value="Project Management">Project Management</option>
              <option value="IT Consulting">IT Consulting</option>
              <option value="Cybersecurity">Cybersecurity</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="job_type" className="block text-gray-700">Job Type:</label>
            <select
              name="job_type"
              value={formData.job_type}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            >
              <option value="normal">Normal</option>
              <option value="premium">Premium</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="industry" className="block text-gray-700">Industry:</label>
            <select
              name="industry"
              value={formData.industry}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            >
              <option value="">Select Industry</option>
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
            <label htmlFor="salary_range" className="block text-gray-700">Salary Range:</label>
            <select
              name="salary_range"
              value={formData.salary_range}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
            >
              <option value="">Select Salary Range</option>
              <option value="Not Listed">Not Listed</option>
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
            <label htmlFor="salary_type" className="block text-gray-700">Salary Type:</label>
            <input
              type="text"
              name="salary_type"
              value={formData.salary_type}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              maxLength="10"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="work_location" className="block text-gray-700">Work Location:</label>
            <select
              name="work_location"
              value={formData.work_location}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            >
              <option value="">Select Work Location</option>
              <option value="Remote">Remote</option>
              <option value="Hybrid">Hybrid</option>
              <option value="Office">Office</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="min_experience_years" className="block text-gray-700">Minimum Experience Years:</label>
            <input
              type="number"
              name="min_experience_years"
              value={formData.min_experience_years}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              min="0"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="experience_level" className="block text-gray-700">Experience Level:</label>
            <select
              name="experience_level"
              value={formData.experience_level}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            >
              <option value="">Select Experience Level</option>
              <option value="Junior">Junior</option>
              <option value="Mid-Level">Mid-Level</option>
              <option value="Senior">Senior</option>
              <option value="Executive">Executive</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="tech_stack" className="block text-gray-700">Tech Stack (comma-separated):</label>
            <input
              type="text"
              name="tech_stack"
              // value={formData.tech_stack.join(', ')}
              onChange={handleTechStackChange}
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="city" className="block text-gray-700">City:</label>
            <input
              type="text"
              name="city"
              value={formData.city}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              maxLength="255"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="state" className="block text-gray-700">State:</label>
            <select
              name="state"
              value={formData.state}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
            >
              <option value="">Select State</option>
              <option value="VIC">VIC</option>
              <option value="NSW">NSW</option>
              <option value="ACT">ACT</option>
              <option value="WA">WA</option>
              <option value="QLD">QLD</option>
              <option value="NT">NT</option>
              <option value="TAS">TAS</option>
              <option value="SA">SA</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="country" className="block text-gray-700">Country:</label>
            <select
              name="country"
              value={formData.country}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
            >
              <option value="">Select Country</option>
              <option value="Australia">Australia</option>
              <option value="New Zealand">New Zealand</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="jobpost_url" className="block text-gray-700">Job Post URL:</label>
            <input
              type="url"
              name="jobpost_url"
              value={formData.jobpost_url}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              maxLength="255"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="work_rights" className="block text-gray-700">Work Rights:</label>
            <select
              name="work_rights"
              value={formData.work_rights}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              multiple
            >
              <option value="Australian Citizen">Australian Citizen</option>
              <option value="Australian Permanent Resident">Australian Permanent Resident</option>
              <option value="New Zealand Citizen">New Zealand Citizen</option>
              <option value="New Zealand Permanent Resident">New Zealand Permanent Resident</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="job_arrangement" className="block text-gray-700">Job Arrangement:</label>
            <select
              name="job_arrangement"
              value={formData.job_arrangement}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
            >
              <option value="">Select Job Arrangement</option>
              <option value="Permanent">Permanent</option>
              <option value="Contract/Temp">Contract/Temp</option>
              <option value="Internship">Internship</option>
              <option value="Part-Time">Part-Time</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="contract_duration" className="block text-gray-700">Contract Duration:</label>
            <select
              name="contract_duration"
              value={formData.contract_duration}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
            >
              <option value="">Select Contract Duration</option>
              <option value="3-6 Months">3-6 Months</option>
              <option value="6-9 Months">6-9 Months</option>
              <option value="9-12 Months">9-12 Months</option>
              <option value="12 Months+">12 Months+</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="hourly_range" className="block text-gray-700">Hourly Range:</label>
            <input
              type="text"
              name="hourly_range"
              value={formData.hourly_range}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              maxLength="255"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="daily_range" className="block text-gray-700">Daily Range:</label>
            <input
              type="text"
              name="daily_range"
              value={formData.daily_range}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              maxLength="255"
            />
          </div>

          <div className="mb-4">
            <label htmlFor="overview" className="block text-gray-700">Overview:</label>
            <textarea
              name="overview"
              value={formData.overview}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              rows="4"
            ></textarea>
          </div>

          <div className="mb-4">
            <label htmlFor="responsibilities" className="block text-gray-700">Responsibilities:</label>
            <textarea
              name="responsibilities"
              value={formData.responsibilities}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              rows="4"
            ></textarea>
          </div>

          <div className="mb-4">
            <label htmlFor="requirements" className="block text-gray-700">Requirements:</label>
            <textarea
              name="requirements"
              value={formData.requirements}
              onChange={handleChange}
              className="w-full p-2 border border-gray-300 rounded"
              rows="4"
            ></textarea>
          </div>

          <button
            type="submit"
            className="w-full bg-lime-500 text-white py-2 border border-lime-600 rounded hover:bg-green-700"
          >
            Update Job
          </button>
        </form>
      </div>
    </div>
  );
};

export default EditJob;




// import React, { useState, useEffect } from "react";
// import { useNavigate, useParams } from "react-router-dom";
// import { toast } from "react-hot-toast";

// const EditJob = () => {
//   const { jobId } = useParams();
//   const [formData, setFormData] = useState({
//     title: "",
//     description: "",
//     specialization: "",
//     job_type: "normal",
//     industry: "Government",
//     salary_range: "20000 - 40000",
//     salary_type: "Annual",
//     work_location: "Office",
//     min_experience_years: 0,
//     experience_level: "Entry Level",
//     city: "",
//     state: "",
//     country: "",
//     jobpost_url: "",
//     work_rights: [],
//     tech_stack: [], //new
//   });

//   const navigate = useNavigate();

//   useEffect(() => {
//     const fetchJob = async () => {
//       try {
//         const response = await fetch(`/api/job/${jobId}`, {
//           method: "GET",
//           credentials: "include",
//         });
//         if (response.ok) {
//           const jobData = await response.json();
//           setFormData(jobData);
//         } else {
//           toast.error("Failed to fetch job details.");
//         }
//       } catch (error) {
//         console.error("Error fetching job data:", error);
//         toast.error("An error occurred. Please try again.");
//       }
//     };
//     fetchJob();
//   }, [jobId]);

//   const handleChange = (e) => {
//     const { name, value, type, selectedOptions } = e.target;
//     if (type === "select-multiple") {
//       const values = Array.from(selectedOptions, (option) => option.value);
//       setFormData({ ...formData, [name]: values });
//     } else {
//       setFormData({ ...formData, [name]: value });
//     }
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       // const response = await fetch(`${apiUrl}/update_job/${jobId}`, {
//       const response = await fetch(`/api/update_job/${jobId}`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         credentials: "include",
//         body: JSON.stringify(formData),
//       });
//       if (response.ok) {
//         toast.success("Job successfully updated!");
//         navigate("/");
//       } else {
//         toast.error("Failed to update job.");
//       }
//     } catch (error) {
//       console.error("Error submitting the form:", error);
//       toast.error("An error occurred. Please try again.");
//     }
//   };

//   const handleTechChange = (index, value) => {
//     const newTechStack = [...formData.tech_stack];
//     newTechStack[index] = value;
//     setFormData({ ...formData, tech_stack: newTechStack });
//   };

//   const addTech = () => {
//     setFormData({ ...formData, tech_stack: [...formData.tech_stack, ""] });
//   };

//   const removeTech = (index) => {
//     const newTechStack = formData.tech_stack.filter((_, i) => i !== index);
//     setFormData({ ...formData, tech_stack: newTechStack });
//   };

//   return (
//     <div className="flex justify-center items-center p-20 bg-gray-100" style={{fontFamily: "Avenir, san-serif"}}>
//       <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md border border-green-400">
//         <h1 className="text-2xl font-bold mb-4">Edit Job</h1>
//         <form onSubmit={handleSubmit}>
//           <div className="mb-4">
//             <label htmlFor="title" className="block text-gray-700">
//               Title:
//             </label>
//             <input
//               type="text"
//               name="title"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.title}
//               onChange={handleChange}
//             />
//           </div>
//           <div className="mb-4">
//             <label htmlFor="description" className="block text-gray-700">
//               Description:
//             </label>
//             <textarea
//               name="description"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.description}
//               onChange={handleChange}
//             ></textarea>
//           </div>
//           <div className="mb-4">
//             <label htmlFor="specialization" className="block text-gray-700">
//               Specialization:
//             </label>
//             <input
//               type="text"
//               name="specialization"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.specialization}
//               onChange={handleChange}
//             />
//           </div>
//           <div className="mb-4">
//             <label htmlFor="job_type" className="block text-gray-700">
//               Job Type:
//             </label>
//             <select
//               name="job_type"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.job_type}
//               onChange={handleChange}
//             >
//               <option value="normal">Normal</option>
//               <option value="premium">Premium</option>
//             </select>
//           </div>
//           <div className="mb-4">
//             <label htmlFor="industry" className="block text-gray-700">
//               Industry:
//             </label>
//             <select
//               name="industry"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.industry}
//               onChange={handleChange}
//             >
//               <option value="Government">Government</option>
//               <option value="Banking & Financial Services">
//                 Banking & Financial Services
//               </option>
//               <option value="Fashion">Fashion</option>
//               <option value="Mining">Mining</option>
//               <option value="Healthcare">Healthcare</option>
//               <option value="IT - Software Development">
//                 IT - Software Development
//               </option>
//               <option value="IT - Data Analytics">IT - Data Analytics</option>
//               <option value="IT - Cybersecurity">IT - Cybersecurity</option>
//               <option value="IT - Cloud Computing">IT - Cloud Computing</option>
//               <option value="IT - Artificial Intelligence">
//                 IT - Artificial Intelligence
//               </option>
//               <option value="Agriculture">Agriculture</option>
//               <option value="Automotive">Automotive</option>
//               <option value="Construction">Construction</option>
//               <option value="Education">Education</option>
//               <option value="Energy & Utilities">Energy & Utilities</option>
//               <option value="Entertainment">Entertainment</option>
//               <option value="Hospitality & Tourism">
//                 Hospitality & Tourism
//               </option>
//               <option value="Legal">Legal</option>
//               <option value="Manufacturing">Manufacturing</option>
//               <option value="Marketing & Advertising">
//                 Marketing & Advertising
//               </option>
//               <option value="Media & Communications">
//                 Media & Communications
//               </option>
//               <option value="Non-Profit & NGO">Non-Profit & NGO</option>
//               <option value="Pharmaceuticals">Pharmaceuticals</option>
//               <option value="Real Estate">Real Estate</option>
//               <option value="Retail & Consumer Goods">
//                 Retail & Consumer Goods
//               </option>
//               <option value="Telecommunications">Telecommunications</option>
//               <option value="Transportation & Logistics">
//                 Transportation & Logistics
//               </option>
//             </select>
//           </div>
//           <div className="mb-4">
//             <label htmlFor="salary_range" className="block text-gray-700">
//               Salary Range:
//             </label>
//             <select
//               name="salary_range"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.salary_range}
//               onChange={handleChange}
//             >
//               <option value="20000 - 40000">20000 - 40000</option>
//               <option value="40000 - 60000">40000 - 60000</option>
//               <option value="60000 - 80000">60000 - 80000</option>
//               <option value="80000 - 100000">80000 - 100000</option>
//               <option value="100000 - 120000">100000 - 120000</option>
//               <option value="120000 - 140000">120000 - 140000</option>
//               <option value="140000 - 160000">140000 - 160000</option>
//               <option value="160000 - 180000">160000 - 180000</option>
//               <option value="180000 - 200000">180000 - 200000</option>
//               <option value="200000 - 220000">200000 - 220000</option>
//               <option value="220000 - 240000">220000 - 240000</option>
//               <option value="240000 - 260000">240000 - 260000</option>
//               <option value="260000+">260000+</option>
//             </select>
//           </div>
//           <div className="mb-4">
//             <label htmlFor="salary_type" className="block text-gray-700">
//               Salary Type:
//             </label>
//             <select
//               name="salary_type"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.salary_type}
//               onChange={handleChange}
//             >
//               <option value="Annual">Annual</option>
//               <option value="Hourly">Hourly</option>
//             </select>
//           </div>
//           <div className="mb-4">
//             <label htmlFor="work_location" className="block text-gray-700">
//               Work Location:
//             </label>
//             <select
//               name="work_location"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.work_location}
//               onChange={handleChange}
//             >
//               <option value="Office">Office</option>
//               <option value="Remote">Remote</option>
//               <option value="Hybrid">Hybrid</option>
//             </select>
//           </div>
//           <div className="mb-4">
//             <label
//               htmlFor="min_experience_years"
//               className="block text-gray-700"
//             >
//               Minimum Experience Years:
//             </label>
//             <input
//               type="number"
//               name="min_experience_years"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.min_experience_years}
//               onChange={handleChange}
//             />
//           </div>
//           <div className="mb-4">
//             <label className="block text-gray-700">Technologies:</label>
//             {formData.tech_stack.map((tech, index) => (
//               <div key={index} className="flex mb-2">
//                 <input
//                   type="text"
//                   value={tech}
//                   onChange={(e) => handleTechChange(index, e.target.value)}
//                   className="w-full p-2 border border-gray-300 rounded-l"
//                 />
//                 <button
//                   type="button"
//                   onClick={() => removeTech(index)}
//                   className="bg-red-500 text-white p-2 rounded-r"
//                 >
//                   Remove
//                 </button>
//               </div>
//             ))}
//             <button
//               type="button"
//               onClick={addTech}
//               className="mt-2 bg-blue-500 text-white p-2 rounded"
//             >
//               Add Technology
//             </button>
//           </div>
//           <div className="mb-4">
//             <label htmlFor="experience_level" className="block text-gray-700">
//               Experience Level:
//             </label>
//             <select
//               name="experience_level"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.experience_level}
//               onChange={handleChange}
//             >
//               <option value="Entry Level">Entry Level</option>
//               <option value="Associate">Associate</option>
//               <option value="Mid-Senior Level">Mid-Senior Level</option>
//               <option value="Director">Director</option>
//               <option value="Executive">Executive</option>
//             </select>
//           </div>
//           <div className="mb-4">
//             <label htmlFor="city" className="block text-gray-700">
//               City:
//             </label>
//             <input
//               type="text"
//               name="city"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.city}
//               onChange={handleChange}
//             />
//           </div>
//           <div className="mb-4">
//             <label htmlFor="state" className="block text-gray-700">
//               State:
//             </label>
//             <input
//               type="text"
//               name="state"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.state}
//               onChange={handleChange}
//             />
//           </div>
//           <div className="mb-4">
//             <label htmlFor="country" className="block text-gray-700">
//               Country:
//             </label>
//             <input
//               type="text"
//               name="country"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.country}
//               onChange={handleChange}
//             />
//           </div>
//           <div className="mb-4">
//             <label htmlFor="jobpost_url" className="block text-gray-700">
//               Job Post URL:
//             </label>
//             <input
//               type="url"
//               name="jobpost_url"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               value={formData.jobpost_url}
//               onChange={handleChange}
//             />
//           </div>
//           <div className="mb-4">
//             <label htmlFor="work_rights" className="block text-gray-700">
//               Work Rights:
//             </label>
//             <select
//               name="work_rights"
//               className="w-full p-2 border border-gray-300 rounded"
//               required
//               multiple
//               value={formData.work_rights}
//               onChange={handleChange}
//             >
//               <option value="Australian Citizen">Australian Citizen</option>
//               <option value="Australian Permanent Resident">
//                 Australian Permanent Resident
//               </option>
//               <option value="New Zealand Citizen">New Zealand Citizen</option>
//               <option value="New Zealand Permanent Resident">
//                 New Zealand Permanent Resident
//               </option>
//             </select>
//           </div>
//           <button
//             type="submit"
//             className="w-full bg-lime-500 text-white py-2 border border-lime-600 rounded hover:bg-green-700"
//           >
//             Update Job
//           </button>
//         </form>
//       </div>
//     </div>
//   );
// };

// export default EditJob;
