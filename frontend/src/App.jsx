import { Route, Routes, Link } from "react-router-dom";
import Register from "./Register";
import "./App.css";

function App() {
  return (
    <>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/register">Register</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </>
  );
}

const Home = () => (
  <div>
    <h1>Welcome to Autopick!</h1>
    <p>Click "Register" to sign up.</p>
  </div>
);

export default App;
