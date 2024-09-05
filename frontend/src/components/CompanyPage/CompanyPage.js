import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import CompanyPageHeader from "./CompanyPageHeader";
import CompanyPageTechStackGrid from "./CompanyPageTechStackGrid";
import CompanyJobSection from "./CompanyJobSection";
import HashLoader from "react-spinners/HashLoader";

const CompanyPage = ({ onSave, onApply, onView }) => {
  const [company, setCompany] = useState(null);
  const [jobs, setJobs] = useState([]);
  const { companyId } = useParams();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCompanyDetails = async () => {
      try {
        const response = await fetch(`/api/company/${companyId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch company details');
        }
        const data = await response.json();
        console.log(data)
        setCompany(data);
        setJobs(data.jobs);
      } catch (error) {
        console.error('Error fetching company details:', error);
      }
      finally {
        setLoading(false);
      }
  };

    fetchCompanyDetails();
  }, [companyId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <HashLoader color="#8823cf" size={120} />
      </div>
    );
  }

  return (
    <>
      <div className="max-w-6xl mx-auto" style={{ fontFamily: "Roobert-Regular, sans-serif" }}>
        <CompanyPageHeader 
          heading={company.name}
          subheading={company.description}
          logoSrc={company.logo_url}
          company={company}
        />
        <CompanyPageTechStackGrid company={company} />
        <div className="gap-12 mt-4">
        <div className="col-span-2">
          <CompanyJobSection
            title={`Jobs at ${company.name}`}
            jobs={jobs}
            company={company}
            onSave={onSave}
            onApply={onApply}
            onView={onView}
          />
        </div>
        {/* <SignupForm /> */}
      </div>
      </div>
    </>
  );
};

export default CompanyPage;
