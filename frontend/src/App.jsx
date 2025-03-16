import { Route, Routes, Link, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Register from "./Register";
import Login from "./Login";
import "./App.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Check login state on component mount
  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token); // Set isLoggedIn to true if token exists
  }, []);

  return (
    <>
      <nav>
        <Link to="/register">Register</Link>
        <Link to="/login">Login</Link>
      </nav>
      <Routes>
        <Route
          path="/"
          element={isLoggedIn ? <Home /> : <Navigate to="/login" />}
        />
        <Route path="/register" element={<Register />} />
        <Route
          path="/login"
          element={<Login onLogin={() => setIsLoggedIn(true)} />}
        />
      </Routes>
    </>
  );
}

const Home = () => (
  <div>
    <h1>Welcome to Autopick!</h1>
    <p>Please answer the following questions:</p>
    <ul>
      <li>Do you want a car that saves money on gas? (Fuel efficiency)</li>
      <li>Do you need extra cargo space for groceries, luggage, or gear? (Cargo space)</li>
      <li>Will you be driving in snowy or icy conditions often? (Snow handling)</li>
    </ul>
  </div>
);

export default App;