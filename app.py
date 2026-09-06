from flask import Flask, jsonify, request, send_from_directory, session
from functools import wraps
from datetime import datetime

app = Flask(__name__, static_folder="static")
app.secret_key = "mseuf-cet-secret-key-2026"

# ── In-memory room data ──────────────────────────────────────────────
rooms = [
    {
        "id": "cpe-lab",
        "code": "CpE Lab",
        "name": "Computer Engineering Lab",
        "status": "Occupied",
        "schedules": [
            {"time": "08:00 AM - 11:00 AM", "subject": "CPE 411 - Embedded Systems", "prof": "Engr. Santos"}
        ],
    },
    {
        "id": "cet-101",
        "code": "CET 101",
        "name": "Lecture Room 101",
        "status": "Vacant",
        "schedules": [],
    },
    {
        "id": "cet-102",
        "code": "CET 102",
        "name": "Lecture Room 102",
        "status": "Occupied",
        "schedules": [
            {"time": "01:00 PM - 04:00 PM", "subject": "CPE 311 - Logic Circuits", "prof": "Engr. Ramos"}
        ],
    },
    {
        "id": "circuits-lab",
        "code": "Circuits Lab",
        "name": "Electrical Lab",
        "status": "Vacant",
        "schedules": [],
    },
    {
        "id": "deans-office",
        "code": "Dean's Office",
        "name": "CET Administrative Office",
        "status": "Occupied",
        "schedules": [
            {"time": "08:00 AM - 05:00 PM", "subject": "Faculty Consultations", "prof": "Dean Engineering"}
        ],
    },
]

# ── In-memory public notes ───────────────────────────────────────────
# { room_id: [ { "author": str, "text": str, "timestamp": str } ] }
public_notes = {room["id"]: [] for room in rooms}


# ── Role protection decorator ────────────────────────────────────────
def teacher_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "teacher":
            return jsonify({"error": "Teacher access required"}), 403
        return f(*args, **kwargs)
    return decorated


# ── Static pages ─────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ── Auth endpoints ───────────────────────────────────────────────────
@app.route("/api/login", methods=["POST"])
def login():
    body = request.get_json(force=True)
    role = body.get("role", "").lower()
    name = body.get("name", "").strip()
    if role not in ("teacher", "student"):
        return jsonify({"error": "Invalid role"}), 400
    if not name:
        return jsonify({"error": "Name is required"}), 400
    session["role"] = role
    session["name"] = name
    return jsonify({"role": role, "name": name})


@app.route("/api/me")
def me():
    if "role" not in session:
        return jsonify({"logged_in": False}), 200
    return jsonify({"logged_in": True, "role": session["role"], "name": session["name"]})


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})


# ── Room endpoints ───────────────────────────────────────────────────
@app.route("/api/rooms")
def get_rooms():
    return jsonify(rooms)


@app.route("/api/rooms/<room_id>/toggle", methods=["POST"])
@teacher_required
def toggle_status(room_id):
    room = next((r for r in rooms if r["id"] == room_id), None)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    room["status"] = "Vacant" if room["status"] == "Occupied" else "Occupied"
    return jsonify(room)


@app.route("/api/rooms/<room_id>/schedule", methods=["POST"])
@teacher_required
def add_schedule(room_id):
    room = next((r for r in rooms if r["id"] == room_id), None)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    body = request.get_json(force=True)
    room["schedules"].append({
        "subject": body["subject"],
        "prof": body["prof"],
        "time": body["time"],
    })
    room["status"] = "Occupied"
    return jsonify(room)


# ── Public notes endpoints ───────────────────────────────────────────
@app.route("/api/rooms/<room_id>/public-notes")
def get_public_notes(room_id):
    if room_id not in public_notes:
        return jsonify({"error": "Room not found"}), 404
    return jsonify(public_notes[room_id])


@app.route("/api/rooms/<room_id>/public-notes", methods=["POST"])
@teacher_required
def add_public_note(room_id):
    if room_id not in public_notes:
        return jsonify({"error": "Room not found"}), 404
    body = request.get_json(force=True)
    text = body.get("text", "").strip()
    if not text:
        return jsonify({"error": "Note text is required"}), 400
    note = {
        "author": session.get("name", "Unknown"),
        "text": text,
        "timestamp": datetime.now().strftime("%b %d, %Y %I:%M %p"),
    }
    public_notes[room_id].append(note)
    return jsonify(public_notes[room_id])


@app.route("/api/rooms/<room_id>/public-notes/<int:note_index>", methods=["DELETE"])
@teacher_required
def delete_public_note(room_id, note_index):
    if room_id not in public_notes:
        return jsonify({"error": "Room not found"}), 404
    notes = public_notes[room_id]
    if note_index < 0 or note_index >= len(notes):
        return jsonify({"error": "Note not found"}), 404
    notes.pop(note_index)
    return jsonify(notes)


if __name__ == "__main__":
    app.run(debug=True)
