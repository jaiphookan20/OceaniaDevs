import React, { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import { icons } from "../../data/tech-icons";
import JobPostSideBar from "./JobPostSideBar";
import RecommendedJobs from "./RecommendedJobs";
import HashLoader from "react-spinners/HashLoader";
import { useNavigate } from "react-router-dom";
import { getRelativeTimeString } from '../../utils/time';
import greenTick from '../../assets/green-tick.svg';
import industryIcon from '../../assets/jobpost/industry-icon.webp';
import experienceIcon from '../../assets/jobpost/experience-icon.webp';
import salaryIcon from '../../assets/jobpost/salary-icon.webp';
import locationIcon from '../../assets/jobpost/location-icon.webp';
import minExperienceIcon from '../../assets/jobpost/min-experience-icon.webp';
import specialisationIcon from '../../assets/jobpost/specialisation-icon.webp';
import workLocationIcon from '../../assets/jobpost/work-location-icon.webp';
import jobArrangementIcon from '../../assets/jobpost/job-arrangement-icon.webp';  

const JobPost = ({ onSave, onApply, isInSession, userJobStatuses, onUnsave }) => {
  const { jobId } = useParams();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const technologiesRef = useRef(null);
  const [recommendedJobs, setRecommendedJobs] = useState([]);
  const [showDescription, setShowDescription] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [isApplied, setIsApplied] = useState(false);
  const [applicationDate, setApplicationDate] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchRecommendedJobs = async () => {
      try {
        const response = await fetch(`/api/recommended_jobs/${jobId}`);
        const data = await response.json();
        setRecommendedJobs(data);
      } catch (error) {
        console.error("Error fetching recommended jobs:", error);
      }
    };
  
    if (job) {
      fetchRecommendedJobs();
    }
  }, [job, jobId]);
  
  useEffect(() => {
    if (userJobStatuses && job) {
      setIsSaved(userJobStatuses.saved_jobs.includes(job.job_id));
      setIsApplied(userJobStatuses.applied_jobs.includes(job.job_id));
    }
  }, [userJobStatuses, job]);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const response = await fetch(`/api/job_post/${jobId}`);
        const data = await response.json();
        if (response.ok) {
          setJob(data);
          // Set the application date if the job has been applied to
          if (data.application_date) {
            setApplicationDate(new Date(data.application_date));
          }
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
    return (
      <div className="flex justify-center items-center h-screen">
        <HashLoader color="#8823cf" size={120} />
      </div>
    );
  }

  if (error) {
    return <div>{error}</div>;
  }
  console.log(job.tech_stack)
  const techStackIcons = job.tech_stack.filter(tech => icons[tech.toLowerCase()]);
  const scrollToTechnologies = () => {
    technologiesRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Helper function to parse the custom string format
  const parseCustomString = (str) => {
    if (typeof str !== 'string') {
      console.warn("Input is not a string:", str);
      return [];
    }
    // Remove the outer curly braces and split by ","
    const items = str.replace(/^\{|\}$/g, '').split('","');
    // Remove any remaining quotes and trim whitespace
    return items.map(item => item.replace(/^"|"$/g, '').trim());
  };

  const responsibilities = parseCustomString(job.responsibilities[0]);
  const requirements = parseCustomString(job.requirements[0]);
  
  return (
    <div className="flex flex-col max-w-6xl mx-auto min-h-screen justify-center">
      <div className="flex-grow container mx-auto bg-white shadow-lg rounded-lg border border-slate-400 ">
      <header className="flex justify-between pb-1 mb-4">
          <div className="flex items-center">
            <img src={job.company_logo_url} alt={job.company_name} className="w-20 h-20 object-contain bg-white" />
          </div>
          <div className="flex mt-4 space-x-4 pr-4 items-center">
            {techStackIcons.slice(0, 5).map((tech) => (
              <div
                key={tech}
                className="p-2 rounded-md flex items-center space-x-2"
              >
                <img
                  src={icons[tech.toLowerCase()]}
                  alt={tech}
                  className="w-20 h-20"
                />
              </div>
            ))}
            {techStackIcons.length > 5 && (
              <div 
                className="cursor-pointer bg-slate-600 text-white text-4xl rounded-full w-16 h-16 flex items-center justify-center text-3xl font-bold text-gray-600 hover:bg-gray-300"
                onClick={scrollToTechnologies}
              >
                +
              </div>
            )}
          </div>
        </header>
        <div className="ml-4">
          <h1 className="text-5xl font-bold">{job.title}</h1>
          <div className="flex justify-between">
            <h3 className="text-3xl pt-2 text-slate-500 font-semibold hover:text-slate-700 hover:cursor-pointer" onClick={()=> navigate(`/company/${job.company_id}`)}>
              {job.company}
            </h3>
            <p className="items-bottom p-2 text-xl text-emerald-700 font-semibold">{getRelativeTimeString(job.created_at)}</p>
          </div>
          <p className="text-gray-500 mt-2 text-xl">
            {job.company_description}
          </p>
        </div>
        <div className="grid grid-cols-4 gap-6 mt-6 p-4 bg-[#f5f5ec] border-t border-b border-slate-400 rounded-md shadow-sm">
  {[
    { icon: industryIcon, label: "Industry", value: job.industry },
    { icon: experienceIcon, label: "Experience", value: job.experience_level },
    { icon: salaryIcon, label: "Salary", value: job.salary_range !== 'Not Listed' ? `${job.salary_range} AUD` : 'Not Listed'},
    { icon: locationIcon, label: "Location", value: job.location },
    { icon: minExperienceIcon, label: "Min. Experience", value: job.min_experience_years > 0 ? `${job.min_experience_years}+ Years` : 'Not Listed' },
    { icon: specialisationIcon, label: "Specialization", value: job.specialization },
    { icon: workLocationIcon, label: "Work Location", value: job.work_location },
    { icon: jobArrangementIcon, label: "Job Arrangement", value: job.job_arrangement }
  ].map((item, index) => (
    <div key={index} className="flex flex-col items-center p-2 bg-white rounded-md shadow-sm border border-slate-400 transition-all duration-300 hover:shadow-md">
      <img
        width="40"
        height="40"
        src={item.icon}
        alt={item.label}
        className="mb-2"
      />
      <p className="text-sm text-slate-600 mb-1 font-medium" style={{fontFamily: "HeyWow, sans-serif"}}>{item.label}</p>
      <p className="text-md font-bold text-gray-700 text-center" style={{ fontFamily: "Avenir, sans-serif" }}>{item.value}</p>
    </div>
  ))}
</div>
            <div className="flex justify-between items-between pxb-20">
          <div className="w-3/4 pl-8 pr-2">
          {/* Add this conditional rendering for the applied status */}
          {isApplied && applicationDate && (
              <div className="flex justify-start font-semibold text-emerald-600 px-4 py-1 mt-4 rounded-lg relative mb-4" role="alert">
                <div className="flex text-center items-center">
                  <img src={greenTick} alt="Green Tick" className="w-4 h-4 mr-2" />
                  <span className="block sm:inline">Applied on External Website | October 7th</span>
                </div>
              </div>
            )}
            <section className="mt-6">
              <h2 className="text-3xl font-semibold mt-4 mb-1 text-slate-800" style={{ fontFamily: "Avenir, sans-serif" }}>
                About the role
              </h2>
              <p className="mt-2 text-slate-600 text-md leading-loose" style={{ fontFamily: "Avenir, sans-serif" }}>
                {job.overview}
              </p>
            </section>
            <section className="mt-6">
              <h2 className="text-3xl font-semibold mt-4 mb-1 text-slate-800" style={{ fontFamily: "Avenir, sans-serif" }}>
                Responsibilities
              </h2>
              <ul className="list-disc pl-5 mt-2 text-slate-600 text-md leading-loose" style={{ fontFamily: "Avenir, sans-serif" }}>
                {responsibilities.map((responsibility, index) => (
                  <li key={index}>{responsibility}</li>
                ))}
              </ul>
            </section>
            <section className="mt-6">
              <h2 className="text-3xl font-semibold mt-4 mb-1 text-slate-800"  style={{ fontFamily: "Avenir, sans-serif" }}>
                Requirements
              </h2>
              <ul className="list-disc pl-5 mt-2 text-slate-600 text-md leading-loose" style={{ fontFamily: "Avenir, sans-serif" }}>
                {requirements.map((requirement, index) => (
                  <li key={index}>{requirement}</li>
                ))}
              </ul>
            </section>
            {/* New toggle section for job description */}
            <section className="mt-6">
              <h2 
                className="text-3xl font-semibold mt-4 mb-1 text-slate-800 cursor-pointer flex items-center"
                style={{ fontFamily: "Avenir, sans-serif" }}
                onClick={() => setShowDescription(!showDescription)}
              >
                Full Job Description
                <span className="ml-2">{showDescription ? '▲' : '▼'}</span>
              </h2>
              {showDescription && (
                <p className="mt-2 text-slate-600 text-md leading-loose" style={{ fontFamily: "Avenir, sans-serif" }}>
                  {job.description}
                </p>
              )}
            </section>
            <section ref={technologiesRef} className="mt-6" style={{ fontFamily: "Avenir, sans-serif" }}>
              <h2 className="text-3xl font-semibold mt-4 mb-1 text-slate-800">
                Tech Stack
              </h2>
              <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-4 mt-4 border border-slate-400 rounded-lg">
                {techStackIcons.map((tech) => (
                  <div
                    key={tech}
                    className="flex flex-col items-center justify-center p-2 rounded-md"
                  >
                    <img
                      src={icons[tech.toLowerCase()]}
                      alt={tech}
                      className="w-16 h-16"
                    />
                    <span className="mt-2 text-md text-slate-700 font-semibold text-center">{tech.charAt(0).toUpperCase() + tech.slice(1).toLowerCase()}</span>
                  </div>
                ))}
              </div>
            </section>
          </div>
          <div className="w-1/4 p-4">
            <JobPostSideBar job={job} onSave={onSave} onApply={onApply} isInSession={isInSession} onUnsave={onUnsave} isSaved={isSaved} isApplied={isApplied} />
          </div>
        </div>
        <RecommendedJobs jobs={recommendedJobs} />
      </div>
    </div>
  );
};

export default JobPost;
