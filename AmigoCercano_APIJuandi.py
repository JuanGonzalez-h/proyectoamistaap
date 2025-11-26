"""
AmigoCercano_APIJuandi.py - API de Juan (POST - CREAR/MODIFICAR)

Esta API permite CREAR y MODIFICAR amigos usando el método POST.
Usa programación orientada a objetos para manejar las peticiones.

Autor: Juan
Versión: 2.0 - Simplificada con POO
"""

from flask import Flask, request, jsonify
from AmigoRegular import AmigoRegular
from AmigoCercano import AmigoCercano
from config import obtener_gestor, guardar_datos

# Crear la aplicación Flask
app = Flask(__name__)


# ============================================
# CLASE AUXILIAR: ManejadorRespuestas
# ============================================
class ManejadorRespuestas:
    """
    Clase que centraliza la creación de respuestas JSON.
    
    Esto sigue el principio de POO: una clase con una responsabilidad específica.
    En lugar de repetir código, usamos métodos reutilizables.
    """
    
    @staticmethod
    def exito(mensaje, datos=None, codigo=200):
        """
        Crea una respuesta exitosa.
        
        Args:
            mensaje (str): Mensaje descriptivo
            datos (dict): Datos adicionales a incluir
            codigo (int): Código HTTP (200, 201, etc.)
        
        Returns:
            tuple: (respuesta_json, codigo_http)
        """
        respuesta = {
            "exito": True,
            "mensaje": mensaje
        }
        
        if datos:
            respuesta.update(datos)
        
        return jsonify(respuesta), codigo
    
    @staticmethod
    def error(mensaje, codigo=400):
        """
        Crea una respuesta de error.
        
        Args:
            mensaje (str): Mensaje de error
            codigo (int): Código HTTP de error (400, 404, 500, etc.)
        
        Returns:
            tuple: (respuesta_json, codigo_http)
        """
        return jsonify({
            "exito": False,
            "error": mensaje
        }), codigo


