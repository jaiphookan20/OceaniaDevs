import React from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ session, children }) => {
  if (!session) {
    return <Navigate to="/supabase-auth" />;
  }

  return children;
};

export default ProtectedRoute;
