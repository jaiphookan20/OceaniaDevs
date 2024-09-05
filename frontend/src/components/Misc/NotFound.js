// Navbar.js
import React from "react";

const NotFound = () => {
  // const apiUrl = "http://localhost:4040"; // This should point to your backend service in Docker
  const apiUrl = "http://localhost/api"; // Updated to work with Nginx reverse proxy

  return (
    <div>
      <h2>404 Error. This Page does not exist</h2>
    </div>
  );
};

export default NotFound;
