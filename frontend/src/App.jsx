import { Route, Routes, Link, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import Register from "./Register";
import Login from "./Login";
import "./App.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();
  const location = useLocation(); // Get the current path

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (token) {
      setIsLoggedIn(true);
    } else {
      // ✅ Redirect to login unless already on Register page
      if (location.pathname !== "/register") {
        navigate("/login");
      }
    }
  }, [navigate, location.pathname]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    navigate("/login");
  };

  return (
    <>
      {/* ✅ Show nav only when NOT logged in and NOT on login/register pages */}
      {!isLoggedIn && location.pathname !== "/login" && location.pathname !== "/register" && (
        <nav className="auth-nav">
          <Link to="/register">Register</Link>
          <Link to="/login">Login</Link>
        </nav>
      )}

      {/* ✅ Logout button when logged in */}
      {isLoggedIn && (
        <button className="logout-btn" onClick={handleLogout}>Logout</button>
      )}

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login onLogin={() => setIsLoggedIn(true)} />} />
      </Routes>
    </>
  );
}

// ✅ Improved Home Page
const Home = () => (
  <div className="home-container">
    <h1>Welcome to Autopick!</h1>
    <p>Answer the following questions:</p>
    <ul>
      <li>Do you want a fuel-efficient car?</li>
      <li>Do you need cargo space?</li>
      <li>Will you be driving in snow?</li>
    </ul>
  </div>
);

export default App;
