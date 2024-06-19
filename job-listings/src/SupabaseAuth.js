// // src/pages/SupabaseAuth.js
// import { useEffect } from "react";
// import { Auth } from "@supabase/auth-ui-react";
// import { ThemeSupa } from "@supabase/auth-ui-shared";
// import supabase from "./SupabaseClient";
// import { useNavigate } from "react-router-dom";

// const SupabaseAuth = () => {
//   const navigate = useNavigate();

//   useEffect(() => {
//     const handleAuthRedirect = async () => {
//       const urlParams = new URLSearchParams(window.location.search);
//       const authCode = urlParams.get("code");

//       if (authCode) {
//         const { data, error } = await supabase.auth.exchangeCodeForSession(
//           authCode
//         );
//         if (error) {
//           console.log("ERROR");
//           console.error("Error exchanging code for session:", error);
//         } else if (data.session) {
//           const user = data.session.user;
//           console.log("RECEIVED SESSION");
//           await sendUserDataToBackend(user);
//           navigate("/");
//         }
//       }
//     };

//     handleAuthRedirect();
//   }, [navigate]);

// //   const sendUserDataToBackend = async (user) => {
// //     const data = {
// //       id: user.id,
// //       email: user.email,
// //       name: user.user_metadata.full_name,
// //       type: new URLSearchParams(window.location.search).get("type"), // assuming type is in query params
// //     };

// //     console.log("inside sendUserDataToBackend");

// //     try {
// //       const response = await fetch("http://127.0.0.1:4040/callback", {
// //         method: "POST",
// //         headers: {
// //           "Content-Type": "application/json",
// //         },
// //         credentials: "include",
// //         body: JSON.stringify(data),
// //       });

// //       if (!response.ok) {
// //         throw new Error("Failed to send user data to backend");
// //       }
// //     } catch (error) {
// //       console.error("Error sending user data to backend:", error);
// //     }
// //   };

//   return (
//     <Auth
//       supabaseClient={supabase}
//       providers={["google"]}
//       appearance={{ theme: ThemeSupa }}
//     />
//   );
// };

// export default SupabaseAuth;
