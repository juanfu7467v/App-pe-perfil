from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Configurar conexión a PostgreSQL (usando DATABASE_URL desde Railway)
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = conn.cursor()

# Ruta para guardar o actualizar perfil
@app.route("/perfil", methods=["POST"])
def guardar_perfil():
    data = request.json
    cursor.execute("""
        INSERT INTO perfiles (numero_whatsapp, nombre, genero, edad, descripcion)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (numero_whatsapp)
        DO UPDATE SET nombre=%s, genero=%s, edad=%s, descripcion=%s
    """, (
        data['numero_whatsapp'], data['nombre'], data['genero'], data['edad'], data['descripcion'],
        data['nombre'], data['genero'], data['edad'], data['descripcion']
    ))
    conn.commit()
    return jsonify({"status": "perfil guardado"})

# Ruta para obtener perfil por número
@app.route("/perfil", methods=["GET"])
def obtener_perfil():
    numero = request.args.get("numero_whatsapp")
    cursor.execute("SELECT nombre, genero, edad, descripcion FROM perfiles WHERE numero_whatsapp = %s", (numero,))
    result = cursor.fetchone()
    if result:
        return jsonify({
            "nombre": result[0],
            "genero": result[1],
            "edad": result[2],
            "descripcion": result[3]
        })
    else:
        return jsonify({"error": "Perfil no encontrado"}), 404

@app.route("/", methods=["GET"])
def inicio():
    return "API de Perfiles funcionando"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
