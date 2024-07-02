import React from "react";
import { Navigate, useLocation } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const location = useLocation();
  const isAuthenticated = sessionStorage.getItem("isAuthenticated") === "true";

  if (!isAuthenticated) {
    // Redirect to login page, saving the intended destination
    return (
      <Navigate to="/login/recruiter" state={{ from: location }} replace />
    );
  }

  return children;
};

export default ProtectedRoute;
