import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import { AuthProvider } from "./context/AuthContext";
import ChatsPage from "./pages/ChatsPage";
import MessagesPage from "./pages/MessagesPage";
import "./index.css";
import { Toaster } from "react-hot-toast";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AuthProvider>
      <Toaster position="top-center" reverseOrder={false} />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/chats" element={<ChatsPage />} />
          <Route path="/chats/:chatId" element={<MessagesPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
);
