import api from "./axios";

export async function register(username: string, email: string, password: string) {
  const response = await api.post("/auth/register", { username, email, password });
    // Save JWT for later use
  localStorage.setItem("token", response.data.access_token);
  localStorage.setItem("username", username);
  return response.data;

}

export async function login(username: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const response = await api.post("/auth/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  // Save JWT for later use
  localStorage.setItem("token", response.data.access_token);
  localStorage.setItem("username", username);
  return response.data;
}

export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
}