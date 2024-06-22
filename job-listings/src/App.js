import React, { useState, useEffect } from "react";
import { Route, Routes, useNavigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Header from "./components/Header";
import JobSection from "./components/JobSection";
import SignupForm from "./components/SignupForm";
import BottomContainer from "./components/BottomContainer";
import SearchBar from "./components/SearchBar";
import CategoryGrid from "./components/CategoryGrid";
import JobPost from "./JobPost";
import { toast, Toaster } from "react-hot-toast";
import SavedAppliedJobSection from "./SavedAppliedJobSection";
import MarqueeDemo from "./components/magicui/MarqueeDemo";
import EmployerSignupStep1 from "./recruiter/EmployerSignupStep1";
import EmployerSignupStep2 from "./recruiter/EmployerSignupStep2";
import EmployerSignupStep3 from "./recruiter/EmployerSignupStep3";
import FindEmployerForm from "./FindEmployerForm";

const App = () => {
  const [jobs, setJobs] = useState([]);
  const [savedJobs, setSavedJobs] = useState([]);
  const [appliedJobs, setAppliedJobs] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isInSession, setisInSession] = useState(false);
  const [title, setTitle] = useState("Technology Jobs");

  const [filters, setFilters] = useState({
    specialization: "",
    experience_level: "",
    city: "",
    industry: "",
    tech_stack: "",
    salary_range: "",
  });

  const [currentPage, setCurrentPage] = useState(1);
  const [totalJobs, setTotalJobs] = useState(0);
  const pageSize = 10;

  const navigate = useNavigate();

  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await fetch("http://127.0.0.1:4040/check-session", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        const data = await response.json();
        if (data.userinfo) {
          console.log(`${data.userinfo.name} is in session`);
          setisInSession(true);
        } else {
          setisInSession(false);
        }
      } catch (error) {
        console.error("Error checking session:", error);
      }
    };

    checkSession();
  }, []);

  const handleSave = async (jobId) => {
    try {
      const response = await fetch("http://127.0.0.1:4040/bookmark_job", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ jobid: jobId }),
      });
      const result = await response.json();
      toast.success(result.message);
    } catch (error) {
      if (!isInSession) {
        toast.error("Sign in first to save a job.");
      } else {
        console.error("Error saving job:", error);
        toast.error("Failed to save job.");
      }
    }
  };

  const handleApply = async (jobId) => {
    try {
      const response = await fetch("http://127.0.0.1:4040/apply_to_job", {
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
    } catch (error) {
      if (!isInSession) {
        toast.error("Sign in first to apply.");
      } else {
        console.error("Error applying to job:", error);
        toast.error("Failed to apply to job.");
      }
    }
  };

  const handleView = (jobId) => {
    navigate(`/job_post/${jobId}`);
  };

  const handleSearch = async (event) => {
    setSearchQuery(event.target.value);
    const title = `${event.target.value} Roles`;
    setTitle(title);
    if (event.target.value.trim() === "") {
      console.log("fetchJobs called");
      fetchJobs();
    } else {
      console.log("Calling Instant Search Jobs");
      const response = await fetch(
        `http://127.0.0.1:4040/instant_search_jobs?query=${event.target.value}`,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      console.log(data);
      setJobs(data.results);
    }
  };

  const handleFilterSearch = async () => {
    const queryParams = new URLSearchParams(filters);
    const response = await fetch(
      `http://127.0.0.1:4040/filtered_search_jobs?${queryParams.toString()}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      }
    );
    const data = await response.json();
    setJobs(data.results);
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFilters({
      ...filters,
      [name]: value,
    });
  };

  const fetchJobs = async (page = 1, pageSize = 10) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:4040/alljobs?page=${page}&page_size=${pageSize}`,
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
      setJobs(data.jobs);
      setTotalJobs(data.total_jobs);
      setCurrentPage(page);
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchSavedJobs = async () => {
    try {
      const response = await fetch("http://127.0.0.1:4040/bookmarked_jobs", {
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

  useEffect(() => {
    fetchSavedJobs();
    fetchAppliedJobs();
  }, []);

  const fetchAppliedJobs = async () => {
    try {
      const response = await fetch("http://127.0.0.1:4040/applied_jobs", {
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
              <MarqueeDemo />
              <CategoryGrid />
              <SearchBar
                searchQuery={searchQuery}
                onSearchChange={handleSearch}
                filters={filters}
                onFilterChange={handleChange}
                onFilterSearch={handleFilterSearch}
              />
              <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-7">
                <div className="col-span-2">
                  <JobSection
                    title={title}
                    jobs={jobs}
                    onSave={handleSave}
                    onApply={handleApply}
                    onView={handleView}
                    currentPage={currentPage}
                    totalJobs={totalJobs}
                    pageSize={pageSize}
                    onPageChange={handlePageChange}
                  />
                </div>
                <SignupForm />
              </div>
              <BottomContainer />
            </>
          }
        />
        <Route
          path="/job_post/:jobId"
          element={<JobPost onSave={handleSave} onApply={handleApply} />}
        />
        <Route
          path="/saved-jobs"
          element={
            <>
              {/* <h2 className="text-3xl font-bold mb-4">Saved Jobs</h2> */}
              <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-7">
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
            </>
          }
        />
        <Route
          path="/applied-jobs"
          element={
            <>
              {/* <h2 className="text-3xl font-bold mb-4">Saved Jobs</h2> */}
              <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-7">
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
            </>
          }
        />
        <Route path="/register/employer" element={<EmployerSignupStep1 />} />
        <Route
          path="/register/employer/info"
          element={<EmployerSignupStep2 />}
        />
        <Route
          path="/register/employer/organization-details"
          element={<EmployerSignupStep3 />}
        />
        <Route
          path="/register/employer/new/organization-details"
          element={<FindEmployerForm />}
        />
      </Routes>
      <Footer />
    </div>
  );
};

export default App;