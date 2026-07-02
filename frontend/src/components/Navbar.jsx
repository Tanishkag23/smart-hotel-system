import { Link, useNavigate } from "react-router-dom";
import { Hotel, LogOut, LayoutDashboard, DoorOpen, Settings } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { isAuthenticated, isAdmin, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="sticky top-0 z-50 glass-card border-b border-white/40">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-9 h-9 rounded-xl bg-brand-gradient flex items-center justify-center shadow-glow group-hover:scale-105 transition-transform">
            <Hotel className="w-5 h-5 text-white" />
          </div>
          <span className="font-display font-bold text-lg brand-text">
            LuxeStay
          </span>
        </Link>

        <div className="flex items-center gap-2">
          {isAuthenticated ? (
            <>
              <Link
                to="/rooms"
                className="flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium text-gray-700 hover:bg-primary-50 hover:text-primary-700 transition-colors"
              >
                <DoorOpen className="w-4 h-4" />
                Rooms
              </Link>
              <Link
                to="/bookings"
                className="flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium text-gray-700 hover:bg-primary-50 hover:text-primary-700 transition-colors"
              >
                <LayoutDashboard className="w-4 h-4" />
                {isAdmin ? "All Bookings" : "My Bookings"}
              </Link>
              {isAdmin && (
                <Link
                  to="/admin/rooms"
                  className="flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium text-gray-700 hover:bg-primary-50 hover:text-primary-700 transition-colors"
                >
                  <Settings className="w-4 h-4" />
                  Manage Rooms
                </Link>
              )}
              <button
                onClick={handleLogout}
                className="flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium text-white bg-gray-900 hover:bg-gray-800 transition-colors ml-2"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="px-4 py-2 rounded-full text-sm font-medium text-gray-700 hover:bg-primary-50 transition-colors"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="px-5 py-2 rounded-full text-sm font-semibold text-white bg-brand-gradient shadow-glow hover:opacity-90 transition-opacity"
              >
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}