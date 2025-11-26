"""
AmigoRegular_APIlaura.py - API de Laura (GET - CONSULTAR)

Esta API permite CONSULTAR información de amigos usando el método GET.
Usa programación orientada a objetos para manejar las consultas.

Autor: Laura
Versión: 2.0 - Simplificada con POO
"""

from flask import Flask, request, jsonify
from config import obtener_gestor

# Crear la aplicación Flask
app = Flask(__name__)


# ============================================
# CLASE AUXILIAR: FormateadorDatos
# ============================================
class FormateadorDatos:
    """
    Clase que formatea los datos de los amigos para enviarlos como JSON.
    
    Responsabilidad: Convertir objetos Python a diccionarios serializables.
    """
    
    @staticmethod
    def amigo_a_diccionario(amigo):
        """
        Convierte un objeto Amigo a un diccionario JSON-serializable.
        
        Args:
            amigo: Objeto AmigoRegular o AmigoCercano
        
        Returns:
            dict: Diccionario con los datos del amigo
        """
        # Datos básicos que tienen todos los amigos
        datos = {
            "nombre": amigo.nombre,
            "cumpleanos": amigo.cumpleanos,
            "gustos": amigo.gustos,
            # Convertir el objeto Recuerdo a lista de strings
            "recuerdos": amigo.recuerdos.recuerdos,
            "anecdotas": amigo.anecdotas
        }
        
        # Determinar el tipo de amigo
        nombre_clase = type(amigo).__name__
        
        if nombre_clase == "AmigoCercano":
            datos["tipo"] = "Amigo Cercano"
            datos["nivelConfianza"] = amigo.nivelConfianza
        else:
            datos["tipo"] = "Amigo Regular"
        
        return datos
    
    @staticmethod
    def amigo_detallado(amigo):
        """
        Convierte un amigo a diccionario con información detallada.
        
        Args:
            amigo: Objeto AmigoRegular o AmigoCercano
        
        Returns:
            dict: Diccionario con datos detallados del amigo
        """
        datos = FormateadorDatos.amigo_a_diccionario(amigo)
        
        # Agregar información adicional
        datos["tipo_clase"] = type(amigo).__name__
        datos["informacion"] = amigo.obtenerInfo()
        
        return datos


# ============================================
# CLASE AUXILIAR: BuscadorAmigos
# ============================================
class BuscadorAmigos:
    """
    Clase que maneja la búsqueda de amigos en el gestor.
    
    Responsabilidad: Buscar y filtrar amigos.
    """
    
    @staticmethod
    def buscar_por_nombre(gestor, nombre):
        """
        Busca un amigo por nombre usando un ciclo while.
        
        Args:
            gestor: GestorAmigos con la lista de amigos
            nombre (str): Nombre del amigo a buscar
        
        Returns:
            Amigo o None: El amigo encontrado o None si no existe
        """
        amigo_encontrado = None
        indice = 0
        
        # Recorrer la lista con while (requisito académico)
        while indice < len(gestor.amigos):
            amigo_actual = gestor.amigos[indice]
            
            if amigo_actual.obtenerNombre() == nombre:
                amigo_encontrado = amigo_actual
                break
            
            indice = indice + 1
        
        return amigo_encontrado


