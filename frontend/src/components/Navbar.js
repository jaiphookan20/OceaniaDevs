import React, { useState, useEffect } from "react";
import Logo from "./Logo";
import { Link, useNavigate } from "react-router-dom";
import oceBlackLogo from "../assets/oce-black-logo.png"

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

  return (
    <nav
      className="flex justify-between items-center py-7 px-8 bg-white max-w-8xl mx-auto"
      style={navbarStyles}
    >
      <div className="flex items-center ">
        {/* <img src={oceBlackLogo}/> */}
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
            href="#"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Overview
          </a>
          <a
            href="#"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Jobs
          </a>
          <a
            href="#"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Featured
          </a>
          <a
            href="/companies"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Explore Companies
          </a>
          <a
            href="/company-page"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Company Page
          </a>
          <a
            href="/search-page"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Search Page
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
            <button
              className="px-4 py-2 text-white bg-black rounded-md hover:bg-violet-400"
              onClick={() => (window.location.href = "/login/recruiter")}
            >
              Recruiter Sign-Up
            </button>
          </>
        )}

        {isLoggedIn ? ( // Show dropdown menu if user is logged in
          <div className="relative inline-block text-left">
            <div>
              <button
                type="button"
                className="flex items-center justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50"
                id="options-menu"
                aria-haspopup="true"
                aria-expanded={isDropdownOpen}
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              >
                {userName}
                <svg
                  className="-mr-1 ml-2 h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M5.23 7.21a.75.75 0 011.06 0L10 10.92l3.71-3.71a.75.75 0 111.06 1.06l-4 4a.75.75 0 01-1.06 0l-4-4a.75.75 0 010-1.06z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
            {isDropdownOpen && (
              <div className="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                <div
                  className="py-1"
                  role="menu"
                  aria-orientation="vertical"
                  aria-labelledby="options-menu"
                >
                  <Link
                    to="/profile"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    role="menuitem"
                  >
                    My Profile
                  </Link>
                  {userType === "recruiter" ? ( // Show Add Recruiter Details link only for recruiters
                    <>
                      <Link
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
                      </Link>
                      <Link
                        to="/recruiter-dashboard"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        role="menuitem"
                      >
                        Recruiter Dashboard
                      </Link>
                    </>
                  ) : (
                    <>
                      <Link
                        to="/saved-jobs"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        role="menuitem"
                      >
                        Saved Jobs
                      </Link>
                      <Link
                        to="/applied-jobs"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        role="menuitem"
                      >
                        Applied Jobs
                      </Link>
                    </>
                  )}
                  <Link
                    to="/job-alerts"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    role="menuitem"
                  >
                    Job Alerts
                  </Link>
                  <Link
                    to="/settings"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    role="menuitem"
                  >
                    Settings
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    role="menuitem"
                  >
                    Sign out
                  </button>
                </div>
              </div>
            )}
          </div>
        ) : (
          <>
            <button
              className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-100"
              onClick={() => (window.location.href = "/login/seeker")}
            >
              Log In
            </button>
            <button
              className="px-4 py-2 text-white bg-black rounded-md hover:bg-violet-400"
              onClick={() => (window.location.href = "/login/seeker")}
            >
              Sign Up
            </button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
