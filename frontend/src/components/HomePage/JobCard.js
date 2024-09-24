import React, { useState, useEffect } from "react";
import { toast } from "react-hot-toast";
import LoginModal from "./LoginModal";
import { useNavigate } from "react-router-dom";
import { ChevronRight, ChevronLeft, Hourglass } from "lucide-react";
import newTooltipGif from "../../assets/new-tooltip.gif"
import { icons } from "../../data/tech-icons";


const JobCard = ({ job, onSave, onApply, onView, isInSession, userData, userJobStatuses, onUnsave}) => {
  // const [isSaved, setIsSaved] = useState(false);
  // const [isApplied, setIsApplied] = useState(false);
   // Add a default value for userJobStatuses
   const isSaved = userJobStatuses.saved_jobs.includes(job.job_id);
  const isApplied = userJobStatuses.applied_jobs.includes(job.job_id);

  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [currentSlide, setCurrentSlide] = useState(0);

  const navigate = useNavigate();

  // useEffect(() => {
  //   if (isInSession) {
  //     checkIfJobIsSaved();
  //     checkIfJobIsApplied();
  //   }
  // }, [isInSession, job.job_id]);

  /* checkIfJobIsSaved and checkIfJobIsApplied functions should only be called when 'seeker' is logged in and not when recruiter*/
  const checkIfJobIsSaved = async () => {
    try {
      const response = await fetch(`/api/is_job_saved/${job.job_id}`, {
        method: 'GET',
        credentials: 'include',
      });
      const data = await response.json();
      setIsSaved(data.is_saved);
    } catch (error) {
      console.error("Error checking if job is saved:", error);
    }
  };

  const checkIfJobIsApplied = async () => {
    try {
      const response = await fetch(`/api/is_job_applied/${job.job_id}`, {
        method: 'GET',
        credentials: 'include',
      });
      const data = await response.json();
      setIsApplied(data.is_applied);
    } catch (error) {
      console.error("Error checking if job is applied:", error);
    }
  };

  // const handleSaveToggle = async () => {
  //   if (!isInSession) {
  //     setIsLoginModalOpen(true);
  //     return;
  //   }

  //   if (userData && userData.type =="recruiter") {
  //     toast.error("Cannot Save as a Recruiter");
  //     return;
  //   }

  //   try {
  //     if (isSaved) {
  //       await fetch(`/api/unsave_job/${job.job_id}`, {
  //         method: 'DELETE',
  //         credentials: 'include',
  //       });
  //       setIsSaved(false);
  //       toast.success("Job Unsaved.");
  //     } else {
  //       await onSave(job.job_id);
  //       setIsSaved(true);
  //       toast.success("Job Saved.");
  //     }
  //   } catch (error) {
  //     console.error("Error toggling job save status:", error);
  //     toast.error("Failed to save/unsave job.");
  //   }
  // };

  const handleSaveToggle = () => {
    if (!isInSession) {
      toast.error("Sign in first to save a job.");
      return;
    }

    if (isSaved) {
      onUnsave(job.job_id);
    } else {
      onSave(job.job_id);
    }
  };

 


  // const handleApply = async () => {
  //   if (!isInSession) {
  //     setIsLoginModalOpen(true);
  //     return;
  //   }

  //   if (userData && userData.type =="recruiter") {
  //     toast.error("Cannot Apply as a Recruiter");
  //     return;
  //   }

  //   try {
  //     navigate(`/job_post/${job.job_id}`);
  //     // setIsApplied(true);
  //     // toast.success("Application submitted successfully!");
  //   } catch (error) {
  //     console.error("Error applying to job:", error);
  //     toast.error("Failed to apply to job.");
  //   }
  // };

  const handleApply = () => {
    if (!isInSession) {
      toast.error("Sign in first to apply.");
      return;
    }

    onApply(job.job_id);
  };


  const nextSlide = () => {
    setCurrentSlide((prev) => (prev === 0 ? 1 : 0));
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev === 1 ? 0 : 1));
  };

  const techStackIcons = (job.tech_stack || []).filter(tech => icons[tech.toLowerCase()]);
  const displayedTechStack = techStackIcons.slice(0, 5);
  const remainingTechCount = techStackIcons.length - 5;

  return (
    <>
      <div className="relative flex items-center justify-between bg-zinc-50/50 p-4 border-b border-grey-200 mb-2 rounded-lg shadow-lg shadow-slate-200 cursor-pointer hover:bg-slate-100 hover:shadow-xl h-[100px] overflow-hidden">
        <div className="w-full h-full">
          {currentSlide === 0 ? (
            // First slide content
            <div className="flex items-center justify-between h-full">
              <div className="flex items-center">
                <img src={job.logo} alt={job.company} className="w-14 h-14 mr-4" />
                <div>
                  <h3
                    className="font-bold text-lg flex items-center hover:text-violet-500 text-slate-800"
                    style={{fontFamily: "Avenir, san-serif"}}
                    onClick={() => onView(job.job_id)}
                  >
                    {job.title}
                    {(job.created_at === "2 days ago" || job.created_at === "Today" || job.created_at === "1 week ago") && (
                      <img
                        src={newTooltipGif}
                        alt="New"
                        className="w-8 h-6 ml-3"
                      />
                    )}
                  </h3>
                  <div className="flex flex-wrap gap-2 pt-1" style={{fontFamily: "HeyWow, san-serif"}}>
                    <span className="bg-fuchsia-100 text-fuchsia-600 font-medium px-2 py-1 rounded-lg hover:underline cursor-pointer" onClick={() => navigate(`/company/${job.company_id}`)}>
                      {job.company}
                    </span>
                    <span className="text-gray-600 bg-lime-50 text-lime-600 font-medium px-2 py-1 rounded-lg">
                      {job.city}
                    </span>
                    <span className="text-gray-600 bg-orange-50 text-orange-700 px-2 py-1 rounded-lg">
                      {job.experience_level}
                    </span>
                    <span className="bg-cyan-50 text-cyan-700 px-2 py-1 rounded-lg">
                      {job.specialization}
                    </span>
                    {job.salary_range && job.salary_range !== 'Not Listed' && (
                      <span className="flex items-center bg-green-50 text-emerald-700 px-2 py-1 rounded-lg">
                        ${job.salary_range}
                      </span>
                    )}
                    {job.min_experience_years > 0 && (
                      <span className="bg-pink-50 text-pink-800 px-2 py-1 rounded-md">
                        {job.min_experience_years}+ Years
                      </span>
                    )}
                    <span className="text-gray-600 bg-purple-50 text-purple-700 px-2 py-1 rounded-lg">
                      {job.created_at}
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex space-x-2">
              <button
                  className={`px-4 py-2 border border-gray-300 rounded-md ${
                    isSaved
                      ? "bg-fuchsia-600 hover:bg-fuchsia-700 text-white"
                      : "hover:bg-lime-300"
                  }`}
                  onClick={handleSaveToggle}
                >
                  {isSaved ? "Unsave" : "Save"}
                </button>
                <button
                  className={`px-4 py-2 rounded-md ${
                    isApplied
                      ? "bg-lime-500 border border-emerald-600 text-white cursor-not-allowed"
                      : "bg-black hover:bg-violet-700 text-white"
                  }`}
                  onClick={() => onApply(job.job_id)}
                  disabled={isApplied}
                >
                  {isApplied ? "Applied" : "Apply"}
                </button>
              </div>
            </div>
          ) : (
            // Second slide content
            <div className="w-full h-full flex items-center justify-start bg-slate-50/50">
              <h2 className="items-center font-medium text-lg p-1 text-slate-700">Tech Stack:</h2>
              <div className="flex space-x-8 ml-10" style={{fontFamily: "Avenir, san-serif"}}>
                {displayedTechStack.map((tech) => (
                  <div key={tech} className="flex items-center justify-between pl-4 pr-4">
                   <img
                    src={icons[tech.toLowerCase()]}
                    alt={tech}
                    className="w-12 h-12 mr-4"
                  />
                  <span className="mt-1 text-md font-semibold font-medium text-slate-700 text-center items-center">{tech}</span>
                </div>
                ))}
                {remainingTechCount > 0 && (
                <div className="flex flex-col items-center justify-center">
                  <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-sm font-bold">
                    +{remainingTechCount}
                  </div>
                  <span className="mt-1 text-xs text-center">More</span>
                </div>
              )}
              </div>
            </div>
          )}
        </div> 
        {/* Navigation buttons */}
        <button 
          className="absolute top-1/2 right-0 transform -translate-y-1/3 bg-slate-100 rounded-md shadow-xs "
          onClick={nextSlide}
        >
          <ChevronRight size={14} />
        </button>
        <button 
          className="absolute top-1/2 left-0 transform -translate-y-1/3 bg-slate-100 rounded-md shadow-xs "
          onClick={prevSlide}
        >
          <ChevronLeft size={14} />
        </button>
      </div>
      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
      />
    </>
  );
};

export default JobCard;