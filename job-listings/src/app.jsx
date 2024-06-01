import React from "react";

const jobsData = [
  {
    title: "Staff Software Engineer (Backend)",
    company: "Fora",
    location: "United States",
    salary: "$200k – $230k",
    date: "5 days ago",
    logo: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQNq25SGwUGZGM72wsSTmoBtUK92v50s_sYQ&s",
    new: true,
  },
  {
    title: "Senior Software Engineer, Networking (Python), Restaurants",
    company: "SoundHound",
    location: "Santa Clara",
    salary: "$182k – $193k",
    date: "1 week ago",
    logo: "https://upload.wikimedia.org/wikipedia/en/archive/9/9f/20171204173437%21Xero_software_logo.svg",
    new: true,
  },
  {
    title: "Senior Software Engineer - Domain Services",
    company: "Fastly",
    location: "New York City",
    salary: "$168k – $210k",
    date: "1 week ago",
    logo: "https://builtin.com/sites/www.builtin.com/files/2021-11/CIRCLE%20LOGO%20-%20GRADIENT%20-%20RGB_0.png",
    new: true,
  },
  {
    title: "Growth Engineer - Analyst",
    company: "SingleStore",
    location: "San Francisco",
    salary: "$120k – $145k",
    date: "2 weeks ago",
    logo: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRiQFvSQMZ4Bj8nt60XrWJWW1moOiYmrJ7DRA&s",
  },
  {
    title: "Senior IT Engineer",
    company: "Wunderkind (formerly BounceX)",
    location: "New York",
    salary: "$68k – $80k",
    date: "2 weeks ago",
    logo: "https://seeklogo.com/images/C/culture-amp-logo-F3EE0956BD-seeklogo.com.png",
  },
];

const productJobsData = [
  {
    title: "Associate Product Manager – Broker Research",
    company: "AlphaSense",
    location: "New York City",
    salary: "$101k – $126k",
    date: "yesterday",
    logo: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQNq25SGwUGZGM72wsSTmoBtUK92v50s_sYQ&s",
  },
  {
    title: "Principal Technical Product Manager",
    company: "LivePerson",
    location: "United States",
    salary: "$150k – $180k",
    date: "yesterday",
    logo: "https://upload.wikimedia.org/wikipedia/en/archive/9/9f/20171204173437%21Xero_software_logo.svg",
  },
  {
    title: "Staff Product Manager",
    company: "The RealReal",
    location: "San Francisco",
    salary: "$164k – $190k",
    date: "yesterday",
    logo: "https://builtin.com/sites/www.builtin.com/files/2021-11/CIRCLE%20LOGO%20-%20GRADIENT%20-%20RGB_0.png",
  },
  {
    title: "Senior Product Manager",
    company: "Vistar Media",
    location: "New York",
    salary: "$150k – $170k",
    date: "1 day ago",
    logo: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRiQFvSQMZ4Bj8nt60XrWJWW1moOiYmrJ7DRA&s",
  },
];

const JobCard = ({ job }) => {
  return (
    <div className="flex items-center justify-between p-4 border-b border-gray-200">
      <div className="flex items-center">
        <img src={job.logo} alt={job.company} className="w-12 h-12 mr-4" />
        <div>
          <h3 className="font-bold text-lg flex items-center">
            {job.title}
            {job.new && (
              <img
                src="https://remoteok.com/assets/new2x.gif"
                alt="New"
                className="w-8 h-6 ml-3"
              />
            )}
          </h3>
          <p className="text-gray-600">
            {job.company} • {job.location} • {job.salary} • {job.date}
          </p>
        </div>
      </div>
      <div className="flex space-x-2">
        <button className="px-4 py-2 border border-gray-300 rounded-md">
          Save
        </button>
        <button className="px-4 py-2 bg-lime-300 text-white rounded-md">
          Apply
        </button>
      </div>
    </div>
  );
};

const JobSection = ({ title, jobs }) => {
  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-indigo-600">{title}</h2>
        <a href="#" className="text-indigo-600">
          View all {title.toLowerCase()}
        </a>
      </div>
      <div className="bg-white rounded-lg shadow-md">
        {jobs.map((job, index) => (
          <JobCard key={index} job={job} />
        ))}
      </div>
    </div>
  );
};

const SignupForm = () => {
  return (
    <div className="max-w-sm p-6 h-1/2 bg-violet-100 rounded-lg shadow-lg">
      <div className="text-left">
        <h2 className="text-xl font-bold mb-4">
          Stay in the loop: Get your dose of frontend twice a week
        </h2>
        <p className="mb-4">
          👾 <strong>Hey! Looking for the latest in frontend?</strong> Twice a
          week, we'll deliver the freshest frontend news, website inspo, cool
          code demos, videos and UI animations right to your inbox.
        </p>
        <p className="mb-6">
          <strong>Zero fluff, all quality,</strong> to make your Mondays and
          Thursdays more creative!
        </p>
        <form className="flex flex-col space-y-3">
          <input
            type="email"
            placeholder="Your email"
            className="px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400"
          />
          <button className="px-4 py-2 text-white bg-black rounded-md shadow-md hover:bg-gray-800">
            Subscribe
          </button>
        </form>
        <a href="#" className="mt-3 inline-block text-indigo-600">
          Find out more →
        </a>
      </div>
    </div>
  );
};

const App = () => {
  return (
    <div
      className="bg-slate-50 p-6"
      style={{ fontFamily: "HeyWow, sans-serif" }}
    >
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="col-span-2">
          <JobSection title="Engineering jobs" jobs={jobsData} />
          <div className="mt-8">
            <JobSection title="Product jobs" jobs={productJobsData} />
          </div>
        </div>
        <SignupForm />
      </div>
    </div>
  );
};

export default App;
