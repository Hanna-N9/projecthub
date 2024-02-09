import React from "react";
import axios from "axios";
import { useAuth } from "./AuthContext"; // Import the useAuth hook
import { useNavigate } from "react-router-dom";

export default function Logout() {
  const { setIsAuthenticated, setCurrentUser } = useAuth(); // Use the custom hook to get the setIsAuthenticated and setCurrentUser functions
  const navigate = useNavigate();

  const handleLogout = () => {
    axios
      .delete("/signOut")
      .then(() => {
        setIsAuthenticated(false); // Set isAuthenticated to false
        setCurrentUser(null); // Clear user data from the context
        navigate("/"); // Redirect to the home page
      })
      .catch(error => {
        console.error("Network error", error); // Log any errors that occur
      });
  };

  return <button onClick={handleLogout}>Logout</button>;
}