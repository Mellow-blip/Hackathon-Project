from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")

def make_room(id, code, name, floor, status="Vacant"):
    return {"id": id, "code": code, "name": name, "floor": floor,
            "status": status, "schedules": []}

rooms = [
    # ── GROUND FLOOR ────────────────────────────────────────────────
    make_room("machine-shop", "Machine Shop",      "Machine Shop",                    "ground"),
    make_room("cet-117",      "CET 117",           "Lecture Room 117",                "ground"),
    make_room("cet-118",      "CET 118",           "Lecture Room 118",                "ground"),
    make_room("cet-119",      "CET 119",           "Lecture Room 119",                "ground"),
    make_room("cet-121",      "CET 121",           "Lecture Room 121",                "ground"),
    make_room("cet-122",      "CET 122",           "Lecture Room 122",                "ground"),
    make_room("cet-123",      "CET 123",           "Lecture Room 123",                "ground"),
    make_room("cet-124",      "CET 124",           "Lecture Room 124",                "ground"),
    make_room("cet-116",      "CET 116",           "Lecture Room 116",                "ground"),
    make_room("cet-115",      "CET 115",           "Lecture Room 115",                "ground"),
    make_room("faculty-tech", "Faculty Tech",      "Faculty Tech. Dept.",             "ground"),
    make_room("cet-114",      "CET 114",           "Hydraulics Laboratory",           "ground"),
    make_room("soil-lab",     "Soil Lab",          "Soil Laboratory",                 "ground"),
    make_room("sto",          "STO",               "School Treasurer's Office",       "ground"),
    make_room("deans-office", "Dean's Office",     "Dean's Office (Ground)",          "ground"),
    make_room("cet-120",      "CET 120",           "Lecture Room 120",                "ground"),
    make_room("cet-113",      "CET 113",           "Physics Laboratory",              "ground"),
    make_room("cet-112",      "CET 112",           "Lecture Room 112",                "ground"),
    make_room("cet-111",      "CET 111",           "Lecture Room 111",                "ground"),
    make_room("cet-110",      "CET 110",           "Lecture Room 110",                "ground"),
    make_room("cet-109",      "CET 109",           "Lecture Room 109",                "ground"),
    make_room("faculty-rm",   "Faculty RM",        "Faculty Room (College of Eng.)",  "ground"),
    make_room("cet-105",      "CET 105",           "Lecture Room 105",                "ground"),
    make_room("cet-106",      "CET 106",           "Lecture Room 106",                "ground"),
    make_room("cet-107",      "CET 107",           "Lecture Room 107",                "ground"),
    make_room("cet-108",      "CET 108",           "Lecture Room 108",                "ground"),
    make_room("faculty-cba",  "Faculty RM CBA",    "Faculty Room (CBA)",              "ground"),
    make_room("deans-cba",    "Dean's CBA",        "Dean's Office (CBA)",             "ground"),
    make_room("cet-104",      "CET 104",           "Lecture Room 104",                "ground"),
    make_room("rba-hall",     "RBA Hall",          "RBA Hall",                        "ground"),
    make_room("san-lorenzo",  "San Lorenzo Ruiz",  "San Lorenzo Ruiz Study Area",     "ground"),
    make_room("cet-103",      "CET 103",           "Lecture Room 103",                "ground"),
    make_room("cet-102",      "CET 102",           "Lecture Room 102",                "ground"),
    make_room("cet-101",      "CET 101",           "Lecture Room 101",                "ground"),
    make_room("garage",       "Garage",            "Garage",                          "ground"),
    # ── SECOND FLOOR ────────────────────────────────────────────────
    make_room("emrc-ii",       "EMRC II",            "EMRC II Laboratory",             "second"),
    make_room("cet-213",       "CET 213",            "Lecture Room 213",               "second"),
    make_room("cet-214",       "CET 214",            "Lecture Room 214",               "second"),
    make_room("cet-215",       "CET 215",            "Lecture Room 215",               "second"),
    make_room("cet-216",       "CET 216",            "Lecture Room 216",               "second"),
    make_room("cet-217",       "CET 217",            "Lecture Room 217",               "second"),
    make_room("accounting",    "Accounting Clinic",  "Accounting Clinic",              "second"),
    make_room("control-room",  "Control Room",       "Control Room",                   "second"),
    make_room("cet-212",       "CET 212",            "Lecture Room 212",               "second"),
    make_room("cet-211",       "CET 211",            "Lecture Room 211",               "second"),
    make_room("cet-208",       "CET 208",            "Lecture Room 208",               "second"),
    make_room("cet-207",       "CET 207",            "Lecture Room 207",               "second"),
    make_room("cet-206",       "CET 206",            "Lecture Room 206",               "second"),
    make_room("office-sim",    "Office Sim Room",    "Office Simulation Room",         "second"),
    make_room("cet-210",       "CET 210",            "CBA-DSC Room 210",               "second"),
    make_room("cet-209",       "CET 209",            "Lecture Room 209",               "second"),
    make_room("nutrition-lab", "Nutrition Lab",      "Nutrition Laboratory",           "second"),
    make_room("cet-204",       "CET 204",            "Lecture Room 204",               "second"),
    make_room("cet-203",       "CET 203",            "Lecture Room 203",               "second"),
    make_room("cet-202",       "CET 202",            "Lecture Room 202",               "second"),
    make_room("cet-201",       "CET 201",            "Lecture Room 201",               "second"),
    make_room("counseling",    "Counseling Room",    "Counseling Room",                "second"),
]


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/rooms")
def get_rooms():
    floor = request.args.get("floor")
    if floor:
        return jsonify([r for r in rooms if r["floor"] == floor])
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
