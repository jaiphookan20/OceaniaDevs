import styles from "../SignupForm.module.css";
import SideBar from "./SideBar";

const SignupForm = () => {
  return (
    <div>
      <SideBar />
      <div className={`${styles.ctHomeBox} ${styles.ctHomeBoxNl}`}>
        <div className="text-left">
          <h2 className="text-xl font-bold mb-4">
            Stay in the loop: Get your dose of frontend twice a week
          </h2>
          <p className="mb-4">
            👾 <strong>Hey! Looking for the latest in frontend?</strong> Twice a
            week, we'll deliver the freshest frontend news, website inspo, cool
            code demos, videos and UI animations right to your inbox.
          </p>
          <p className="mb-6">
            <strong>Zero fluff, all quality,</strong> to make your Mondays and
            Thursdays more creative!
          </p>
          <form className="flex flex-col space-y-3">
            <input
              type="email"
              placeholder="Your email"
              className="px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
            <button className="px-4 py-2 text-white bg-black rounded-md shadow-md hover:bg-gray-800">
              Subscribe
            </button>
          </form>
          <a href="#" className="mt-3 inline-block text-indigo-600">
            Find out more →
          </a>
        </div>
      </div>
    </div>
  );
};

export default SignupForm;
