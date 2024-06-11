import React from "react";
import Logo from "./Logo";

const Footer = () => {
  return (
    <footer className="bg-grey-300 py-10 px-4">
      <div className="container mx-auto">
        <div className="flex flex-wrap justify-between mb-8">
          <div className="w-1/2 md:w-1/4 mb-4">
            <h6 className="font-semibold mb-4">About</h6>
            <ul>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  About
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Contact
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Blog
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Story
                </a>
              </li>
            </ul>
          </div>
          <div className="w-1/2 md:w-1/4 mb-4">
            <h6 className="font-semibold mb-4">Company</h6>
            <ul>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Product
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Press
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  More
                </a>
              </li>
            </ul>
          </div>
          <div className="w-1/2 md:w-1/4 mb-4">
            <h6 className="font-semibold mb-4">Press</h6>
            <ul>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Press
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Careers
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Newsletters
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  More
                </a>
              </li>
            </ul>
          </div>
          <div className="w-1/2 md:w-1/4 mb-4">
            <h6 className="font-semibold mb-4">Press</h6>
            <ul>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Press
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Careers
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  Newsletters
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-600 hover:text-gray-800">
                  More
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="flex items-center justify-between border-t pt-6">
          <div className="flex items-center">
            {/* <img
              src="https://via.placeholder.com/40"
              alt="Magic UI"
              className="mr-3"
            /> */}
            <Logo />
            <div>
              <h6 className="font-semibold">OceaniaDevs</h6>
              <p className="text-gray-600">
                The Technologist's Job Platform of Choice.
              </p>
            </div>
          </div>
          <div className="flex space-x-6">
            <a href="#" className="text-gray-600 hover:text-gray-800">
              <i className="fab fa-linkedin"></i>
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-800">
              <i className="fab fa-instagram"></i>
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-800">
              <i className="fab fa-twitter"></i>
            </a>
          </div>
          <div>
            <p className="text-gray-600">All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
