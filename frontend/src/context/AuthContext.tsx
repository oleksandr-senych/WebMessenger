import { createContext, useContext, useState, type ReactNode } from "react";

interface AuthContextType {
  token: string | null;
  setToken: (token: string | null) => void;
  username: string | null;
  setUsername: (username: string | null) => void;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  setToken: () => {},
  username: null,
  setUsername: () => {}
 
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [username, setUsername] = useState<string | null>(localStorage.getItem("username"));
  return (
    <AuthContext.Provider value={{ token, setToken, username, setUsername }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}