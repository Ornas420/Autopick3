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
      // ✅ Allow access to register page even when not logged in
      if (location.pathname !== "/register") {
        navigate("/login"); // Redirect if not logged in
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
      {!isLoggedIn && (
        <nav>
          <Link to="/register">Register</Link>
          <Link to="/login">Login</Link>
        </nav>
      )}

      {isLoggedIn && (
        <button className="logout-btn" onClick={handleLogout}>Logout</button>
      )}

      <Routes>
        <Route path="/" element={<Home isLoggedIn={isLoggedIn} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login onLogin={() => setIsLoggedIn(true)} />} />
      </Routes>
    </>
  );
}

const Home = ({ isLoggedIn }) => (
  <div>
    <h1>Welcome to Autopick!</h1>
    <p>Please answer the following questions:</p>
    <ul>
      <li>Do you want a fuel-efficient car?</li>
      <li>Do you need cargo space?</li>
      <li>Will you be driving in snow?</li>
    </ul>
  </div>
);

export default App;
