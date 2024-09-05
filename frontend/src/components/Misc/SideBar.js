import React from "react";
import styles from "../SignupForm.module.css";

const SideBar = () => {
  return (
    <div
      className={`${styles.ctSideBar} ${styles.ctHomeBoxNl}`}
      style={{ fontFamily: "HeyWow, sans-serif" }}
    >
      <h2 className="text-2xl text-white font-bold mb-6">
        Level up your job search
      </h2>
      <ul className="space-y-4 ml-2">
        <li className="flex items-center">
          {/* <FcOk className="mr-4" /> */}
          <img
            width="50"
            height="50"
            src="https://img.icons8.com/isometric/50/new.png"
            alt="new"
          />
          <span className="text-md font-bold text-white ml-4 ml-4">
            Unique jobs in niche industries
          </span>
        </li>
        <li className="flex items-center">
          {/* <FcPortraitMode className="mr-4 text-2xl" /> */}
          <img
            width="50"
            height="50"
            src="https://img.icons8.com/isometric/50/panorama--v1.png"
            alt="panorama--v1"
          />
          <span className="text-md font-bold text-white ml-4">
            Set salary & equity upfront
          </span>
        </li>
        <li className="flex items-center">
          {/* <FcBullish className="mr-4 text-2xl" /> */}
          <img
            width="50"
            height="50"
            src="https://img.icons8.com/isometric/50/pizza.png"
            alt="pizza"
          />
          <span className="text-md font-bold text-white ml-4">
            Personalized job filters
          </span>
        </li>
        <li className="flex items-center">
          {/* <FcBinoculars className="mr-4 text-xl" /> */}
          <img
            width="50"
            height="50"
            src="https://img.icons8.com/isometric/50/banknotes--v1.png"
            alt="banknotes--v1"
          />
          <span className="text-md font-bold text-white ml-4">
            Showcase skills beyond a resume
          </span>
        </li>
        <li className="flex items-center">
          {/* <FcConferenceCall className="mr-4 text-2xl" /> */}
          <img
            width="50"
            height="50"
            src="https://img.icons8.com/isometric/50/bank-cards.png"
            alt="bank-cards"
          />
          <span className="text-md font-bold font-bold text-white ml-4">
            Let recruiters reach out
          </span>
        </li>
      </ul>
      <button className="mt-8 px-4 py-2 border border-black rounded-md hover:bg-gray-200 bg-lime-300 text-black">
        Sign up & search
      </button>
    </div>
  );
};

export default SideBar;
