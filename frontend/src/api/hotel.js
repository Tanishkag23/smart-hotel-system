import api from "./axios";

// ---- Rooms ----
export async function getRooms() {
  const res = await api.get("/rooms/");
  return res.data;
}

export async function createRoom(room) {
  const res = await api.post("/rooms/", room);
  return res.data;
}

export async function updateRoom(roomId, room) {
  const res = await api.put(`/rooms/${roomId}`, room);
  return res.data;
}

export async function deleteRoom(roomId) {
  const res = await api.delete(`/rooms/${roomId}`);
  return res.data;
}

// ---- Bookings ----
export async function createBooking({ room_id, check_in, check_out }) {
  const res = await api.post("/bookings/", { room_id, check_in, check_out });
  return res.data;
}

export async function getBookings() {
  const res = await api.get("/bookings/");
  return res.data;
}

export async function updateBookingStatus(bookingId, newStatus) {
  const res = await api.put(`/bookings/${bookingId}/status`, null, {
    params: { new_status: newStatus },
  });
  return res.data;
}

export async function deleteBooking(bookingId) {
  const res = await api.delete(`/bookings/${bookingId}`);
  return res.data;
}