# ============================================
# CLASE PRINCIPAL: ControladorAmigos
# ============================================
class ControladorAmigos:
    """
    Controlador que maneja todas las operaciones relacionadas con amigos.
    
    Esta clase encapsula la lógica de negocio de la API.
    Cada método representa una operación específica.
    """
    
    def __init__(self):
        """Constructor: inicializa el manejador de respuestas"""
        self.respuestas = ManejadorRespuestas()
    
    def validar_datos_basicos(self, datos):
        """
        Valida que los datos básicos estén presentes.
        
        Args:
            datos (dict): Datos recibidos en la petición
        
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        if not datos:
            return False, "No se enviaron datos"
        
        if not datos.get('nombre'):
            return False, "Falta el campo obligatorio: nombre"
        
        if not datos.get('cumpleanos'):
            return False, "Falta el campo obligatorio: cumpleanos"
        
        return True, None
    
    def crear_amigo_regular(self, datos):
        """
        Crea un nuevo amigo regular.
        
        Args:
            datos (dict): Datos del amigo a crear
        
        Returns:
            tuple: Respuesta HTTP
        """
        # 1. Validar datos básicos
        es_valido, mensaje_error = self.validar_datos_basicos(datos)
        if not es_valido:
            return self.respuestas.error(mensaje_error, 400)
        
        # 2. Extraer datos con valores por defecto
        nombre = datos.get('nombre')
        cumpleanos = datos.get('cumpleanos')
        gustos = datos.get('gustos', [])
        recuerdos = datos.get('recuerdos', [])
        anecdotas = datos.get('anecdotas', [])
        
        # 3. Crear el objeto AmigoRegular (POO)
        nuevo_amigo = AmigoRegular(nombre, cumpleanos, gustos, recuerdos, anecdotas)
        
        # 4. Obtener el gestor y agregar el amigo
        gestor = obtener_gestor()
        gestor.agregarAmigo(nuevo_amigo)
        
        # 5. Guardar en el archivo
        guardar_datos()
        
        # 6. Retornar respuesta exitosa
        return self.respuestas.exito(
            "Amigo regular creado exitosamente",
            {"nombre": nombre, "tipo": "Amigo Regular"},
            201
        )
    
    def crear_amigo_cercano(self, datos):
        """
        Crea un nuevo amigo cercano.
        
        Args:
            datos (dict): Datos del amigo a crear
        
        Returns:
            tuple: Respuesta HTTP
        """
        # 1. Validar datos básicos
        es_valido, mensaje_error = self.validar_datos_basicos(datos)
        if not es_valido:
            return self.respuestas.error(mensaje_error, 400)
        
        # 2. Validar nivel de confianza
        nivelConfianza = datos.get('nivelConfianza')
        
        if nivelConfianza is None:
            return self.respuestas.error("Falta el campo obligatorio: nivelConfianza", 400)
        
        if nivelConfianza < 1 or nivelConfianza > 10:
            return self.respuestas.error("El nivel de confianza debe estar entre 1 y 10", 400)
        
        # 3. Extraer datos con valores por defecto
        nombre = datos.get('nombre')
        cumpleanos = datos.get('cumpleanos')
        gustos = datos.get('gustos', [])
        recuerdos = datos.get('recuerdos', [])
        anecdotas = datos.get('anecdotas', [])
        
        # 4. Crear el objeto AmigoCercano (POO)
        nuevo_amigo = AmigoCercano(nombre, cumpleanos, gustos, recuerdos, anecdotas, nivelConfianza)
        
        # 5. Obtener el gestor y agregar el amigo
        gestor = obtener_gestor()
        gestor.agregarAmigo(nuevo_amigo)
        
        # 6. Guardar en el archivo
        guardar_datos()
        
        # 7. Retornar respuesta exitosa
        return self.respuestas.exito(
            "Amigo cercano creado exitosamente",
            {
                "nombre": nombre,
                "nivelConfianza": nivelConfianza,
                "tipo": "Amigo Cercano"
            },
            201
        )
    
    def agregar_recuerdo(self, nombre, recuerdo, tipo_amigo):
        """
        Agrega un recuerdo a un amigo existente.
        
        Args:
            nombre (str): Nombre del amigo
            recuerdo (str): Texto del recuerdo
            tipo_amigo (str): "AmigoRegular" o "AmigoCercano"
        
        Returns:
            tuple: Respuesta HTTP
        """
        # 1. Validar que se envió el recuerdo
        if not recuerdo:
            return self.respuestas.error("Falta el campo: recuerdo", 400)
        
        # 2. Buscar el amigo en el gestor
        gestor = obtener_gestor()
        amigo = gestor.buscarAmigo(nombre)
        
        if not amigo:
            return self.respuestas.error(f"No se encontró el amigo: {nombre}", 404)
        
        # 3. Verificar que el tipo coincida
        tipo_actual = type(amigo).__name__
        if tipo_actual != tipo_amigo:
            return self.respuestas.error(
                f"El amigo '{nombre}' no es de tipo {tipo_amigo}, es {tipo_actual}",
                400
            )
        
        # 4. Agregar el recuerdo usando el método del objeto (POO)
        resultado = amigo.agregarRecuerdo(recuerdo)
        
        # 5. Guardar cambios
        guardar_datos()
        
        # 6. Retornar respuesta exitosa
        return self.respuestas.exito(
            "Recuerdo agregado exitosamente",
            {"nombre": nombre, "resultado": resultado}
        )


# ============================================
# INSTANCIAR EL CONTROLADOR
# ============================================
# Creamos UNA SOLA instancia del controlador (patrón Singleton simplificado)
controlador = ControladorAmigos()


# ============================================
# RUTAS DE LA API (Endpoints)
# ============================================

@app.route('/', methods=['GET'])
def inicio():
    """
    Endpoint de información: muestra qué hace esta API.
    """
    return jsonify({
        "mensaje": "Bienvenido a la API de Creación de Amigos",
        "autor": "Juan",
        "version": "2.0 - POO Simplificada",
        "endpoints": {
            "1": "POST /amigo-regular - Crear amigo regular",
            "2": "POST /amigo-cercano - Crear amigo cercano",
            "3": "POST /amigo-regular/<nombre>/recuerdo - Agregar recuerdo a amigo regular",
            "4": "POST /amigo-cercano/<nombre>/recuerdo - Agregar recuerdo a amigo cercano"
        }
    }), 200

@app.route('/amigo-regular', methods=['POST'])
def crear_amigo_regular():
    """
    POST /amigo-regular - Crea un nuevo amigo regular.
    
    Ejemplo de Body JSON:
    {
        "nombre": "Carlos",
        "cumpleanos": "10/06/1995",
        "gustos": ["deportes", "musica"],
        "recuerdos": ["viaje a la playa"],
        "anecdotas": ["nos reimos mucho"]
    }
    """
    try:
        # Obtener los datos del JSON
        datos = request.get_json()
        
        # Delegar la lógica al controlador (POO)
        return controlador.crear_amigo_regular(datos)
        
    except Exception as e:
        # Manejo de errores inesperados
        return controlador.respuestas.error(f"Error interno: {str(e)}", 500)


@app.route('/amigo-cercano', methods=['POST'])
def crear_amigo_cercano():
    """
    POST /amigo-cercano - Crea un nuevo amigo cercano.
    
    Ejemplo de Body JSON:
    {
        "nombre": "Juan",
        "cumpleanos": "15/03/1995",
        "gustos": ["futbol", "musica"],
        "recuerdos": ["viaje a la playa", "concierto"],
        "anecdotas": ["anecdota 1", "anecdota 2"],
        "nivelConfianza": 8
    }
    """
    try:
        # Obtener los datos del JSON
        datos = request.get_json()
        
        # Delegar la lógica al controlador (POO)
        return controlador.crear_amigo_cercano(datos)
        
    except Exception as e:
        # Manejo de errores inesperados
        return controlador.respuestas.error(f"Error interno: {str(e)}", 500)


@app.route('/amigo-regular/<nombre>/recuerdo', methods=['POST'])
def agregar_recuerdo_regular(nombre):
    """
    POST /amigo-regular/<nombre>/recuerdo - Agrega recuerdo a amigo regular.
    
    Ejemplo de Body JSON:
    {
        "recuerdo": "Fuimos al cine"
    }
    """
    try:
        # Obtener los datos del JSON
        datos = request.get_json()
        recuerdo = datos.get('recuerdo') if datos else None
        
        # Delegar la lógica al controlador (POO)
        return controlador.agregar_recuerdo(nombre, recuerdo, "AmigoRegular")
        
    except Exception as e:
        # Manejo de errores inesperados
        return controlador.respuestas.error(f"Error interno: {str(e)}", 500)


@app.route('/amigo-cercano/<nombre>/recuerdo', methods=['POST'])
def agregar_recuerdo_cercano(nombre):
    """
    POST /amigo-cercano/<nombre>/recuerdo - Agrega recuerdo a amigo cercano.
    
    Ejemplo de Body JSON:
    {
        "recuerdo": "Fuimos al concierto"
    }
    """
    try:
        # Obtener los datos del JSON
        datos = request.get_json()
        recuerdo = datos.get('recuerdo') if datos else None
        
        # Delegar la lógica al controlador (POO)
        return controlador.agregar_recuerdo(nombre, recuerdo, "AmigoCercano")
        
    except Exception as e:
        # Manejo de errores inesperados
        return controlador.respuestas.error(f"Error interno: {str(e)}", 500)


if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*50)
    print("  API DE CREACIÓN - JUAN (POST)")
    print("="*50)
    print("Servidor corriendo en:")
    print(f"  Local:  http://127.0.0.1:5001")
    print(f"  Red:    http://{local_ip}:5001")
    print("\nEndpoints disponibles:")
    print("  POST /amigo-regular")
    print("  POST /amigo-cercano")
    print("  POST /amigo-regular/<nombre>/recuerdo")
    print("  POST /amigo-cercano/<nombre>/recuerdo")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)