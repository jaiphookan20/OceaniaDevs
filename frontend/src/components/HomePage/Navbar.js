import React, { useState, useEffect } from "react";
import Logo from "./Logo";
import { Link, useNavigate } from "react-router-dom";
import { UserCircle, BookMarked, BookCheck, Activity, Settings, LogOut,  ChevronDown, ChevronUp } from 'lucide-react';


const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState("");
  const [userType, setUserType] = useState("");
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const navigate = useNavigate();

  /* Effect to check the session and update the state accordingly */
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
          setIsLoggedIn(true);
          setUserName(data.userinfo.name);
          setUserType(data.type);
        } else {
          setIsLoggedIn(false);
          setUserName("");
          setUserType("");
          setUserType("");
        }

      } catch (error) {
        console.error("Error checking session:", error);
      }
    };

    const getUserInfo = async () => {
      try {
        const response = await fetch(`/api/get-user-info`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        const data = await response.json();
        if (data.userinfo) {
          setIsLoggedIn(true);
          setUserName(data.userinfo.name);
          setUserType(data.type);
        } else {
          setIsLoggedIn(false);
          setUserName("");
          setUserType("");
          setUserType("");
        }

      } catch (error) {
        console.error("Error checking session:", error);
      }
    };

    checkSession();
  }, []);

  const handleLogout = async () => {
    await fetch("/logout", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });
    setIsLoggedIn(false);
    setUserName("");
    setUserType("");
    navigate("/")
  };

  const navbarStyles = {
    position: "sticky",
    top: 0,
    zIndex: 10,
  };

  /* Effect to handle clicks outside the dropdown menu */
  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (
        isDropdownOpen &&
        !event.target.closest(".relative") &&
        !event.target.closest("button")
      ) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener("click", handleOutsideClick);

    return () => {
      document.removeEventListener("click", handleOutsideClick);
    };
  }, [isDropdownOpen]);

  const getInitials = (name) => {
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase();
  };


  return (
    <nav
      className="flex justify-between items-center py-7 px-8 bg-white max-w-7xl mx-auto"
      style={navbarStyles}
    >
      <div className="flex items-center ">
        <Logo
          className="h-24 w-auto"
          alt="Logo"
          onClick={() => (window.location.href = "/")}
        />
        <div className="">
          <a
            href="#"
            className="text-gray-600 font-bold text-2xl hover:text-gray-800 mr-10"
          >
            OceaniaDevs
          </a>
        </div>
        <div className="flex justify-between items-center space-x-8">
          <a
            href="/companies"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Explore Companies
          </a>
          <a
            href="/search-page"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Search Jobs
          </a>
          {/* <a
            href="/profile"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Profile
          </a> */}
          <a
            href="/pricing"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Pricing
          </a>
        </div>
      </div>
      <div className="flex items-center space-x-4">
        {isLoggedIn && userType === "recruiter" ? (
          <>
            <button
              className="px-4 py-2 text-white bg-violet-500 border border-gray-400 shadow-sm rounded-md hover:bg-violet-800 hover:text-white"
              onClick={() => (window.location.href = "/employer/post-job")}
            >
              Post Job
            </button>
            <button
              className="px-4 py-2 text-white bg-violet-500 border border-gray-400 shadow-sm rounded-md hover:bg-violet-800 hover:text-white"
              onClick={() => (window.location.href = "/employer/post-job-ai")}
            >
              Post Job with AI
            </button>
          </>
        ) : (
          <>
            <button
              className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-100"
              onClick={() => (window.location.href = "/login/recruiter")}
            >
              Recruiter Login
            </button>
            {/* <button
              className="px-4 py-2 text-white bg-black rounded-md hover:bg-violet-400"
              onClick={() => (window.location.href = "/login/recruiter")}
            >
              Recruiter Sign-Up
            </button> */}
          </>
        )}

{isLoggedIn ? (
          <div className="relative inline-block text-left">
            <div>
              <button
                type="button"
                className="flex items-center justify-center space-x-2"
                id="options-menu"
                aria-haspopup="true"
                aria-expanded={isDropdownOpen}
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              >
                <div className="w-10 h-10 rounded-full bg-violet-700 text-white text-sm font-medium flex items-center justify-center">
                  {getInitials(userName)}
                </div>
                {isDropdownOpen ? (
                  <ChevronUp className="h-5 w-5 text-gray-500" />
                ) : (
                  <ChevronDown className="h-5 w-5 text-gray-500" />
                )}
              </button>
            </div>
            {isDropdownOpen && (
              <div className="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                <div className="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
                  <Link to="/profile" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
                    <UserCircle className="mr-3 h-5 w-5" />
                    My Profile
                  </Link>
                  {userType === "recruiter" ? (
                    <>
                      {/* <Link
                        to="/employer/add-details"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        role="menuitem"
                      >
                        Add Recruiter Details
                      </Link>
                      <Link
                        to="/employer/new/organization-details"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        role="menuitem"
                      >
                        Register Employer
                      </Link> */}
                      <Link
                        to="/recruiter-dashboard"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        role="menuitem"
                      >
                        Recruiter Dashboard
                      </Link>
                      <Link
                        to="/recruiter-settings"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        role="menuitem"
                      >
                        Settings
                      </Link>
                    </>
                  ) : (
                    <>
                    <Link to="/dashboard" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
                        <Activity className="mr-3 h-5 w-5" />
                        Application Dashboard
                      </Link>
                      <Link to="/saved-jobs" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
                        <BookMarked className="mr-3 h-5 w-5" />
                        Saved Jobs
                      </Link>
                      <Link to="/applied-jobs" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
                        <BookCheck className="mr-3 h-5 w-5" />
                        Applied Jobs
                      </Link>
                    <Link to="/job-alerts" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
                    <Activity className="mr-3 h-5 w-5" />
                    Job Alerts
                  </Link>
                  <Link to="/seeker/settings" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
                    <Settings className="mr-3 h-5 w-5" />
                    Settings
                  </Link>
                   </> 
                  )}
                  <div className="border-t border-gray-100 my-1"></div>
                  <button onClick={handleLogout} className="flex items-center w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
                    <LogOut className="mr-3 h-5 w-5" />
                    Sign out
                  </button>
                </div>
              </div>
            )}
          </div>
        ) : (
          <>
            <button
              className="px-4 py-2 text-gray-600 border border-gray-300 bg-black text-white rounded-md hover:bg-gray-100"
              onClick={() => (window.location.href = "/login/seeker")}
            >
              Log In
            </button>
            {/* <button
              className="px-4 py-2 text-white bg-black rounded-md hover:bg-violet-400"
              onClick={() => (window.location.href = "/login/seeker")}
            >
              Sign Up
            </button> */}
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