# ============================================
# CLASE PRINCIPAL: ControladorConsultas
# ============================================
class ControladorConsultas:
    """
    Controlador que maneja todas las consultas (GET) de la API.
    
    Esta clase encapsula la lógica de negocio para consultar amigos.
    """
    
    def __init__(self):
        """Constructor: inicializa las dependencias"""
        self.formateador = FormateadorDatos()
        self.buscador = BuscadorAmigos()
    
    def obtener_todos_los_amigos(self):
        """
        Obtiene la lista completa de amigos.
        
        Returns:
            tuple: (respuesta_json, codigo_http)
        """
        # Obtener el gestor con datos actualizados
        gestor = obtener_gestor()
        
        # Verificar si hay amigos
        if len(gestor.amigos) == 0:
            return jsonify({
                "mensaje": "No hay amigos registrados",
                "total": 0,
                "amigos": []
            }), 200
        
        # Convertir cada amigo a diccionario usando while
        lista_de_amigos = []
        indice = 0
        
        while indice < len(gestor.amigos):
            amigo_actual = gestor.amigos[indice]
            
            # Usar el formateador para convertir el amigo
            datos_amigo = self.formateador.amigo_a_diccionario(amigo_actual)
            lista_de_amigos.append(datos_amigo)
            
            indice = indice + 1
        
        # Retornar respuesta
        return jsonify({
            "exito": True,
            "total": len(gestor.amigos),
            "amigos": lista_de_amigos
        }), 200
    
    def buscar_amigo_por_nombre(self, nombre):
        """
        Busca un amigo específico por nombre.
        
        Args:
            nombre (str): Nombre del amigo a buscar
        
        Returns:
            tuple: (respuesta_json, codigo_http)
        """
        # Obtener el gestor con datos actualizados
        gestor = obtener_gestor()
        
        # Buscar el amigo usando la clase BuscadorAmigos
        amigo_encontrado = self.buscador.buscar_por_nombre(gestor, nombre)
        
        # Verificar si se encontró
        if amigo_encontrado is None:
            return jsonify({
                "error": "No se encontró el amigo",
                "mensaje": f"No existe un amigo con el nombre: {nombre}"
            }), 404
        
        # Formatear los datos del amigo encontrado
        datos = self.formateador.amigo_detallado(amigo_encontrado)
        datos["exito"] = True
        
        return jsonify(datos), 200
    
    def obtener_estadisticas(self):
        """
        Calcula estadísticas sobre los amigos registrados.
        
        Returns:
            tuple: (respuesta_json, codigo_http)
        """
        # Obtener el gestor con datos actualizados
        gestor = obtener_gestor()
        
        total = len(gestor.amigos)
        cantidad_regulares = 0
        cantidad_cercanos = 0
        
        # Contar por tipo usando while
        indice = 0
        while indice < total:
            amigo = gestor.amigos[indice]
            nombre_clase = type(amigo).__name__
            
            if nombre_clase == "AmigoCercano":
                cantidad_cercanos = cantidad_cercanos + 1
            else:
                cantidad_regulares = cantidad_regulares + 1
            
            indice = indice + 1
        
        # Retornar estadísticas
        return jsonify({
            "exito": True,
            "total_amigos": total,
            "amigos_regulares": cantidad_regulares,
            "amigos_cercanos": cantidad_cercanos
        }), 200


# ============================================
# INSTANCIAR EL CONTROLADOR
# ============================================
# Creamos UNA SOLA instancia del controlador (patrón Singleton simplificado)
controlador = ControladorConsultas()


# ============================================
# RUTAS DE LA API (Endpoints)
# ============================================

@app.route('/', methods=['GET'])
def inicio():
    """
    Endpoint de información: muestra qué hace esta API.
    """
    return jsonify({
        "mensaje": "Bienvenido a la API de Gestión de Amigos",
        "autor": "Laura",
        "version": "2.0 - POO Simplificada",
        "endpoints": {
            "1": "GET / - Información",
            "2": "GET /amigos - Ver todos los amigos",
            "3": "GET /amigos?nombre=NombreAmigo - Buscar un amigo",
            "4": "GET /estadisticas - Ver estadísticas"
        }
    }), 200


@app.route('/amigos', methods=['GET'])
def obtener_amigos():
    """
    GET /amigos - Obtiene todos los amigos o busca uno por nombre.
    
    Parámetro opcional: ?nombre=Juan
    
    Ejemplos:
        GET /amigos              → Lista todos los amigos
        GET /amigos?nombre=Juan  → Busca a Juan específicamente
    """
    try:
        # Obtener el parámetro de búsqueda (si existe)
        nombre_a_buscar = request.args.get('nombre')
        
        # Decidir qué hacer según si hay parámetro o no
        if nombre_a_buscar:
            # Buscar un amigo específico
            return controlador.buscar_amigo_por_nombre(nombre_a_buscar)
        else:
            # Obtener todos los amigos
            return controlador.obtener_todos_los_amigos()
    
    except Exception as e:
        # Manejo de errores inesperados
        return jsonify({
            "exito": False,
            "error": f"Error interno: {str(e)}"
        }), 500


@app.route('/estadisticas', methods=['GET'])
def ver_estadisticas():
    """
    GET /estadisticas - Obtiene estadísticas de los amigos.
    
    Calcula y retorna:
    - Total de amigos
    - Cantidad de amigos regulares
    - Cantidad de amigos cercanos
    """
    try:
        # Delegar la lógica al controlador (POO)
        return controlador.obtener_estadisticas()
    
    except Exception as e:
        # Manejo de errores inesperados
        return jsonify({
            "exito": False,
            "error": f"Error interno: {str(e)}"
        }), 500


if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*50)
    print("  API DE CONSULTAS - LAURA (GET)")
    print("="*50)
    print("Servidor corriendo en:")
    print(f"  Local:  http://127.0.0.1:5000")
    print(f"  Red:    http://{local_ip}:5000")
    print("\nEndpoints disponibles:")
    print("  GET /")
    print("  GET /amigos")
    print("  GET /amigos?nombre=Juan")
    print("  GET /estadisticas")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)