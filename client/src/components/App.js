import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./AuthContext";

import HomePage from "./Homepage";
import Dashboard from "./Dashboard";
import Login from "./Login";
import SignUp from "./SignUp";
import Logout from "./Logout";
import ProjectDetailPage from "./ProjectDetail";
import NavBar from "./NavBar";
import AdminPage from "./AdminPage";
import CommentForm from "./CommentForm";
import EditComment from "./EditComment";
import EditTask from "./EditTask";
import ProjectForm from "./ProjectForm";
import UserProfile from "./UserProfile";
import EditProject from "./EditProject";
import TaskForm from "./TaskForm";

import "../App.css";

export default function App() {
  return (
    <div className="App">
      <NavBar />
      <AuthProvider>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/sign_up" element={<SignUp />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/project/:id" element={<ProjectDetailPage />} />
          <Route path="/user" element={<UserProfile />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/comment-form" element={<CommentForm />} />
          <Route path="/edit-task" element={<EditTask />} />
          <Route path="/task-form" element={<TaskForm />} />
          <Route path="/edit-comment" element={<EditComment />} />
          <Route path="/edit-project" element={<EditProject />} />
          <Route path="/project-form" element={<ProjectForm />} />
          <Route
            path="/redirect-page"
            element={<Navigate to="/error-page" replace />}
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AuthProvider>
    </div>
  );
}