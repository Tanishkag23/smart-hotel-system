import { useEffect, useState } from "react";
import {
  Plus,
  Trash2,
  Pencil,
  X,
  Loader2,
  BedDouble,
  IndianRupee,
} from "lucide-react";
import { getRooms, createRoom, updateRoom, deleteRoom } from "../api/hotel";

const ROOM_TYPES = ["Single", "Double", "Deluxe", "Suite"];

const emptyForm = { room_number: "", room_type: "Single", base_price: "" };

export default function AdminRooms() {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const load = () => {
    setLoading(true);
    getRooms()
      .then(setRooms)
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  const openCreate = () => {
    setEditingId(null);
    setForm(emptyForm);
    setError("");
    setShowForm(true);
  };

  const openEdit = (room) => {
    setEditingId(room.id);
    setForm({
      room_number: room.room_number,
      room_type: room.room_type,
      base_price: room.base_price,
    });
    setError("");
    setShowForm(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      const payload = { ...form, base_price: parseFloat(form.base_price) };
      if (editingId) {
        await updateRoom(editingId, payload);
      } else {
        await createRoom(payload);
      }
      setShowForm(false);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong.");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this room?")) return;
    await deleteRoom(id);
    load();
  };

  return (
    <div className="min-h-screen bg-hero-gradient">
      <div className="max-w-5xl mx-auto px-6 py-12">
        <div className="flex items-center justify-between mb-8 animate-fade-in">
          <div>
            <h1 className="font-display font-bold text-3xl text-gray-900">
              Manage Rooms
            </h1>
            <p className="text-gray-500 mt-2">Add, edit, or remove hotel rooms.</p>
          </div>
          <button
            onClick={openCreate}
            className="flex items-center gap-2 bg-brand-gradient text-white font-semibold px-5 py-3 rounded-xl shadow-glow hover:opacity-90 transition-opacity"
          >
            <Plus className="w-4 h-4" /> Add Room
          </button>
        </div>

        {loading ? (
          <div className="flex justify-center py-24">
            <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
          </div>
        ) : (
          <div className="glass-card rounded-2xl shadow-card overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b border-gray-200/70">
                  <th className="px-5 py-3.5 font-semibold">Room</th>
                  <th className="px-5 py-3.5 font-semibold">Type</th>
                  <th className="px-5 py-3.5 font-semibold">Price / night</th>
                  <th className="px-5 py-3.5 font-semibold">Availability</th>
                  <th className="px-5 py-3.5 font-semibold text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {rooms.map((room) => (
                  <tr key={room.id} className="border-b border-gray-100/70 last:border-0">
                    <td className="px-5 py-4 font-medium text-gray-900 flex items-center gap-2">
                      <BedDouble className="w-4 h-4 text-primary-500" />
                      {room.room_number}
                    </td>
                    <td className="px-5 py-4 text-gray-600">{room.room_type}</td>
                    <td className="px-5 py-4 text-gray-900 font-semibold flex items-center gap-0.5">
                      <IndianRupee className="w-3.5 h-3.5" />
                      {room.base_price?.toLocaleString("en-IN")}
                    </td>
                    <td className="px-5 py-4">
                      <span
                        className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
                          room.is_available
                            ? "bg-green-100 text-green-700"
                            : "bg-gray-200 text-gray-600"
                        }`}
                      >
                        {room.is_available ? "Available" : "Booked"}
                      </span>
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => openEdit(room)}
                          className="p-2 rounded-lg text-primary-600 hover:bg-primary-50 transition-colors"
                        >
                          <Pencil className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(room.id)}
                          className="p-2 rounded-lg text-red-600 hover:bg-red-50 transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
                {rooms.length === 0 && (
                  <tr>
                    <td colSpan={5} className="text-center py-16 text-gray-400">
                      No rooms yet. Add your first room.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-50 flex items-center justify-center px-4 animate-fade-in">
          <div className="bg-white rounded-3xl shadow-2xl max-w-sm w-full p-7 relative animate-slide-up">
            <button
              onClick={() => setShowForm(false)}
              className="absolute top-5 right-5 text-gray-400 hover:text-gray-700"
            >
              <X className="w-5 h-5" />
            </button>

            <h2 className="font-display font-bold text-xl text-gray-900 mb-6">
              {editingId ? "Edit Room" : "Add New Room"}
            </h2>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 text-sm rounded-xl px-4 py-3 mb-4">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700 mb-1.5 block">
                  Room Number
                </label>
                <input
                  type="text"
                  required
                  value={form.room_number}
                  onChange={(e) => setForm({ ...form, room_number: e.target.value })}
                  placeholder="e.g. 204"
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-400 text-sm"
                />
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 mb-1.5 block">
                  Room Type
                </label>
                <select
                  value={form.room_type}
                  onChange={(e) => setForm({ ...form, room_type: e.target.value })}
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-400 text-sm bg-white"
                >
                  {ROOM_TYPES.map((t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 mb-1.5 block">
                  Base Price (₹ / night)
                </label>
                <input
                  type="number"
                  required
                  min="0"
                  value={form.base_price}
                  onChange={(e) => setForm({ ...form, base_price: e.target.value })}
                  placeholder="e.g. 4000"
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-400 text-sm"
                />
              </div>

              <button
                type="submit"
                disabled={saving}
                className="w-full flex items-center justify-center gap-2 bg-brand-gradient text-white font-semibold py-3 rounded-xl shadow-glow hover:opacity-90 transition-opacity disabled:opacity-60 mt-2"
              >
                {saving ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : editingId ? (
                  "Save Changes"
                ) : (
                  "Add Room"
                )}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}