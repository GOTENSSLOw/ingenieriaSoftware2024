from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# Endpoint para el favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Endpoint raiz
@app.route("/")
def root():
    return "hola Rossman"

# Endpoint para obtener un usuario
@app.route("/users/<user_id>")
def get_user(user_id):
    user = {
        "id": user_id,
        "name": "Rosa",
        "telefono": "78485278"
    }
    query = request.args.get("query")
    if query:
        user["query"] = query
    return jsonify(user), 200

# Endpoint para crear un usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    data["status"] = "user created"
    return jsonify(data), 201

# Endpoint para actualizar un usuario
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    updated_user = {
        "id": user_id,
        "name": data.get("name", "Rossman"),
        "telefono": data.get("telefono", "88967051"),
        "status": "user updated"
    }
    return jsonify(updated_user), 200

# Endpoint para borrar un usuario
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    response = {
        "id": user_id,
        "status": "user deleted"
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
