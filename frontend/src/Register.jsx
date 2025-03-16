import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

const Register = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isSuccess, setIsSuccess] = useState(false); // ✅ Track success/error message
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (response.ok) {
      setMessage("User registered successfully!");
      setIsSuccess(true); // ✅ Success message (green)
      setTimeout(() => navigate("/login"), 1500);
    } else {
      setMessage(data.error);
      setIsSuccess(false); // ✅ Error message (red)
    }
  };

  return (
    <div className="form-wrapper">
      <div className="form-container">
        <h2>Sign Up</h2>
        <p>Sign up to continue</p>
        <form onSubmit={handleRegister}>
          <input
            type="text"
            className="input-field"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            className="input-field"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" className="btn">Sign Up</button>
        </form>

        {/* ✅ Success (green) or error (red) message */}
        {message && (
          <p className={isSuccess ? "success-message" : "error-message"}>
            {message}
          </p>
        )}

        <div className="auth-links">
          <p>Already have an account? <a href="/login">Log in</a></p>
        </div>
      </div>
    </div>
  );
};

export default Register;
