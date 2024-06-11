import React from "react";

const JobListing = () => {
  return (
    <div className="max-w-7xl mx-auto bg-white shadow-lg rounded-lg flex border-t">
      {/* Main Content Section */}
      <div className="w-full">
        <header className="flex justify-between pb-4 mb-4 ">
          <div className="flex items-center">
            <img
              src="https://buildkite.com/_next/static/assets/assets/images/brand-assets/buildkite-logo-portrait-on-light-f7f1af58.png"
              alt="logo"
              className="p-6 max-w-32"
            />
          </div>
          <div className="flex mt-4 space-x-4">
            <div className=" p-2 rounded-md flex items-center space-x-2">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png"
                alt="JavaScript"
                className="w-16 h-16"
              />
            </div>
            <div className=" p-2 rounded-md flex items-center space-x-2">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg"
                alt="Python"
                className="w-16 h-16"
              />
            </div>
            <div className=" p-2 rounded-md flex items-center space-x-2">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/6/61/HTML5_logo_and_wordmark.svg"
                alt="HTML5"
                className="w-16 h-16"
              />
            </div>
            <div className=" p-2 rounded-md flex items-center space-x-2">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/d/d5/CSS3_logo_and_wordmark.svg"
                alt="CSS3"
                className="w-16 h-16"
              />
            </div>
          </div>
        </header>
        <div className="ml-4">
          <h1 className="text-5xl font-bold">Senior Product Manager</h1>
          <p className="text-gray-500 mt-4 text-xl">
            Mezmo, formerly LogDNA, is a comprehensive platform that makes
            observability data consumable and actionable.
          </p>
          <div className="flex justify-between mt-2 p-4">
            <div className="flex items-center space-x-2">
              {/* <FontAwesomeIcon icon={faBuilding} /> */}
              <img
                width="36"
                height="36"
                // src="https://img.icons8.com/?size=100&id=yhAssOTULtI7&format=png&color=000000"
                src="https://img.icons8.com/?size=100&id=Z3STIRU4hxMn&format=png&color=000000"
                alt="new"
              />
              <p className="text-gray-500">Mezmo</p>
            </div>
            <div className="flex items-center space-x-2">
              {/* <FontAwesomeIcon icon={faUsers} /> */}
              <img
                width="36"
                height="36"
                // src="https://img.icons8.com/?size=100&id=INggyhkrV8C4&format=png&color=000000"
                src="https://img.icons8.com/?size=100&id=3BUZy0U5CdQL&format=png&color=000000"
                alt="new"
              />
              <p className="text-gray-500">Experience</p>
            </div>
            <div className="flex items-center space-x-2">
              {/* <FontAwesomeIcon icon={faDollarSign} /> */}
              <img
                width="36"
                height="36"
                // src="https://img.icons8.com/?size=100&id=emIu3CT0zYjk&format=png&color=000000"
                src="https://img.icons8.com/?size=100&id=tUxN1SSkN8zG&format=png&color=000000"
                alt="new"
              />
              <p className="text-gray-500">160k-200k USD</p>
            </div>
            <div className="flex items-center space-x-2">
              {/* <FontAwesomeIcon icon={faGlobeAmericas} /> */}
              <img
                width="36"
                height="36"
                // src="https://img.icons8.com/?size=100&id=kSFAST6TliFQ&format=png&color=000000"
                src="https://img.icons8.com/?size=100&id=HvkLiNNdKM33&format=png&color=000000"
                alt="new"
              />
              <p className="text-gray-500 ">United States only</p>
            </div>
          </div>
        </div>
        <div className="flex justify-between items-between pb-20">
          <div className="w-2/3 pl-8 pr-2">
            <section className="mt-6">
              <h2 className="text-2xl font-semibold">About the role</h2>
              <p className="mt-2 text-gray-700">
                At <span className="text-blue-500">Mezmo</span>, our Senior
                Product Managers play a crucial role in shaping the Product
                experience and strategy for our Pipeline Telemetry platform. As
                a valued member of a growing, innovative team, you will work to
                enable organizations to Understand, Optimize and Respond to
                their telemetry data in a cost effective and efficient manner
                saving both money and precious time.
              </p>
              <p className="mt-2 text-gray-700">
                As a Senior Product Manager at{" "}
                <span className="text-blue-500">Mezmo</span>, you will play a
                crucial role in shaping the product experience and strategy for{" "}
                <span className="text-blue-500">Mezmo’s</span> pipeline
                telemetry platform, a growing market with huge opportunity! As a
                valued member of a growing, innovative team, you will work to
                enable organizations to Understand, Optimize and Respond to
                their telemetry data in a cost effective and efficient manner
                saving both money and precious time.
              </p>
            </section>
            <section className="mt-6">
              <h2 className="text-2xl font-semibold">Responsibilities:</h2>
              <ul className="mt-2 text-gray-700 list-disc list-inside">
                <li>
                  Guide the product roadmap by understanding core customer and
                  business challenges, identifying the best solution and
                  balancing priorities between near term needs and long term
                  vision.
                </li>
                <li>
                  Work closely with Marketing and the GTM team taking new
                  offerings to market and validating them including
                  functionality, pricing and packaging, ensuring smooth adoption
                  and penetration.
                </li>
                <li>
                  Partner with Design and Product Marketing teams to create go
                  to market strategy, positioning and messaging for new products
                  and features.
                </li>
                <li>
                  Guide the product roadmap by understanding core customer and
                  business challenges, identifying the best solution and
                  balancing priorities between near term needs and long term
                  vision.
                </li>
                <li>
                  Work closely with Marketing and the GTM team taking new
                  offerings to market and validating them including
                  functionality, pricing and packaging, ensuring smooth adoption
                  and penetration.
                </li>
                <li>
                  Partner with Design and Product Marketing teams to create go
                  to market strategy, positioning and messaging for new products
                  and features.
                </li>
              </ul>
            </section>
          </div>
          {/* Side Column Section */}
          <div className="w-1/4 p-4">
            <div className="border rounded-md p-4 mb-6">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold">Apply now</h3>
                {/* <span className="text-purple-600">Job expired?</span> */}
              </div>
              <p className="mt-2 text-gray-700">
                {/* Please let Mezmo know you found this job on Himalayas. This
                helps us grow! */}
              </p>
              <button className="w-full mt-4 bg-[#c3f53c] text-black border px-4 py-2 rounded-md">
                Apply now
              </button>
              <button className="w-full mt-4 bg-black text-white px-4 py-2 rounded-md">
                Bookmark Job
              </button>
            </div>
            {/* <div className="border rounded-md p-4 mb-6">
              <h3 className="text-lg font-semibold">
                Elevate your application
              </h3>
              <p className="mt-2 text-gray-700">
                Let our AI craft your perfect cover letter and align your resume
                to this job's criteria.
              </p>
              <button className="w-full mt-4 bg-purple-600 text-white px-4 py-2 rounded-md">
                Optimize my resume
              </button>
              <button className="w-full mt-4 bg-purple-200 text-purple-600 px-4 py-2 rounded-md">
                Craft my cover letter
              </button>
              <p className="mt-2 text-gray-600 text-sm">
                By using our AI tools, you consent to sharing your profile with
                our AI partner for this purpose.
              </p>
            </div> */}
            <div className="border p-4 ">
              <h3 className="text-lg font-semibold">About the job</h3>
              <p className="mt-2 text-gray-700">
                <strong>Apply before:</strong> Aug 10, 2024
              </p>
              <p className="text-gray-700">
                <strong>Posted on:</strong> Jun 11, 2024
              </p>
              <p className="text-gray-700">
                <strong>Job type:</strong> Full Time
              </p>
              <p className="text-gray-700">
                <strong>Experience level:</strong> Senior
              </p>
              <p className="text-gray-700">
                <strong>Salary:</strong> 160k-200k USD
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobListing;
