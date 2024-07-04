import React, { useState, useEffect } from "react";
import JobsPostedByRecruiterSection from "./JobsPostedByRecruiterSection";
import { useNavigate } from "react-router-dom";

const RecruiterDashboard = () => {
  const [jobs, setJobs] = useState([]);
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
          setJobs(jobsData);
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
    // Navigate to the EditJob page with jobId
    navigate(`/edit-job/${jobId}`);
  };

  return (
    <div className="max-w-5xl mx-auto">
      <JobsPostedByRecruiterSection
        title="Posted Jobs"
        jobs={jobs}
        onEdit={handleEdit}
        onView={(jobId) => navigate(`/job_post/${jobId}`)}
      />
    </div>
  );
};

export default RecruiterDashboard;
