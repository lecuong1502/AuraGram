import { Routes, Route, Navigate } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";
import MainLayout from "@/components/layout/MainLayout";
import FeedPage from "@/pages/Feed/FeedPage";
import ProfilePage from "@/pages/Profile/ProfilePage";
import PostPage from "@/pages/Post/PostPage";
import LoginPage from "@/pages/Auth/LoginPage";
import RegisterPage from "@/pages/Auth/RegisterPage";

function PrivateRoute({ children }) {
  const accessToken = useAuthStore((s) => s.accessToken);
  return accessToken ? children : <Navigate to="/login" replace />;
}
 
function GuestRoute({ children }) {
  const accessToken = useAuthStore((s) => s.accessToken);
  return accessToken ? <Navigate to="/" replace /> : children;
}
 
export default function App() {
  return (
    <Routes>
      {/* Guest only */}
      <Route path="/login" element={<GuestRoute><LoginPage /></GuestRoute>} />
      <Route path="/register" element={<GuestRoute><RegisterPage /></GuestRoute>} />
 
      {/* Protected */}
      <Route element={<PrivateRoute><MainLayout /></PrivateRoute>}>
        <Route index element={<FeedPage />} />
        <Route path="/p/:postId" element={<PostPage />} />
        <Route path="/:username" element={<ProfilePage />} />
      </Route>
 
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}