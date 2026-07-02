import { useEffect, useState } from "react";
import {
  Loader2,
  Calendar,
  IndianRupee,
  ShieldAlert,
  XCircle,
  Trash2,
  BadgeCheck,
} from "lucide-react";
import { getBookings, updateBookingStatus, deleteBooking } from "../api/hotel";
import { useAuth } from "../context/AuthContext";

const statusStyles = {
  confirmed: "bg-green-100 text-green-700",
  cancelled: "bg-red-100 text-red-700",
  completed: "bg-blue-100 text-blue-700",
};

function riskColor(risk) {
  if (risk >= 0.6) return "text-red-600 bg-red-50";
  if (risk >= 0.3) return "text-amber-600 bg-amber-50";
  return "text-green-600 bg-green-50";
}

export default function Bookings() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const { isAdmin } = useAuth();

  const load = () => {
    setLoading(true);
    getBookings()
      .then(setBookings)
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  const handleCancel = async (id) => {
    await updateBookingStatus(id, "cancelled");
    load();
  };

  const handleDelete = async (id) => {
    await deleteBooking(id);
    load();
  };

  return (
    <div className="min-h-screen bg-hero-gradient">
      <div className="max-w-5xl mx-auto px-6 py-12">
        <div className="mb-8 animate-fade-in">
          <h1 className="font-display font-bold text-3xl text-gray-900">
            {isAdmin ? "All Bookings" : "My Bookings"}
          </h1>
          <p className="text-gray-500 mt-2">
            {isAdmin
              ? "Manage every booking across the hotel."
              : "Track your upcoming stays and their status."}
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center py-24">
            <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
          </div>
        ) : bookings.length === 0 ? (
          <div className="text-center py-24 text-gray-400">No bookings yet.</div>
        ) : (
          <div className="space-y-4">
            {bookings.map((b, i) => (
              <div
                key={b.id}
                className="glass-card rounded-2xl shadow-card p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 animate-slide-up"
                style={{ animationDelay: `${i * 50}ms` }}
              >
                <div className="flex items-start gap-4">
                  <div className="w-11 h-11 rounded-xl bg-primary-100 flex items-center justify-center shrink-0">
                    <Calendar className="w-5 h-5 text-primary-600" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <p className="font-semibold text-gray-900">
                        Booking #{b.id} · Room #{b.room_id}
                      </p>
                      <span
                        className={`text-xs font-semibold px-2.5 py-0.5 rounded-full ${statusStyles[b.status] || "bg-gray-100 text-gray-600"}`}
                      >
                        {b.status}
                      </span>
                    </div>
                    <p className="text-sm text-gray-500 mt-0.5">
                      {b.check_in} → {b.check_out}
                      {isAdmin && <span className="ml-2">· Customer #{b.customer_id}</span>}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 flex-wrap">
                  <div className="text-center">
                    <p className="text-[11px] text-gray-400 flex items-center gap-1 justify-center">
                      <IndianRupee className="w-3 h-3" /> Price
                    </p>
                    <p className="font-bold text-gray-900 text-sm">
                      ₹{b.predicted_price?.toLocaleString("en-IN") ?? "—"}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-[11px] text-gray-400 flex items-center gap-1 justify-center">
                      <ShieldAlert className="w-3 h-3" /> Risk
                    </p>
                    <span
                      className={`text-xs font-bold px-2 py-1 rounded-lg ${riskColor(b.cancellation_risk ?? 0)}`}
                    >
                      {b.cancellation_risk != null
                        ? `${(b.cancellation_risk * 100).toFixed(0)}%`
                        : "—"}
                    </span>
                  </div>

                  {b.status !== "cancelled" && (
                    <button
                      onClick={() => handleCancel(b.id)}
                      className="flex items-center gap-1.5 text-xs font-semibold text-amber-700 bg-amber-50 hover:bg-amber-100 px-3 py-2 rounded-xl transition-colors"
                    >
                      <XCircle className="w-3.5 h-3.5" /> Cancel
                    </button>
                  )}
                  {isAdmin && (
                    <button
                      onClick={() => handleDelete(b.id)}
                      className="flex items-center gap-1.5 text-xs font-semibold text-red-700 bg-red-50 hover:bg-red-100 px-3 py-2 rounded-xl transition-colors"
                    >
                      <Trash2 className="w-3.5 h-3.5" /> Delete
                    </button>
                  )}
                  {isAdmin && b.status === "confirmed" && (
                    <button
                      onClick={() => updateBookingStatus(b.id, "completed").then(load)}
                      className="flex items-center gap-1.5 text-xs font-semibold text-blue-700 bg-blue-50 hover:bg-blue-100 px-3 py-2 rounded-xl transition-colors"
                    >
                      <BadgeCheck className="w-3.5 h-3.5" /> Complete
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
