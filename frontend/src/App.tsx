import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import NavButton from "./components/NavButton";

export default function App() {
  const { token } = useAuth();
  const navigate = useNavigate();

  const username = localStorage.getItem("username");

  useEffect(() => {
    // optional: if user not logged in, you can choose to redirect to login
  }, [token]);

  const handleChatsClick = () => {
    if (!token) {
      navigate("/login");
    } else {
      navigate("/chats");
    }
  };
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 text-gray-800">
      <div className="bg-white shadow-md rounded-xl p-8 max-w-md text-center border border-gray-200">
        <h1 className="text-3xl font-bold text-blue-600 mb-4">
          Welcome, {token ? username : "Guest"}!
        </h1>
        <p className="text-gray-600 mb-6">
          {token
            ? "You are logged in."
            : "Please register or log in to start chatting."}
        </p>

        <div className="flex flex-col gap-3">
          <NavButton label="Register" to="/register" />
          <NavButton label="Login" to="/login" />
          <button
            onClick={handleChatsClick}
            className="px-4 py-2 rounded-md text-white font-medium bg-blue-500 hover:bg-blue-600 focus:ring-2 focus:ring-blue-400 transition"
          >
            Chats
          </button>
        </div>
      </div>
    </div>
  );
}
