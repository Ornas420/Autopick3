import { Route, Routes, Link } from "react-router-dom";
import Register from "./Register";
<<<<<<< HEAD
=======
import Login from "./Login";
>>>>>>> Feature
import "./App.css";

function App() {
  return (
    <>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/register">Register</Link>
<<<<<<< HEAD
=======
        <Link to="/login">Login</Link>
>>>>>>> Feature
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
<<<<<<< HEAD
=======
        <Route path="/login" element={<Login />} />
>>>>>>> Feature
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

<<<<<<< HEAD
export default App;
=======
export default App;
>>>>>>> Feature
