import axios from "axios";

const instance = axios.create({
  baseURL: "/api",
  withCredentials: true,
});

instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (
      error.response &&
      error.response.status === 401 &&
      error.response.data.login_required
    ) {
      // Redirect to login page
      window.location.href = "/login/recruiter";
    }
    return Promise.reject(error);
  }
);

export default instance;
