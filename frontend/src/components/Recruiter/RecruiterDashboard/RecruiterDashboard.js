import React, { useState, useEffect } from "react";
import RecruiterJobSection from "./RecruiterJobSection";
import { useNavigate } from "react-router-dom";

const RecruiterDashboard = () => {
  const [activeJobs, setActiveJobs] = useState([]);
  const [expiredJobs, setExpiredJobs] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch("/api/jobs_by_recruiter", {
          method: "GET",
          credentials: "include",
        });
        if (response.ok) {
          const jobsData = await response.json();
          setActiveJobs(jobsData.active_jobs);
          setExpiredJobs(jobsData.expired_jobs);
        } else {
          console.error("Failed to fetch jobs.");
        }
      } catch (error) {
        console.error("Error fetching jobs:", error);
      }
    };
    fetchJobs();
  }, []);

  const handleEdit = (jobId) => {
    navigate(`/edit-job/${jobId}`);
  };

  const handleRemove = async (jobId) => {
    try {
      const response = await fetch(`/api/remove-job-by-recruiter/${jobId}`, {
        method: "POST",
        credentials: "include",
      });
      if (response.ok) {
        console.log(`Job with jobId ${jobId} successfully removed`);
        setActiveJobs(activeJobs.filter((job) => job.job_id !== jobId));
        setExpiredJobs(expiredJobs.filter((job) => job.job_id !== jobId));
      } else {
        console.error(`Failed to remove jobId ${jobId}`);
      }
    } catch (error) {
      console.error("Error removing job:", error);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <RecruiterJobSection
        title="Recruiter Dashboard"
        activeJobs={activeJobs}
        expiredJobs={expiredJobs}
        onEdit={handleEdit}
        onView={(jobId) => navigate(`/job_post/${jobId}`)}
        onRemove={handleRemove}
      />
    </div>
  );
};

export default RecruiterDashboard;


