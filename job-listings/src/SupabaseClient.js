// src/supabaseClient.js
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  "https://uyrnqtinwxwhtlaswyrf.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV5cm5xdGlud3h3aHRsYXN3eXJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg1NTQwMzcsImV4cCI6MjAzNDEzMDAzN30.IJjZWNKGU_fPofRw-LDYybPUsCaUZwUJSZ3gXSejwNM",
  {
    auth: {
      detectSessionInUrl: true,
      flowType: "pkce",
    },
  }
);

export default supabase;
