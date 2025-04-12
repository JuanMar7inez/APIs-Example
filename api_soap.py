from flask import Flask, request, make_response
from flask_cors import CORS
from spyne import Application, rpc, ServiceBase, Unicode, Integer, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# Configuración de Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Modelo de curso
class Curso(ComplexModel):
    codigo = Unicode
    nombre = Unicode
    id = Integer

# Servicio SOAP
class EduServicios(ServiceBase):
    cursos = [
        {"id": 1, "codigo": "IP1", "nombre": "Introducción a la Programación"},
        {"id": 2, "codigo": "ED2", "nombre": "Estructuras de Datos"}
    ]

    @rpc(Unicode(custom_namespace='edu.soap.cursos'), _returns=Curso)
    def getCursoPorCodigo(ctx, codigo):
        print(f"[DEBUG] Buscando curso con código: {codigo}")
        curso = next((c for c in EduServicios.cursos if c["codigo"] == codigo), None)
        if curso:
            return Curso(id=curso["id"], codigo=curso["codigo"], nombre=curso["nombre"])
        return Curso(id=-1, codigo="N/A", nombre="No encontrado")

# Aplicación SOAP
soap_app = Application(
    [EduServicios],
    tns='edu.soap.cursos',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

# WSGI app para el servidor SOAP
wsgi_app = WsgiApplication(soap_app)

# Manejo de solicitudes SOAP (POST)
@app.route('/', methods=['POST'])
def soap_request():
    environ = request.environ.copy()

    def start_response(status, headers):
        return None  # No necesitamos hacer nada aquí

    return wsgi_app(environ, start_response)

# Soporte para preflight (CORS)
@app.route('/', methods=['OPTIONS'])
def handle_options():
    response = make_response('')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, SOAPAction'
    return response

# Iniciar servidor
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, app)
    print("✅ SOAP API corriendo en http://127.0.0.1:8000")
    server.serve_forever()
