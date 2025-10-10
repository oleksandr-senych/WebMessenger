import { useState } from "react";
import { register } from "../api/auth";

export default function Register() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await register(form.username, form.email, form.password);
      setMsg(`User ${res.username} registered!`);
    } catch (err: any) {
      setMsg(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input placeholder="Username" value={form.username} onChange={e => setForm({...form, username: e.target.value})} />
      <input placeholder="Email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
      <input type="password" placeholder="Password" value={form.password} onChange={e => setForm({...form, password: e.target.value})} />
      <button type="submit">Register</button>
      <p>{msg}</p>
    </form>
  );
}