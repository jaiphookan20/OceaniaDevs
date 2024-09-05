// import React, { useEffect, useState } from 'react';

// function TechnologyDashboard() {
//   const [jobTechnologiesSummary, setJobTechnologiesSummary] = useState([]);
//   const [technologies, setTechnologies] = useState([]);
//   const [technologyAliases, setTechnologyAliases] = useState([]);
//   const [newTechnology, setNewTechnology] = useState('');
//   const [newAlias, setNewAlias] = useState('');
//   const [selectedTechnologyId, setSelectedTechnologyId] = useState(null);
//   const [selectedJobId, setSelectedJobId] = useState(null);
//   const [error, setError] = useState('');
//   const [success, setSuccess] = useState('');

//   useEffect(() => {
//     fetchJobTechnologiesSummary();
//     fetchTechnologies();
//     fetchTechnologyAliases();
//   }, []);

//   const fetchJobTechnologiesSummary = async () => {
//     try {
//       const response = await fetch('/api/job_technologies_summary');
//       if (!response.ok) throw new Error(await response.text());
//       const data = await response.json();
//       setJobTechnologiesSummary(data);
//     } catch (error) {
//       setError('Failed to fetch job technologies summary.');
//       console.error(error);
//     }
//   };

//   const fetchTechnologies = async () => {
//     try {
//       const response = await fetch('/api/technologies');
//       if (!response.ok) throw new Error(await response.text());
//       const data = await response.json();
//       setTechnologies(data);
//     } catch (error) {
//       setError('Failed to fetch technologies.');
//       console.error(error);
//     }
//   };

//   const fetchTechnologyAliases = async () => {
//     try {
//       const response = await fetch('/api/technology_aliases');
//       if (!response.ok) throw new Error(await response.text());
//       const data = await response.json();
//       setTechnologyAliases(data);
//     } catch (error) {
//       setError('Failed to fetch technology aliases.');
//       console.error(error);
//     }
//   };

//   const handleAddTechnology = async () => {
//     if (!newTechnology) return;
//     try {
//       const response = await fetch('/api/technologies', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ name: newTechnology }),
//       });

//       if (!response.ok) throw new Error(await response.text());

//       setNewTechnology('');
//       fetchTechnologies();
//       setError('');
//       setSuccess('Technology added successfully.');
//     } catch (error) {
//       setError('Failed to add technology.');
//       console.error(error);
//     }
//   };

//   const handleAddAlias = async () => {
//     if (!newAlias || !selectedTechnologyId) return;
//     try {
//       const response = await fetch('/api/technology_aliases', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ alias: newAlias, technology_id: selectedTechnologyId }),
//       });

//       if (!response.ok) throw new Error(await response.text());

//       setNewAlias('');
//       setSelectedTechnologyId(null);
//       fetchTechnologyAliases();
//       setError('');
//       setSuccess('Alias added successfully.');
//     } catch (error) {
//       setError('Failed to add alias.');
//       console.error(error);
//     }
//   };

//   const handleAddJobTechnology = async () => {
//     if (!selectedJobId || !selectedTechnologyId) return;
//     try {
//       const response = await fetch('/api/job_technologies', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ job_id: selectedJobId, technology_id: selectedTechnologyId }),
//       });

//       if (!response.ok) throw new Error(await response.text());

//       fetchJobTechnologiesSummary();
//       setError('');
//       setSuccess('Technology added to job successfully.');
//     } catch (error) {
//       setError('Failed to add technology to job.');
//       console.error(error);
//     }
//   };

//   const handleRemoveJobTechnology = async (jobId, technologyId) => {
//     try {
//       const response = await fetch('/api/job_technologies', {
//         method: 'DELETE',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ job_id: jobId, technology_id: technologyId }),
//       });

//       if (!response.ok) throw new Error(await response.text());

//       fetchJobTechnologiesSummary();
//       setError('');
//       setSuccess('Technology removed from job successfully.');
//     } catch (error) {
//       setError('Failed to remove technology from job.');
//       console.error(error);
//     }
//   };

//   return (
//     <div className="p-6 max-w-4xl mx-auto">
//       {error && <div className="text-red-500 mb-4">{error}</div>}
//       {success && <div className="text-green-500 mb-4">{success}</div>}
//       <h1 className="text-3xl font-bold mb-4 text-center">Technology Dashboard</h1>

//       <section className="mb-6">
//         <h2 className="text-2xl font-bold mb-2">Job Technologies Summary</h2>
//         <table className="min-w-full bg-white border border-gray-200 rounded-lg shadow-md">
//           <thead className="bg-gray-100">
//             <tr>
//               <th className="py-3 px-4 border-b">Job ID</th>
//               <th className="py-3 px-4 border-b">Title</th>
//               <th className="py-3 px-4 border-b">Technologies</th>
//               <th className="py-3 px-4 border-b">Actions</th>
//             </tr>
//           </thead>
//           <tbody>
//             {jobTechnologiesSummary.map((job) => (
//               <tr key={job.job_id}>
//                 <td className="py-3 px-4 border-b text-center">{job.job_id}</td>
//                 <td className="py-3 px-4 border-b">{job.title}</td>
//                 <td className="py-3 px-4 border-b">
//                   {/* Ensure job.technologies is an array before mapping */}
//                   {Array.isArray(job.technologies) ? (
//                     job.technologies.map((tech, index) => (
//                       <span key={index} className="inline-block bg-blue-100 text-blue-800 text-sm px-2 py-1 rounded mr-2 mb-1">
//                         {tech}
//                       </span>
//                     ))
//                   ) : (
//                     <span>No technologies assigned</span>
//                   )}
//                 </td>
//                 <td className="py-3 px-4 border-b text-center">
//                   {Array.isArray(job.technologies) && job.technologies.map((tech, index) => (
//                     <button
//                       key={index}
//                       onClick={() => handleRemoveJobTechnology(job.job_id, tech.id)}
//                       className="bg-red-500 hover:bg-red-600 text-white text-xs px-2 py-1 rounded mr-1"
//                     >
//                       Remove {tech}
//                     </button>
//                   ))}
//                 </td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </section>

//       {/* ... rest of your sections ... */}

//     </div>
//   );
// }

// export default TechnologyDashboard;
