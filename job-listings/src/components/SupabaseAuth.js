// src/components/SupabaseAuth.js
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import supabase from "../SupabaseClient";

const SupabaseAuth = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleOAuthSignIn = async () => {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: "google",
        // options: {
        //   redirectTo: window.location.origin + "/callback",
        // },
      });
      if (error) console.error("OAuth Sign-In Error:", error.message);
    };

    handleOAuthSignIn();
  }, [navigate]);

  return <div>Loading...</div>;
};

export default SupabaseAuth;
