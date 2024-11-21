from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Endpoint raíz
@app.route("/")
def root():
    return render_template("index.html")


'''
Crear los endpoints para los siguientes métodos
GET --> Obtener información
POST --> Crear información
PUT --> Actualizar información
DELETE --> Borrar información
'''
# Endpoint para eliminar un usuario existente (DELETE)

@app.route("/users/delete/<int:user_id>", methods=['GET'])

def delete_user(user_id):

    user = User.query.get(user_id)

    if not user:

        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)

    db.session.commit()

    return redirect(url_for('get_users'))

# Endpoint para editar un usuario existente (PUT)

@app.route("/users/edit/<int:user_id>", methods=['GET', 'POST'])

def edit_user(user_id):

    user = User.query.get(user_id)

    if not user:

        return jsonify({"error": "User not found"}), 404

    if request.method == 'POST':

        data = request.form

        user.name = data.get("name", user.name)

        user.telefono = data.get("telefono", user.telefono)

        db.session.commit()

        return redirect(url_for('get_users'))

    return render_template("edit_user.html", user=user)

# Endpoint para agregar un nuevo usuario (POST)

@app.route("/users/new", methods=['GET', 'POST'])

def add_user():

    if request.method == 'POST':

        data = request.form

        new_user = User(name=data['name'], telefono=data['telefono'])

        db.session.add(new_user)

        db.session.commit()

        return redirect(url_for('get_users'))

    return render_template("add_user.html")

# Endpoint para mostrar todos los usuarios (GET)

@app.route("/users", methods=['GET'])

def get_users():

    users = User.query.all()

    users_list = [{"id": user.id, "name": user.name,
    "telefono": user.telefono} for user in users]

    return render_template("users.html", users=users_list)

# Endpoint para obtener un usuario por ID
@app.route("/users/<user_id>")
def get_user(user_id):
    user = {
        "id": user_id,
        "name": "Aarock",
        "telefono": "57993449"
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
        "name": data.get("name", "Aarock"),  # Valor por defecto si no se envía "name"
        "telefono": data.get("telefono", "57993449"),  # Valor por defecto si no se envía "telefono"
        "status": "user updated"
    }
    return jsonify(updated_user), 200

# Endpoint para borrar un usuario
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user_id(user_id):
    response = {
        "id": user_id,
        "status": "user deleted"
    }
    return jsonify(response), 200

# Define el modelo de usuario

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    telefono = db.Column(db.String(20), nullable=False)

# Crea las tablas en la base de datos (solo la primera vez)

with app.app_context():

    db.create_all() 


if __name__ == '__main__':
    app.run(debug=True)
