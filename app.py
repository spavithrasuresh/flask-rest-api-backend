from flask import Flask, jsonify, request

app = Flask(__name__)

# temporary database (list)
users = [
    {"id": 1, "name": "Pavi"},
    {"id": 2, "name": "Alex"}
]

# ---------------- GET all users ----------------
@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(users), 200


# ---------------- POST add user ----------------
@app.route("/api/users", methods=["POST"])
def add_user():
    data = request.get_json()

    # ✅ validation
    if not data or "name" not in data or data["name"].strip() == "":
        return jsonify({"error": "Name is required"}), 400

    name = data["name"]

    # ✅ duplicate check
    for user in users:
        if user["name"].lower() == name.lower():
            return jsonify({"error": "User already exists"}), 400

    new_user = {
        "id": len(users) + 1,
        "name": name
    }

    users.append(new_user)
    return jsonify(new_user), 201


# ---------------- PUT update user ----------------
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    if not data or "name" not in data or data["name"].strip() == "":
        return jsonify({"error": "Name is required"}), 400

    for user in users:
        if user["id"] == user_id:
            user["name"] = data["name"]
            return jsonify(user), 200

    return jsonify({"error": "User not found"}), 404


# ---------------- DELETE user ----------------
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return jsonify({"message": "User deleted successfully"}), 200

    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
