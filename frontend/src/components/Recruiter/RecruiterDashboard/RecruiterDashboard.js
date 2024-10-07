import React, { useState, useEffect } from "react";
import RecruiterJobSection from "./RecruiterJobSection";
import { useNavigate } from "react-router-dom";
import RecruiterNoActiveJobsCard from "./RecruiterNoActiveJobsCard";
import RecruiterDashboardHeader from "./RecruiterDashboardHeader";
import RecruiterOnboardingIncompleteCard from "../RecruiterOnboarding/RecruiterOnboardingIncompleteCard";
import RecruiterDashboardConfirmationModal from "./RecruiterDashboardConfirmationModal";

const RecruiterDashboard = () => {
  const [activeJobs, setActiveJobs] = useState([]);
  const [expiredJobs, setExpiredJobs] = useState([]);
  const [onboardingComplete, setOnboardingComplete] = useState(true);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [jobToRemove, setJobToRemove] = useState(null);

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

  useEffect(() => {
    const checkOnboardingStatus = async () => {
      try {
        const response = await fetch('/api/check_onboarding_status', {
          method: 'GET',
          credentials: 'include',
        });
        if (response.ok) {
          const data = await response.json();
          setOnboardingComplete(data.onboardingComplete);
        } else {
          console.error('Failed to fetch onboarding status');
        }
      } catch (error) {
        console.error('Error checking onboarding status:', error);
      }
    };
  
    checkOnboardingStatus();
  }, []);

   // Update the handleRemove function
   const handleRemove = (jobId) => {
    setJobToRemove(jobId);
    setShowConfirmModal(true);
  };

  const confirmRemove = async () => {
    if (jobToRemove) {
      try {
        const response = await fetch(`/api/remove-job-by-recruiter/${jobToRemove}`, {
          method: "POST",
          credentials: "include",
        });
        if (response.ok) {
          console.log(`Job with jobId ${jobToRemove} successfully removed`);
          setActiveJobs(activeJobs.filter((job) => job.job_id !== jobToRemove));
          setExpiredJobs(expiredJobs.filter((job) => job.job_id !== jobToRemove));
        } else {
          console.error(`Failed to remove jobId ${jobToRemove}`);
        }
      } catch (error) {
        console.error("Error removing job:", error);
      }
    }
    setShowConfirmModal(false);
    setJobToRemove(null);
  };

  const cancelRemove = () => {
    setShowConfirmModal(false);
    setJobToRemove(null);
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <RecruiterDashboardHeader title="Recruiter Dashboard" />
      {!onboardingComplete ? (
        <RecruiterOnboardingIncompleteCard />
      ) : (
        <>
          <RecruiterJobSection
            activeJobs={activeJobs}
            expiredJobs={expiredJobs}
            onEdit={handleEdit}
            onView={(jobId) => navigate(`/job_post/${jobId}`)}
            onRemove={handleRemove}
          />
          <RecruiterDashboardConfirmationModal
            isOpen={showConfirmModal}
            onConfirm={confirmRemove}
            onCancel={cancelRemove}
            message="Are you sure you want to remove this job?"
          />
        </>
      )}
    </div>
  );
};

export default RecruiterDashboard;


