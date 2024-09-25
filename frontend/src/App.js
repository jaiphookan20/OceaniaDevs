
import React, { useState, useEffect, useCallback, useRef } from "react";
import { Route, Routes, useNavigate, useLocation } from "react-router-dom";
import Navbar from "./components/HomePage/Navbar";
import Footer from "./components/HomePage/Footer";
import Header from "./components/HomePage/Header";
import JobSection from "./components/JobPostPage/JobSection";
import JobPost from "./components/JobPostPage/JobPost";
import { toast, Toaster } from "react-hot-toast";
import SavedAppliedJobSection from "./components/Seeker/SavedAppliedJobSection";
// import TrendingCompanies from "./components/TrendingCompanies";
import SearchPage from "./components/SearchPage/SearchPage";
import CompaniesPage from "./components/CompaniesPage/CompaniesPage";
import searchService from "./services/searchService";
import ApplicationTrackingDashboard from "./components/Seeker/ApplicationTrackingDashboard";
import RecruiterSettings from "./components/Recruiter/RecruiterSettings";
import RecruiterOnboarding from "./components/Recruiter/RecruiterOnboarding/RecruiterOnboarding";
import SignupFormRetro from "./components/HomePage/SignupFormRetro";
import SeekerSettings from "./components/Seeker/SeekerSettings";
import TrendingTechStackGrid from "./components/HomePage/TrendingTechStack";
import CompanyPage from "./components/CompanyPage/CompanyPage";
import PostJob from "./components/Recruiter/PostJob";
import PostJobWithAI from "./components/Recruiter/PostJobWithAI";
import RecruiterDashboard from "./components/Recruiter/RecruiterDashboard/RecruiterDashboard";
import EditJob from "./components/Seeker/EditJob";
import HashLoader from "react-spinners/HashLoader";
import { debounce } from 'lodash';  // Make sure to install and import lodash
import JobBoardProfile from "./components/Misc/JobBoardProfile";
import RecruiterLandingPage from "./components/Recruiter/RecruiterLandingPage";

