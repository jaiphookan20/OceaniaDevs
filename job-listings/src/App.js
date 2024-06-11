import React, { useState, useEffect } from "react";
import Navbar from "./Navbar";
import Header from "./components/Header";
import JobSection from "./components/JobSection";
import SignupForm from "./components/SignupForm";
import BottomContainer from "./components/BottomContainer";
import Footer from "./components/Footer";
import SearchBar from "./components/SearchBar";
import CategoryGrid from "./components/CategoryGrid";
// import MarqueeDemo from "./components/magicui/MarqueeDemo";
import { toast } from "react-hot-toast";

const App = () => {
  const [jobs, setJobs] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isInSession, setisInSession] = useState(false);
  const [title, SetTitle] = useState("Technology Jobs");

  const [filters, setFilters] = useState({
    specialization: "",
    experience_level: "",
    city: "",
    industry: "",
    tech_stack: "",
    salary_range: "",
  });

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
      if (isInSession === false) {
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
        body: JSON.stringify({ jobid: jobId }),
      });
      const result = await response.json();
      toast.success("Redirecting");
      window.location.href = `http://127.0.0.1:4040/job_post/${jobId}`;
    } catch (error) {
      if (isInSession === false) {
        toast.error("Sign in first to apply.");
      } else {
        console.error("Error applying to job:", error);
        toast.error("Failed to apply to job.");
      }
    }
  };

  const handleView = (jobId) => {
    window.location.href = `http://127.0.0.1:4040/job_post/${jobId}`;
  };

  const handleSearch = async (event) => {
    setSearchQuery(event.target.value);
    const title = `${event.target.value} Roles`;
    SetTitle(title);
    if (event.target.value.trim() === "") {
      fetchJobs();
    } else {
      const response = await fetch(
        `http://127.0.0.1:4040/instant_search_jobs?query=${event.target.value}`,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
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
      setJobs(data);
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  return (
    <div
      className="bg-slate-40 p-6"
      style={{ fontFamily: "Roobert-Regular, sans-serif" }}
    >
      <Navbar />
      <Header />
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
          />
        </div>
        <SignupForm />
      </div>
      <div className="mt-12">
        <BottomContainer />
        <Footer />
      </div>
    </div>
  );
};

export default App;
