import { useState } from "react";
import { login } from "../api/auth";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import FormContainer from "../components/FormContainer";
import AuthForm from "../components/AuthForm";
import AuthButton from "../components/AuthButton";
import toast from "react-hot-toast";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [msg, setMsg] = useState("");
  const { setToken, setUsername } = useAuth();
  const navigate = useNavigate();


  const handleChange = (name: string, value: string) => {
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMsg("");
    try {
      const res = await login(form.username, form.password);
      setToken(res.access_token);

      setToken(res.access_token);
      setUsername(form.username);

      localStorage.setItem("token", res.access_token);
      localStorage.setItem("username", form.username);
      toast.success("Login successful");
      navigate("/chats");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Login failed");
    }
  };

  const fields = [
    {
      name: "username",
      label: "Username",
      type: "text",
      value: form.username,
      placeholder: "Enter username",
    },
    {
      name: "password",
      label: "Password",
      type: "password",
      value: form.password,
      placeholder: "Enter password",
    },
  ];

  return (
    <FormContainer title="Login">
      <AuthForm fields={fields} onChange={handleChange} onSubmit={handleSubmit}>
        <AuthButton label="Login" />
      </AuthForm>

      {msg && <div className="text-green mt-10">{msg}</div>}
    </FormContainer>
  );
}
