import { useState } from "react";
import { register } from "../api/auth";
import FormContainer from "../components/FormContainer";
import AuthForm from "../components/AuthForm";
import AuthButton from "../components/AuthButton";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [msg, setMsg] = useState("");
  const navigate = useNavigate()
  const handleChange = (name: string, value: string) => {
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMsg("");
    try {
      const res = await register(form.username, form.email, form.password);
      toast.success(`User ${res.username} registered!`);
      navigate("/chats");
    } catch (err: any) {
      // Extract proper message
      const detail = err.response?.data?.detail;
      let message = "Registration failed";

      if (Array.isArray(detail)) {
        // Join all Pydantic validation messages
        message = detail.map((e: any) => e.msg).join(", ");
      } else if (typeof detail === "string") {
        message = detail;
      }

      toast.error(message);
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
      name: "email",
      label: "Email",
      type: "email",
      value: form.email,
      placeholder: "Enter email",
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
    <FormContainer title="Register">
      <AuthForm fields={fields} onChange={handleChange} onSubmit={handleSubmit}>
        <AuthButton label="Register" />
      </AuthForm>

      {msg && <div className="text-green mt-10">{msg}</div>}
    </FormContainer>
  );
}
