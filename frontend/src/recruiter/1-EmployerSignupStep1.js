import React from "react";

const EmployerSignupStep1 = () => {
  return (
    <div className="flex justify-center items-center p-20 bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg border border-green-400">
        <h1 className="text-2xl font-bold mb-4">Sign up as an employer</h1>
        <p className="mb-4">
          Already have an account on OceaniaDevs?{" "}
          <a href="/login" className="text-green-600">
            Login
          </a>
        </p>
        <form>
          <div className="mb-4">
            <label htmlFor="email" className="block text-gray-700">
              Business Email
            </label>
            <input
              type="email"
              id="email"
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="password" className="block text-gray-700">
              Password
            </label>
            <input
              type="password"
              id="password"
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          <div className="grid grid-cols-2 mt-8 mb-4 text-sm text-gray-600">
            <p>One uppercase character</p>
            <p>One lowercase character</p>
            <p>One number</p>
            <p>One special character</p>
            <p>8 characters minimum</p>
          </div>
          <button
            type="submit"
            className="w-full bg-lime-500 text-white py-2 border border-lime-600 rounded hover:bg-green-700"
          >
            Continue
          </button>
          <p className="mt-4 text-sm text-gray-600">
            If you continue, you agree to our{" "}
            <a href="/privacy" className="text-green-600">
              Privacy Policy
            </a>
          </p>
        </form>
      </div>
    </div>
  );
};

export default EmployerSignupStep1;
