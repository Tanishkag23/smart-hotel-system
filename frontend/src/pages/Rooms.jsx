import { useEffect, useState } from "react";
import {
  BedDouble,
  Users,
  Sparkles,
  X,
  Calendar,
  Loader2,
  IndianRupee,
  ShieldAlert,
  CheckCircle2,
} from "lucide-react";
import { getRooms, createBooking } from "../api/hotel";

const ROOM_IMAGES = {
  Single: "https://images.unsplash.com/photo-1595576508898-0ad5c879a061?w=800&q=80",
  Double: "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800&q=80",
  Deluxe: "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",
  Suite: "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80",
};

function BookingModal({ room, onClose, onSuccess }) {
  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleBook = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const booking = await createBooking({
        room_id: room.id,
        check_in: checkIn,
        check_out: checkOut,
      });
      setResult(booking);
    } catch (err) {
      setError(err.response?.data?.detail || "Booking failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-50 flex items-center justify-center px-4 animate-fade-in">
      <div className="bg-white rounded-3xl shadow-2xl max-w-md w-full p-7 relative animate-slide-up">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 text-gray-400 hover:text-gray-700 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {!result ? (
          <>
            <h2 className="font-display font-bold text-xl text-gray-900 mb-1">
              Book {room.room_type} Room
            </h2>
            <p className="text-gray-500 text-sm mb-6">Room #{room.room_number}</p>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 text-sm rounded-xl px-4 py-3 mb-4">
                {error}
              </div>
            )}

            <form onSubmit={handleBook} className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700 mb-1.5 block">
                  Check-in
                </label>
                <div className="relative">
                  <Calendar className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="date"
                    required
                    value={checkIn}
                    onChange={(e) => setCheckIn(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-400 text-sm"
                  />
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700 mb-1.5 block">
                  Check-out
                </label>
                <div className="relative">
                  <Calendar className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="date"
                    required
                    value={checkOut}
                    onChange={(e) => setCheckOut(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-400 text-sm"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full flex items-center justify-center gap-2 bg-brand-gradient text-white font-semibold py-3 rounded-xl shadow-glow hover:opacity-90 transition-opacity disabled:opacity-60"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Confirm Booking"}
              </button>
            </form>
          </>
        ) : (
          <div className="text-center py-2 animate-fade-in">
            <div className="w-14 h-14 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
              <CheckCircle2 className="w-7 h-7 text-green-600" />
            </div>
            <h2 className="font-display font-bold text-xl text-gray-900 mb-1">
              Booking Confirmed!
            </h2>
            <p className="text-gray-500 text-sm mb-6">
              Your {room.room_type} room is reserved.
            </p>

            <div className="bg-primary-50 rounded-2xl p-5 space-y-3 text-left">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 flex items-center gap-1.5">
                  <IndianRupee className="w-4 h-4" /> AI Predicted Price
                </span>
                <span className="font-bold text-gray-900">
                  ₹{result.predicted_price?.toLocaleString("en-IN")}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500 flex items-center gap-1.5">
                  <ShieldAlert className="w-4 h-4" /> Cancellation Risk
                </span>
                <span className="font-bold text-gray-900">
                  {(result.cancellation_risk * 100).toFixed(1)}%
                </span>
              </div>
            </div>

            <button
              onClick={onSuccess}
              className="w-full mt-6 bg-gray-900 text-white font-semibold py-3 rounded-xl hover:bg-gray-800 transition-colors"
            >
              View My Bookings
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default function Rooms() {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [successNavigate, setSuccessNavigate] = useState(false);

  useEffect(() => {
    getRooms()
      .then(setRooms)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (successNavigate) {
    window.location.href = "/bookings";
  }

  return (
    <div className="min-h-screen bg-hero-gradient">
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="mb-10 animate-fade-in">
          <div className="inline-flex items-center gap-1.5 bg-primary-100 text-primary-700 text-xs font-semibold px-3 py-1.5 rounded-full mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            AI-Powered Dynamic Pricing
          </div>
          <h1 className="font-display font-bold text-3xl md:text-4xl text-gray-900">
            Find your perfect stay
          </h1>
          <p className="text-gray-500 mt-2">
            Prices are calculated in real-time based on demand, season & stay length.
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center py-24">
            <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
          </div>
        ) : rooms.length === 0 ? (
          <div className="text-center py-24 text-gray-400">No rooms available yet.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {rooms.map((room, i) => (
              <div
                key={room.id}
                className="glass-card rounded-3xl overflow-hidden shadow-card hover:shadow-glow hover:-translate-y-1 transition-all duration-300 animate-slide-up"
                style={{ animationDelay: `${i * 60}ms` }}
              >
                <div className="h-44 overflow-hidden relative">
                  <img
                    src={ROOM_IMAGES[room.room_type] || ROOM_IMAGES.Double}
                    alt={room.room_type}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute top-3 right-3 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-xs font-semibold text-primary-700 shadow">
                    {room.room_type}
                  </div>
                  {!room.is_available && (
                    <div className="absolute inset-0 bg-gray-900/60 flex items-center justify-center">
                      <span className="text-white font-semibold text-sm">Fully Booked</span>
                    </div>
                  )}
                </div>

                <div className="p-5">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-display font-semibold text-lg text-gray-900 flex items-center gap-2">
                      <BedDouble className="w-4 h-4 text-primary-500" />
                      Room {room.room_number}
                    </h3>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs text-gray-400">Base price / night</p>
                      <p className="font-bold text-lg text-gray-900">
                        ₹{room.base_price?.toLocaleString("en-IN")}
                      </p>
                    </div>
                    <button
                      onClick={() => setSelectedRoom(room)}
                      disabled={!room.is_available}
                      className="bg-brand-gradient text-white text-sm font-semibold px-5 py-2.5 rounded-xl shadow-glow hover:opacity-90 transition-opacity disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                      Book Now
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedRoom && (
        <BookingModal
          room={selectedRoom}
          onClose={() => setSelectedRoom(null)}
          onSuccess={() => setSuccessNavigate(true)}
        />
      )}
    </div>
  );
}
