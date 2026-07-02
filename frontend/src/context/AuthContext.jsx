import { createContext, useContext, useState } from "react";
import { loginUser, registerUser } from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("access_token"));
  const [role, setRole] = useState(localStorage.getItem("role"));

  const login = async (email, password) => {
    const data = await loginUser({ email, password });
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("role", data.role);
    setToken(data.access_token);
    setRole(data.role);
    return data;
  };

  const register = async (payload) => {
    const data = await registerUser(payload);
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("role", data.role);
    setToken(data.access_token);
    setRole(data.role);
    return data;
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("role");
    setToken(null);
    setRole(null);
  };

  const isAuthenticated = Boolean(token);
  const isAdmin = role === "admin" || role === "staff";

  return (
    <AuthContext.Provider
      value={{ token, role, isAuthenticated, isAdmin, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
