from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")

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


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/rooms")
def get_rooms():
    return jsonify(rooms)


@app.route("/api/rooms/<room_id>/toggle", methods=["POST"])
def toggle_status(room_id):
    room = next((r for r in rooms if r["id"] == room_id), None)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    room["status"] = "Vacant" if room["status"] == "Occupied" else "Occupied"
    return jsonify(room)


@app.route("/api/rooms/<room_id>/schedule", methods=["POST"])
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


if __name__ == "__main__":
    app.run(debug=True)
