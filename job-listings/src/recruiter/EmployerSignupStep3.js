import React from "react";

const EmployerSignupStep3 = () => {
  return (
    <div className="flex justify-center items-center p-20 bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md border border-green-400">
        <h1 className="text-2xl font-bold mb-4">New employer details</h1>
        <form>
          <div className="mb-4">
            <label htmlFor="employerName" className="block text-gray-700">
              Employer name
            </label>
            <input
              type="text"
              id="employerName"
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="employerWebsite" className="block text-gray-700">
              Employer website
            </label>
            <input
              type="url"
              id="employerWebsite"
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="country" className="block text-gray-700">
              Country
            </label>
            <select
              id="country"
              className="w-full p-2 border border-gray-300 rounded"
            >
              <option>Select your country</option>
              <option>Australia</option>
              <option>New Zealand</option>
              {/* Add more options as needed */}
            </select>
          </div>
          <div className="mb-4">
            <label htmlFor="employerSize" className="block text-gray-700">
              Employer size
            </label>
            <input
              type="text"
              id="employerSize"
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="employerAddress" className="block text-gray-700">
              Employer address
            </label>
            <input
              type="text"
              id="employerAddress"
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="employerDescription"
              className="block text-gray-700"
            >
              Employer description
            </label>
            <textarea
              id="employerDescription"
              className="w-full p-2 border border-gray-300 rounded"
              minLength="150"
            ></textarea>
          </div>
          <div className="mb-4">
            <label htmlFor="logo" className="block text-gray-700">
              Add a logo
            </label>
            <input
              type="file"
              id="logo"
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-lime-500 text-white py-2 border border-lime-600 rounded hover:bg-green-700"
          >
            Complete Registration
          </button>
        </form>
      </div>
    </div>
  );
};

export default EmployerSignupStep3;
