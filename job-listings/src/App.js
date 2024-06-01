import React, { useEffect, useState } from "react";
import Navbar from "./Navbar";
import Header from "./Header";
import styles from "./SignupForm.module.css";

const JobCard = ({ job }) => {
  return (
    <div className="flex items-center justify-between p-4 border-b border-grey-200 mb-2 rounded-lg shadow-md shadow-slate-200/50	">
      <div className="flex items-center ">
        <img src={job.logo} alt={job.company} className="w-14 h-14 mr-4" />
        <div>
          <h3 className="font-bold text-lg flex items-center">
            {job.title}
            {job.new && (
              <img
                src="https://remoteok.com/assets/new2x.gif"
                alt="New"
                className="w-8 h-6 ml-3"
              />
            )}
          </h3>
          <p className="text-gray-600 space-x-4">
            {job.company} • {job.location} • {job.experience_level}
          </p>
          {/* • {job.salary} • {job.date} */}
        </div>
      </div>
      <div className="flex space-x-2">
        <button className="px-4 py-2 border border-gray-300 hover:bg-lime-300 rounded-md">
          Save
        </button>
        <button className="px-4 py-2 bg-violet-400 hover:bg-violet-700 text-white rounded-md">
          Apply
        </button>
      </div>
    </div>
  );
};

const JobSection = ({ title, jobs }) => {
  return (
    <div>
      <div className="flex justify-between items-center mb-4 hover:cursor-pointer">
        <h2 className="text-3xl font-bold">{title}</h2>
        <a href="#" className="text-indigo-600">
          View all {title.toLowerCase()}
        </a>
      </div>
      <div className="bg-white rounded-lg shadow-md cursor-pointer">
        {jobs.map((job, index) => (
          <JobCard key={index} job={job} />
        ))}
      </div>
    </div>
  );
};

const SignupForm = () => {
  return (
    <div className={`${styles.ctHomeBox} ${styles.ctHomeBoxNl}`}>
      <div className="text-left">
        <h2 className="text-xl font-bold mb-4">
          Stay in the loop: Get your dose of frontend twice a week
        </h2>
        <p className="mb-4">
          👾 <strong>Hey! Looking for the latest in frontend?</strong> Twice a
          week, we'll deliver the freshest frontend news, website inspo, cool
          code demos, videos and UI animations right to your inbox.
        </p>
        <p className="mb-6">
          <strong>Zero fluff, all quality,</strong> to make your Mondays and
          Thursdays more creative!
        </p>
        <form className="flex flex-col space-y-3">
          <input
            type="email"
            placeholder="Your email"
            className="px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400"
          />
          <button className="px-4 py-2 text-white bg-black rounded-md shadow-md hover:bg-gray-800">
            Subscribe
          </button>
        </form>
        <a href="#" className="mt-3 inline-block text-indigo-600">
          Find out more →
        </a>
      </div>
    </div>
  );
};

const App = () => {
  const [jobs, setJobs] = useState([]);
  // const [frontendJobs, setFrontendJobs] = useState([]);
  // const [devOpsJobs, setDevopsJobs] = useState([]);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch("http://127.0.0.1:4040/alljobs", {
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // setJobs(data.filter((job) => job.specialization === "Backend"));
        setJobs(data);
        // setFrontendJobs(
        //   data.filter((job) => job.specialization === "Frontend")
        // );
        // setDevopsJobs(data.filter((job) => job.specialization === "DevOps"));
      } catch (error) {
        console.error("Error fetching jobs:", error);
      }
    };

    fetchJobs();
  }, []);

  return (
    <div
      className="bg-slate-30 p-6"
      // style={{ fontFamily: "HeyWow, sans-serif" }}
      style={{ fontFamily: "Roobert-Regular, sans-serif" }}
    >
      <Navbar />
      <Header />
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="col-span-2">
          <JobSection title="Engineering Jobs" jobs={jobs} />
          {/* <div className="mt-8">
            <JobSection title="Frontend jobs" jobs={frontendJobs} />
          </div>
          <div className="mt-8">
            <JobSection title="DevOps jobs" jobs={devOpsJobs} />
          </div> */}
        </div>
        <SignupForm />
      </div>
    </div>
  );
};

export default App;
