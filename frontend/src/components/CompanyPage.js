
import React, { useState } from "react";
import { Search, ChevronDown } from "lucide-react";
import JobSection from "./JobSection";
import Header from "./Header";
import SearchPageHeader from "./SearchPageHeader";
import CompanyPageHeader from "./CompanyPageHeader";
import SignupForm from "./SignupForm";
import TechStackGrid from "./TechStackGrid";

const CompanyPage = ({
  title,
  jobs,
  onSave,
  onApply,
  onView,
  currentPage,
  totalJobs,
  pageSize,
  onPageChange,
}) => {
  const [header, setHeader] = useState("Remote jobs");
  const [jobSearch, setJobSearch] = useState("");
  const [locationSearch, setLocationSearch] = useState("");

  const handleSearch = (e) => {
    e.preventDefault();
    if (jobSearch.trim()) {
      setHeader(jobSearch.trim());
    } else {
      setHeader("Remote jobs!");
    }
  };

  return (
    <>
      <div
        className="max-w-6xl mx-auto "
        style={{ fontFamily: "Roobert-Regular, sans-serif" }}
      >
        <CompanyPageHeader 
            heading="Atlassian"
            subheading="Atlassian's team collaboration software like Jira, Confluence and Trello help teams organize, discuss, and complete shared work."
        />
        <div className="flex justify-start p-2 gap-8">
            <div className="flex items-center space-x-2 bg-slate-50/50 rounded-2xl border border-slate-200 p-2">
                <img
                    width="30"
                    height="30"
                    src="https://img.icons8.com/?size=100&id=HvkLiNNdKM33&format=png&color=000000"
                    alt="location"
                />
                <p className="text-gray-500 text-1xl">Sydney, NSW</p>
            </div>
            <div className="flex items-center space-x-2 bg-slate-50/50 rounded-2xl border border-slate-200 p-2">
              <img
                width="30"
                height="30"
                src="https://img.icons8.com/?size=100&id=3BUZy0U5CdQL&format=png&color=000000"
                alt="experience"
              />
              <p className="text-gray-500">IT-Software Development</p>
            </div>
            <div className="flex items-center space-x-2 bg-slate-50/50 rounded-2xl border border-slate-200 p-2">
              <img
                width="30"
                height="30"
                src="https://img.icons8.com/?size=100&id=tUxN1SSkN8zG&format=png&color=000000"
                alt="salary"
              />
              <p className="text-gray-500">Direct</p>
            </div>
        </div>
        <TechStackGrid />
      </div>
      <div className="max-w-6xl mx-auto mt-6 grid grid-cols-1 lg:grid-cols-3 gap-12">
                <div className="col-span-2">
                  <JobSection
                    title={title}
                    jobs={jobs}
                    onSave={onSave}
                    onApply={onApply}
                    onView={onView}
                    currentPage={currentPage}
                    totalJobs={totalJobs}
                    pageSize={pageSize}
                    onPageChange={onPageChange}
                  />
                </div>
                <SignupForm />
              </div>
    </>
  );
};

export default CompanyPage;

