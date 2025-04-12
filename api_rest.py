from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Almacenamiento en memoria
cursos = [
    {"id": 1, "codigo": "IP1", "nombre": "Introducción a la Programación"},
    {"id": 2, "codigo": "ED2", "nombre": "Estructuras de Datos"},
]

@app.route('/cursos', methods=['GET'])
def listar_cursos():
    return jsonify(cursos)

@app.route('/cursos/<int:id>', methods=['GET'])
def obtener_curso(id):
    curso = next((c for c in cursos if c["id"] == id), None)
    if curso:
        return jsonify(curso)
    return jsonify({"error": "Curso no encontrado"}), 404

@app.route('/cursos', methods=['POST'])
def agregar_curso():
    nuevo_curso = request.get_json()
    nuevo_curso["id"] = max([c["id"] for c in cursos], default=0) + 1
    cursos.append(nuevo_curso)
    return jsonify(nuevo_curso), 201


if __name__ == '__main__':
    app.run(port=5000, debug=True)
