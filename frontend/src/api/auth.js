import api from "./axios";

export async function registerUser({ name, email, phone, password, role = "customer" }) {
  const res = await api.post("/auth/register", { name, email, phone, password, role });
  return res.data;
}

export async function loginUser({ email, password }) {
  // Backend OAuth2PasswordRequestForm expects form-urlencoded data,
  // JSON nahi. Isliye URLSearchParams use karte hai.
  const form = new URLSearchParams();
  form.append("username", email); // backend "username" field expect karta hai, hum usme email daal rahe hai
  form.append("password", password);

  const res = await api.post("/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return res.data;
}
