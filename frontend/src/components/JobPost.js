import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { icons } from "../data/tech-icons";

const JobListing = ({ onSave, onApply }) => {
  const { jobId } = useParams();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const response = await fetch(`/api/job_post/${jobId}`);
        const data = await response.json();
        if (response.ok) {
          setJob(data);
        } else {
          setError(data.error);
        }
        setLoading(false);
      } catch (error) {
        console.error("Error fetching job:", error);
        setError("Failed to fetch job.");
        setLoading(false);
      }
    };

    fetchJob();
  }, [jobId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="flex flex-col max-w-6xl mx-auto min-h-screen justify-center">
      <div className="flex-grow container mx-auto bg-white shadow-md rounded-lg border-t">
        <header className="flex justify-between pb-1 mb-4">
          <div className="flex items-center">
            <img src={job.logo} alt={job.company} className="p-6 max-w-32" />
          </div>
          <div className="flex mt-4 space-x-4 pr-4">
            {job.tech_stack.map((tech) => (
              <div
                key={tech}
                className="p-2 rounded-md flex items-center space-x-2"
              >
                <img
                  src={icons[tech.toLowerCase()]}
                  alt={tech}
                  className="w-16 h-16"
                />
              </div>
            ))}
          </div>
        </header>
        <div className="ml-4">
          <h1 className="text-5xl font-bold">{job.title}</h1>
          <h3 className="text-3xl pt-2 text-slate-500 font-semibold">
            {job.company}
          </h3>
          <p className="text-gray-500 mt-2 text-xl">
            Mezmo, formerly LogDNA, is a comprehensive platform that makes
            observability data consumable and actionable.
          </p>
          <div className="flex justify-between mt-2 pt-2 p-2">
            <div className="flex items-center space-x-2">
              <img
                width="36"
                height="36"
                src="https://img.icons8.com/?size=100&id=Z3STIRU4hxMn&format=png&color=000000"
                alt="company"
              />
              <p className="text-gray-500 text-1xl">{job.industry}</p>
            </div>
            <div className="flex items-center space-x-2">
              <img
                width="36"
                height="36"
                src="https://img.icons8.com/?size=100&id=3BUZy0U5CdQL&format=png&color=000000"
                alt="experience"
              />
              <p className="text-gray-500">{job.experience_level}</p>
            </div>
            <div className="flex items-center space-x-2">
              <img
                width="36"
                height="36"
                src="https://img.icons8.com/?size=100&id=tUxN1SSkN8zG&format=png&color=000000"
                alt="salary"
              />
              <p className="text-gray-500">{job.salary_range} USD</p>
            </div>
            <div className="flex items-center space-x-2">
              <img
                width="36"
                height="36"
                src="https://img.icons8.com/?size=100&id=HvkLiNNdKM33&format=png&color=000000"
                alt="location"
              />
              <p className="text-gray-500">{job.location}</p>
            </div>
          </div>
        </div>
        <div className="flex justify-between items-between pb-20">
          <div className="w-2/3 pl-8 pr-2">
            <section className="mt-6">
              <h2 className="text-2xl font-semibold mt-4 mb-1">
                About the role
              </h2>
              <p className="mt-2 text-gray-700 text-md leading-loose">
                {job.description}
              </p>
            </section>
          </div>
          <div className="w-1/4 p-4">
            <div className="border rounded-md p-4 mb-6">
              <div className="flex justify-between items-center"></div>
              <button
                className="w-full mt-4 bg-[#c3f53c] text-lime-700 shadow-md border border-green-500 px-4 py-2 rounded-md"
                onClick={() => onApply(job.job_id)}
              >
                Apply now
              </button>
              <button
                className="w-full mt-4 bg-black shadow-md text-white px-4 py-2 rounded-md"
                onClick={() => onSave(job.job_id)}
              >
                Bookmark Job
              </button>
            </div>
            <div className="border p-4">
              <h3 className="text-lg font-semibold">About the job</h3>
              <p className="mt-2 text-gray-700">
                <strong>Apply before:</strong> Aug 10, 2024
              </p>
              <p className="text-gray-700">
                <strong>Posted on:</strong> Jun 11, 2024
              </p>
              <p className="text-gray-700">
                <strong>Job type:</strong> Full Time
              </p>
              <p className="text-gray-700">
                <strong>Experience level:</strong> Senior
              </p>
              <p className="text-gray-700">
                <strong>Salary:</strong> 160k-200k USD
              </p>
            </div>
          </div>
        </div>
      </div>
      {/* <Footer /> */}
    </div>
  );
};

export default JobListing;
