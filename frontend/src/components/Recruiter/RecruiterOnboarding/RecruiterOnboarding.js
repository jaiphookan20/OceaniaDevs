import React, { useState, useEffect } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import RecruiterPersonalDetails from './RecruiterPersonalDetails';
import FindEmployerForm from './FindEmployerForm';
import RegisterNewEmployer from './RegisterNewEmployer';
import RecruiterNavbarOnboarding from './RecruiterNavbarOnboarding';

const RecruiterOnboarding = () => {
  const [step, setStep] = useState(1);
  const [completedSteps, setCompletedSteps] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const handleBeforeUnload = (event) => {
      event.preventDefault();
      event.returnValue = '';
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  const handleStepComplete = () => {
    setStep(prevStep => {
      const newStep = prevStep + 1;
      setCompletedSteps(prev => [...prev, prevStep]);
      if (newStep > 3) {
        // All steps completed, redirect to dashboard
        navigate('/recruiter-dashboard');
      }
      return newStep;
    });
  };

  const goToCreateEmployer = () => {
    setStep(3);
    setCompletedSteps([1, 2]);
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return <RecruiterPersonalDetails onComplete={handleStepComplete} />;
      case 2:
        return <FindEmployerForm onComplete={handleStepComplete} />;
      case 3:
        return <RegisterNewEmployer onComplete={handleStepComplete} />;
      default:
        return null;
    }
  };

  const handleNavigateAway = () => {
    const confirmNavigation = window.confirm(
      "Are you sure you want to leave? Your onboarding process will not be complete if you navigate away."
    );
    if (confirmNavigation) {
      navigate('/');
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      {/* <RecruiterNavbarOnboarding onNavigateAway={handleNavigateAway} /> */}
      <div className="flex-grow flex flex-col items-center justify-start pt-10" >
        <div className="w-full max-w-4xl px-4">
          <h1 className="text-4xl font-semibold text-slate-600 mb-8 text-center">Recruiter Onboarding</h1>
          {/* <div className="bg-white shadow-lg rounded-lg p-8 mb-8">
            <div className="flex justify-between items-center mb-8">
              {[1, 2, 3].map((stepNumber) => (
                <div key={stepNumber} className="flex flex-col items-center">
                  <div
                    className={`w-12 h-12 rounded-full flex items-center justify-center text-lg font-semibold ${
                      completedSteps.includes(stepNumber) || step === stepNumber
                        ? 'bg-green-500 text-white'
                        : 'bg-gray-200 text-gray-600'
                    }`}
                  >
                    {stepNumber}
                  </div>
                  <div className="mt-2 text-md font-medium text-gray-600">
                    {stepNumber === 1 ? 'Personal Details' : stepNumber === 2 ? 'Find Employer' : 'Register Employer'}
                  </div>
                </div>
              ))}
            </div>
            <div className="relative mb-8">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${((step - 1) / 3) * 100}%` }}
                ></div>
              </div>
            </div>
          </div> */}
          <div className="bg-white shadow-lg rounded-lg p-8">
            {renderStep()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecruiterOnboarding;