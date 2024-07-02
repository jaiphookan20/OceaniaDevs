import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

const AuthRedirect = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const destination = searchParams.get("destination");
    if (destination) {
      navigate(destination);
    } else {
      navigate("/");
    }
  }, [navigate, location]);

  return <div>Redirecting...</div>;
};

export default AuthRedirect;