const App = () => {
  const [homePageJobs, setHomePageJobs] = useState([]);
  const [allJobs, setAllJobs] = useState([]);
  const [savedJobs, setSavedJobs] = useState([]);
  const [appliedJobs, setAppliedJobs] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isInSession, setIsInSession] = useState(false);
  const [searchTitle, setSearchTitle] = useState("Technology");
  const [isInOnboarding, setIsInOnboarding] = useState(false);
  const [specialization, setSpecialization] = useState("");
  const [loading, setLoading] = useState(false);
  const [userData, setUserData] = useState([]);
  const [userJobStatuses, setUserJobStatuses] = useState({ saved_jobs: [], applied_jobs: [] });
  
  const [filters, setFilters] = useState({
    specialization: "",
    experience_level: "",
    location: "",
    work_location: "",
    job_arrangement: "",
    tech_stack: [],
  });

  const prevFilters = useRef(filters);

  const [currentPage, setCurrentPage] = useState(1);
  const [totalJobs, setTotalJobs] = useState(0);
  const pageSize = 10;

  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Scroll to the top of the page when the location changes
    window.scrollTo(0, 0);
  }, [location]);

  useEffect(() => {
    fetchHomePageJobs(); /* Should be called only when we're in the home page? */
    fetchAllJobs(); 
    checkSession();
  }, []);

  useEffect(() => {
    if (isInSession) {
      fetchUserJobStatuses();
    }
  }, [isInSession]);

  const fetchUserJobStatuses = async () => {
    try {
      const response = await fetch('/api/user_job_statuses', {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setUserJobStatuses(data);
      }
    } catch (error) {
      console.error('Error fetching user job statuses:', error);
    }
  };

  const checkSession = async () => {
    try {
      const response = await fetch(`/api/check-session`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      const data = await response.json();
      if (data.userinfo) {
        setUserData(data);
      }
     
      if (data.userinfo) {
        console.log(`${data.userinfo.name} is in session`);
        setIsInSession(true);
      } else {
        setIsInSession(false);
      }
    } catch (error) {
      console.error("Error checking session:", error);
    }
  };

  useEffect(() => {
    if (isInSession) {
      if (location.pathname === "/saved-jobs") {
        fetchSavedJobs();
      } else if (location.pathname === "/applied-jobs") {
        fetchAppliedJobs();
      }
    }
  }, [location, isInSession]);
  
  const fetchHomePageJobs = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/home_page_jobs`, {
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      if (!response.ok) {
        setLoading(false);
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setHomePageJobs(data.jobs);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching home page jobs:", error);
      setLoading(false);
    }
  };

const fetchAllJobs = async (page = 1, filters = {}) => {
  try {
    const response = await searchService.filteredSearchJobs({...filters, page, page_size: pageSize});
    setAllJobs(response.jobs);
    setTotalJobs(response.total_jobs);
    return response;
  } catch (error) {
    console.error("Error fetching all jobs:", error);
    return { jobs: [], total_jobs: 0 };
  }
};


const handleSave = useCallback(async (jobId) => {
  if (!isInSession) {
    toast.error("Please sign in to save a job.");
    return;
  }

  try {
    const response = await fetch(`/api/bookmark_job`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ jobid: jobId }),
    });
    if (response.ok) {
      setUserJobStatuses(prev => ({
        ...prev,
        saved_jobs: [...prev.saved_jobs, jobId]
      }));
      toast.success("Job saved successfully");
    } else {
      toast.error("Failed to save job");
    }
  } catch (error) {
    console.error("Error saving job:", error);
    toast.error("Failed to save job");
  }
}, [isInSession]);

const handleUnsave = useCallback(async (jobId) => {
  if (!isInSession) {
    toast.error("Please sign in to unsave a job.");
    return;
  }

  try {
    const response = await fetch(`/api/unsave_job/${jobId}`, {
      method: 'DELETE',
      credentials: 'include',
    });
    if (response.ok) {
      setUserJobStatuses(prev => ({
        ...prev,
        saved_jobs: prev.saved_jobs.filter(id => id !== jobId)
      }));
      toast.success("Job unsaved successfully");
    } else {
      toast.error("Failed to unsave job");
    }
  } catch (error) {
    console.error("Error unsaving job:", error);
    toast.error("Failed to unsave job");
  }
}, [isInSession]);

const handleApply = useCallback(async (jobId) => {
  if (!isInSession) {
    toast.error("Please sign in to apply for a job.");
    return;
  }

  try {
    const response = await fetch(`/api/apply_job`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ jobid: jobId }),
    });
    const data = await response.json();
    if (response.ok) {
      setUserJobStatuses(prev => ({
        ...prev,
        applied_jobs: [...prev.applied_jobs, jobId]
      }));
      toast.success(data.message || "Application submitted successfully");
    } else {
      toast.error(data.error || "Failed to submit application");
    }
  } catch (error) {
    console.error("Error applying to job:", error);
    toast.error("Failed to submit application. Please try again later.");
  }
}, [isInSession]);

  const handleView = (jobId) => {
    navigate(`/job_post/${jobId}`);
  };

  const handleSearch = (event) => {
    const searchValue = event.target.value;
    setSearchQuery(searchValue);
  };
  

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFilters(prevFilters => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  const handleViewAllRoles = (specialize) => {
    setSpecialization(specialize);
    setFilters(prevFilters => {
      const newFilters = {
        ...prevFilters,
        specialization: specialize,
        tech_stack: []
      };
      setSearchTitle(`${specialize} Jobs`);
      setCurrentPage(1);
      fetchAllJobs(1, newFilters).then(data => {
        setAllJobs(data.jobs);
        setTotalJobs(data.total_jobs);
        navigate('/search-page');
      });
      return newFilters;
    });
  };

  

  // const handleFilterSearch = useCallback(async (page = 1) => {
  //   try {
  //     const data = await searchService.filteredSearchJobs({...filters, query: searchQuery, page, page_size: pageSize});
      
  //     setAllJobs(data.jobs);
  //     setTotalJobs(data.total_jobs);
  //     setCurrentPage(page);

  //     if (searchQuery) {
  //       setSearchTitle(`Results for "${searchQuery}"`);
  //     } else if (filters.tech_stack.length > 0) {
  //       setSearchTitle(`${filters.tech_stack[0].charAt(0).toUpperCase() + filters.tech_stack[0].slice(1)} Jobs`);
  //     } else if (filters.specialization) {
  //       setSearchTitle(`${filters.specialization} Jobs`);
  //     } else {
  //       setSearchTitle("Technology Jobs");
  //     }

  //     prevFilters.current = {...filters};

  //   } catch (error) {
  //     console.error('Error fetching filtered jobs:', error);
  //     setAllJobs([]);
  //     setTotalJobs(0);
  //     toast.error("Failed to fetch jobs. Please try again later.");
  //   }
  // }, [filters, searchQuery, pageSize]);

  const handleFilterSearch = useCallback(async (page = 1, newFilters = null, newQuery = null) => {
  try {
    const filtersToUse = newFilters || filters;
    const queryToUse = newQuery !== null ? newQuery : searchQuery;
    
    const data = await searchService.filteredSearchJobs({
      ...filtersToUse, 
      query: queryToUse, 
      page, 
      page_size: pageSize
    });
    
    setAllJobs(data.jobs);
    setTotalJobs(data.total_jobs);
    setCurrentPage(page);

    if (newFilters) setFilters(newFilters);
    if (newQuery !== null) setSearchQuery(newQuery);

    if (queryToUse) {
      setSearchTitle(`Results for "${queryToUse}"`);
    } else if (filtersToUse.tech_stack.length > 0) {
      setSearchTitle(`${filtersToUse.tech_stack[0].charAt(0).toUpperCase() + filtersToUse.tech_stack[0].slice(1)} Jobs`);
    } else if (filtersToUse.specialization) {
      setSearchTitle(`${filtersToUse.specialization} Jobs`);
    } else {
      setSearchTitle("Technology Jobs");
    }

    prevFilters.current = {...filtersToUse};

  } catch (error) {
    console.error('Error fetching filtered jobs:', error);
    setAllJobs([]);
    setTotalJobs(0);
    toast.error("Failed to fetch jobs. Please try again later.");
  }
}, [filters, searchQuery, pageSize]);

  const fetchSavedJobs = async () => {
    try {
      const response = await fetch(`/api/bookmarked_jobs`, {
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setSavedJobs(data.bookmarked_jobs);
    } catch (error) {
      console.error("Error fetching saved jobs:", error);
    }
  };

  const fetchAppliedJobs = async () => {
    try {
      const response = await fetch(`/api/applied_jobs`, {
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setAppliedJobs(data.applied_jobs);
    } catch (error) {
      console.error("Error fetching applied jobs:", error);
    }
  };

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    if (searchQuery.trim() !== "") {
      searchService.instantSearchJobs(searchQuery, newPage, pageSize).then(data => {
        setAllJobs(data.results);
        setTotalJobs(data.total);
      });
    } else {
      handleFilterSearch(newPage);
    }
  };


  useEffect(() => {
    const onboardingPaths = [
      '/employer/add-details',
      '/employer/new/organization-details',
      '/employer/organization-details',
      '/employer/verify-email',
      '/employer/verify-code'
    ];
    setIsInOnboarding(onboardingPaths.includes(location.pathname));
  }, [location]);

  const removeBookmark = async (jobId) => {
    try {
      const response = await fetch('/api/remove_bookmark', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ jobid: jobId }),
      });
      if (response.ok) {
        setSavedJobs(savedJobs.filter(job => job.job_id !== jobId));
      }
    } catch (error) {
      console.error("Error removing bookmark:", error);
    }
  };

  const removeApplication = async (jobId) => {
    try {
      const response = await fetch(`/api/remove_application/${jobId}`, {
        method: 'DELETE',
        credentials: 'include',
      });
      if (response.ok) {
        setAppliedJobs(prevJobs => prevJobs.filter(job => job.job_id !== jobId));
        toast.success("Application removed successfully");
      } else {
        toast.error("Failed to remove application");
      }
    } catch (error) {
      console.error("Error removing application:", error);
      toast.error("Error removing application");
    }
  };


  const handleClearAll = async () => {
    setSearchQuery("");
    setSearchTitle("Technology");
    setFilters({
      specialization: "",
      experience_level: "",
      city: "",
      industry: "",
      tech_stack: [],
      salary_range: "",
    });
    fetchAllJobs(1);
  };

  const fetchMoreSavedJobs = async (page, pageSize) => {
    try {
      const response = await fetch(`/api/bookmarked_jobs?page=${page}&page_size=${pageSize}`, {
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data.bookmarked_jobs || [];
    } catch (error) {
      console.error("Error fetching more saved jobs:", error);
      return [];
    }
  };


  const fetchMoreAppliedJobs = async (page, pageSize) => {
    try {
      const response = await fetch(`/api/applied_jobs?page=${page}&page_size=${pageSize}`, {
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data.applied_jobs || [];
    } catch (error) {
      console.error("Error fetching more applied jobs:", error);
      return [];
    }
  };

  const handleTechFilter = (tech) => {
    setFilters(prevFilters => {
      const newFilters = {
        ...prevFilters,
        tech_stack: [tech],
        specialization: ''
      };
      setSearchTitle(`${tech.charAt(0).toUpperCase() + tech.slice(1)} Jobs`);
      fetchAllJobs(1, newFilters).then(data => {
        setAllJobs(data.jobs);
        setTotalJobs(data.total_jobs);
      });
      return newFilters;
    });
    navigate('/search-page');
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <HashLoader color="#8823cf" size={120} />
      </div>
    );
}

  return (
    <div className="bg-slate-40 p-6" style={{ fontFamily: "Roobert-Regular, sans-serif" }}>
      <Toaster />
      {!isInOnboarding && <Navbar />}
      <Routes>
        <Route
          exact
          path="/"
          element={
            <>
              <Header />
              {/* <TrendingCompanies /> */}
              <TrendingTechStackGrid />
              {/* <JobAlertPopup /> */}
              <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-1 gap-7">
                <div className="col-span-2">
                  {Object.entries(homePageJobs).map(([specialization, jobsList]) => (
                    <JobSection
                      key={specialization}
                      title={`${specialization} Roles`}
                      jobs={jobsList}
                      onSave={handleSave}
                      onApply={handleApply}
                      onView={handleView}
                      currentPage={currentPage}
                      totalJobs={totalJobs}
                      pageSize={pageSize}
                      onPageChange={handlePageChange}
                      isInSession={isInSession}
                      onViewAll={() => handleViewAllRoles(specialization)}
                      userData={userData}
                      onUnsave={handleUnsave}
                      userJobStatuses={userJobStatuses}
                    />
                  ))}
                </div>
              </div>
              <SignupFormRetro />
            </>
          }
        />
        <Route
          path="/search-page"
          element={
            <SearchPage
              title={searchTitle}
              jobs={allJobs}
              onSave={handleSave}
              onApply={handleApply}
              onView={handleView}
              currentPage={currentPage}
              totalJobs={totalJobs}
              pageSize={pageSize}
              onPageChange={handlePageChange}
              searchQuery={searchQuery}
              filters={filters}
              onSearchChange={handleSearch}
              onFilterChange={handleChange}
              onFilterSearch={handleFilterSearch}
              isInSession={isInSession}
              specialization={specialization}
              onClearAll={handleClearAll}
              onTechFilter={handleTechFilter}
              onUnsave={handleUnsave}
              userJobStatuses={userJobStatuses}
            />
          }
        />
        <Route path="/employer/*" element={<RecruiterOnboarding />} />
        <Route
          path="/companies"
          element={
            <CompaniesPage
              title={searchTitle}
              jobs={allJobs}
              onSave={handleSave}
              onApply={handleApply}
              onView={handleView}
              currentPage={currentPage}
              totalJobs={totalJobs}
              pageSize={pageSize}
              onPageChange={handlePageChange}
              searchQuery={searchQuery}
              filters={filters}
              onSearchChange={handleSearch}
              onFilterChange={handleChange}
              onFilterSearch={handleFilterSearch}
            />
          }
        />
        <Route 
          path="/company/:companyId" 
          element={
            <CompanyPage 
              onSave={handleSave}
              onApply={handleApply}
              onView={handleView}
            />
          } 
        />
        <Route path="/employer/post-job" element={<PostJob />} />
        <Route path="/employer/post-job-ai" element={<PostJobWithAI />} />
        <Route path="/dashboard" element={<ApplicationTrackingDashboard />} />
        <Route path="/recruiter-dashboard" element={<RecruiterDashboard />} />
        <Route path="/recruiter-settings" element={<RecruiterSettings />} />
        <Route path="/edit-job/:jobId" element={<EditJob />} />z
        <Route
          path="/job_post/:jobId"
          element={<JobPost onSave={handleSave} onApply={handleApply} isInSession={isInSession} userJobStatuses={userJobStatuses} onUnsave={handleUnsave} />}
        />
        {/* <Route path="/profile" element={<DeveloperProfile />} /> */}
        <Route path="/profile" element={<JobBoardProfile />} />
        <Route path="/recruiter-page" element={<RecruiterLandingPage />} />
        <Route
          path="/saved-jobs"
          element={
            <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-7">
              <div className="col-span-2">
                <SavedAppliedJobSection
                  title="Saved Jobs"
                  jobs={savedJobs}
                  onApply={handleApply}
                  onView={handleView}
                  fetchMoreJobs={fetchMoreSavedJobs}
                  onRemove={removeBookmark}
                  isSavedJobs={true}
                />
              </div>
            </div>
          }
        />
        <Route
          path="/applied-jobs"
          element={
            <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-7">
              <div className="col-span-2">
                <SavedAppliedJobSection
                  title="Applied Jobs"
                  jobs={appliedJobs}
                  onApply={handleApply}
                  onView={handleView}
                  fetchMoreJobs={fetchMoreAppliedJobs}
                  onRemove={removeApplication}
                  isSavedJobs={false}
                />
              </div>
            </div>
          }
        />
        <Route path="/seeker/settings" element={<SeekerSettings />} />
      </Routes>
      {!isInOnboarding && <Footer />}
    </div>
  );
};

export default App;