import React, { useState, useEffect } from "react";
import Logo from "./Logo";
import { Link } from "react-router-dom";

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState("");
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  /* NOTE: Is it a good idea for this request to run each time the component mounts or we enter home page? */
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
          setIsLoggedIn(true);
          setUserName(data.userinfo.name);
        } else {
          setIsLoggedIn(false);
          setUserName("");
        }
      } catch (error) {
        console.error("Error checking session:", error);
      }
    };

    checkSession();
  }, []);

  /* NOTE: Seemingly getting CORS issues when using this, but managing to logout correctly by just setting
  window.location.href = "http://127.0.0.1:4040/logout") */
  const handleLogout = async () => {
    await fetch("http://127.0.0.1:4040/logout", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });
    setIsLoggedIn(false);
    setUserName("");
    window.location.href = "http://localhost:3000/";
  };

  const navbarStyles = {
    position: "sticky",
    top: 0,
    zIndex: 10,
  };

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
        <Logo
          className="h-24 w-auto"
          alt="Logo"
          onClick={() => (window.location.href = "http://localhost:3000/")}
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
            href="#"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            Remote
          </a>
          <a
            href="#"
            className="text-gray-600 hover:text-gray-800 hover:underline"
          >
            For companies
          </a>
        </div>
      </div>
      <div className="flex items-center space-x-4">
        {isLoggedIn ? (
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
                  <Link
                    to="/followed-employers"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    role="menuitem"
                  >
                    Followed Employers
                  </Link>
                  <Link
                    to="/job-alerts"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    role="menuitem"
                  >
                    Job Alerts
                  </Link>
                  <Link
                    to="/calendar"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    role="menuitem"
                  >
                    Calendar
                  </Link>
                  <Link
                    to="/settings"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    role="menuitem"
                  >
                    Settings
                  </Link>
                  <button
                    // onClick={handleLogout}
                    onClick={() =>
                      (window.location.href = "http://127.0.0.1:4040/logout")
                    }
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
              onClick={() =>
                (window.location.href = "http://127.0.0.1:4040/login/seeker")
              }
            >
              Log In
            </button>
            <button
              className="px-4 py-2 text-white bg-black rounded-md hover:bg-violet-400"
              onClick={() =>
                (window.location.href = "http://127.0.0.1:4040/login/seeker")
              }
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