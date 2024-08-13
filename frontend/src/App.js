import React, { useState, useEffect } from "react";
import { Route, Routes, useNavigate, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Header from "./components/Header";
import JobSection from "./components/JobSection";
import SignupForm from "./components/SignupForm";
import BottomContainer from "./components/BottomContainer";
import SearchBar from "./components/SearchBar";
import JobPost from "./components/JobPost";
import { toast, Toaster } from "react-hot-toast";
import SavedAppliedJobSection from "./components/SavedAppliedJobSection";
import MarqueeDemo from "./components/magicui/MarqueeDemo";
import FindEmployerForm from "./recruiter/FindEmployerForm";
import RegisterNewEmployer from "./recruiter/RegisterNewEmployer";
import PostJob from "./recruiter/PostJob";
import RecruiterDashboard from "./components/RecruiterDashboard";
import EditJob from "./components/EditJob";
import RecruiterPersonalDetails from "./recruiter/RecruiterPersonalDetails";
// import SearchPageBar from "./components/SearchPageBar";
import CompanyPage from "./components/CompanyPage";
import TrendingCompanies from "./components/TrendingCompanies";
import SearchPageBar from "./components/SearchPage";
import SearchPage from "./components/SearchPage";
import CompaniesPage from "./components/CompaniesPage";
import PostJobWithAI from "./recruiter/PostJobWithAI";
import searchService from "./services/searchService";
import ApplicationTrackingDashboard from "./components/ApplicationTrackingDashboard";
import DeveloperProfile from "./components/DeveloperProfile";

const App = () => {
  const [jobs, setJobs] = useState([]);
  const [savedJobs, setSavedJobs] = useState([]);
  const [appliedJobs, setAppliedJobs] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isInSession, setIsInSession] = useState(false);
  const [title, setTitle] = useState("Technology");
  const [searchTitle, setSearchTitle] = useState("Technology");

  const [filters, setFilters] = useState({
    specialization: "",
    experience_level: "",
    city: "",
    industry: "",
    tech_stack: [],
    salary_range: "",
  });

  const [currentPage, setCurrentPage] = useState(1);
  const [totalJobs, setTotalJobs] = useState(0);
  const pageSize = 10;

  const navigate = useNavigate();

  useEffect(() => {
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
          console.log(`${data.userinfo.name} is in session`);
          setIsInSession(true);
          fetchSavedJobs();
          fetchAppliedJobs();
        } else {
          setIsInSession(false);
        }
      } catch (error) {
        console.error("Error checking session:", error);
      }
    };

    checkSession();
  }, []);

  const handleSave = async (jobId) => {
    try {
      if (!isInSession) {
        toast.error("Sign in first to save a job.");
      } 
      else {
        const response = await fetch(`/api/bookmark_job`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({ jobid: jobId }),
        });
        const result = await response.json();
        toast.success(result.message);
      }
    } catch (error) {
      console.error("Error saving job:", error);
      toast.error("Failed to save job.");
    }
  };

  const handleApply = async (jobId) => {
    try {

      if (!isInSession) {
        toast.error("Sign in first to apply.");
      }       
      else {
        const response = await fetch(`/api/apply_to_job`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({ jobid: jobId }),
        });
        
        const result = await response.json();
        toast.success("Boom!");
        navigate(`/job_post/${jobId}`);
      }
      
    } catch (error) {
      console.error("Error applying to job:", error);
      toast.error("Failed to apply to job.");
    }
  };

  const handleView = (jobId) => {
    navigate(`/job_post/${jobId}`);
  };


  const handleSearch = async (event) => {
    setSearchQuery(event.target.value);
    const title = `${event.target.value} Roles`;
    setTitle(title);
    setSearchTitle(event.target.value || "Technology");
    
    if (event.target.value.trim() === "") {
      console.log("fetchJobs called");
      fetchJobs();
    } else {
      console.log("Calling Instant Search Jobs");
      const data = await searchService.instantSearchJobs(event.target.value);
      setJobs(data.results);
      console.log(data);
      setJobs(data.results);
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFilters({
      ...filters,
      [name]: value,
    });
  };

  const fetchJobs = async (page = 1, pageSize = 12) => {
    try {
      const response = await fetch(
        `/api/alljobs?page=${page}&page_size=${pageSize}`,
        {
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log(data)
      setJobs(data.jobs);
      console.log(data.jobs)
      setTotalJobs(data.total_jobs);
      setCurrentPage(page);
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  // Group jobs by specialization
  const groupedJobs = jobs.reduce((acc, job) => {
    const specialization = job.specialization || "Other";
    if (!acc[specialization]) {
      acc[specialization] = [];
    }
    acc[specialization].push(job);
    return acc;
  }, {});

  const location = useLocation();

  //   We added a new useEffect hook that listens for changes in the URL (using useLocation).
// When the URL changes and contains a 'specialization' query parameter, we update the filters state with this specialization.
// We added another useEffect hook that triggers handleFilterSearch whenever filters.specialization changes.
// We updated handleFilterSearch to set the title based on the current specialization.
// We ensured that handleFilterSearch updates both the jobs state and the totalJobs state with the results from the API call.
  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const specialization = searchParams.get('specialization');
    if (specialization) {
      setFilters(prevFilters => ({
        ...prevFilters,
        specialization: specialization
      }));
    }
  }, [location]);

  useEffect(() => {
    if (filters.specialization) {
      handleFilterSearch();
    }
  }, [filters.specialization]);

  const handleFilterSearch = async () => {
    const data = await searchService.filteredSearchJobs(filters);
    setJobs(data.results);
    setTotalJobs(data.total);
    setTitle(`${filters.specialization || 'All'} Roles`);
  };


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
    fetchJobs(newPage, pageSize);
  };

  return (
    <div
      className="bg-slate-40 p-6"
      style={{ fontFamily: "Roobert-Regular, sans-serif" }}
    >
      <Toaster />
      <Navbar />
      <Routes>
        <Route
          exact
          path="/"
          element={
            <>
              <Header />
              <TrendingCompanies />
              <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-1 gap-7">
                <div className="col-span-2">
                  {Object.entries(groupedJobs).map(([specialization, jobsList]) => (
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
                    />
                  ))}
                </div>
                {/* <SignupForm /> */}
              </div>
              <BottomContainer />
            </>
          }
        />
        <Route
          path="/search-page"
          element={
            <SearchPage
              title={`${searchTitle}` }
              jobs={jobs}
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
          path="/companies"
          element={
            <CompaniesPage
              title={`${searchTitle}` }
              jobs={jobs}
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
          path="/dashboard"
          element={<ApplicationTrackingDashboard />}
        />
        <Route
          path="/job_post/:jobId"
          element={<JobPost onSave={handleSave} onApply={handleApply} />}
        />
        <Route
          path="/profile"
          element={<DeveloperProfile />}
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
        <Route
          path="/saved-jobs"
          element={
            <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-7">
              <div className="col-span-2">
                <SavedAppliedJobSection
                  title="Saved Jobs"
                  onSave={handleSave}
                  jobs={savedJobs}
                  onApply={handleApply}
                  onView={handleView}
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
                  onSave={handleSave}
                  jobs={appliedJobs}
                  onApply={handleApply}
                  onView={handleView}
                />
              </div>
            </div>
          }
        />
        <Route path="/recruiter-dashboard" element={<RecruiterDashboard />} />
        <Route path="/edit-job/:jobId" element={<EditJob />} />
        <Route path="/employer/post-job" element={<PostJob />} />
        <Route path="/employer/post-job-ai" element={<PostJobWithAI />} />
        <Route
          path="/employer/add-details"
          element={<RecruiterPersonalDetails />}
        />
        <Route
          path="/employer/organization-details"
          element={<RegisterNewEmployer />}
        />
        <Route
          path="/employer/new/organization-details"
          element={<FindEmployerForm />}
        />
      </Routes>
      <Footer />
    </div>
  );
};

export default App;