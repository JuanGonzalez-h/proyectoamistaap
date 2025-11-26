"""
config.py - Configuración compartida para las APIs

Este archivo proporciona un gestor de amigos compartido que usa un archivo JSON
para persistir los datos. Esto permite que múltiples procesos Python (las dos APIs)
puedan compartir la misma información.

PROBLEMA ORIGINAL:
- Cada API corría en un proceso Python separado
- Cada proceso tenía su propio gestor en memoria (independientes)
- Los datos creados en una API no se veían en la otra

SOLUCIÓN:
- Usar un archivo JSON (amigos_data.json) como "base de datos"
- Ambas APIs leen y escriben en el mismo archivo
- Los datos persisten incluso si reinicias las APIs
"""

import json
import os
from GestorAmigos import GestorAmigos
from ManipuladorTexto import ManipuladorTexto
from AmigoRegular import AmigoRegular
from AmigoCercano import AmigoCercano

# Nombre del archivo donde se guardarán los datos
ARCHIVO_DATOS = "amigos_data.json"

# Crear el manipulador de texto (estilo formal por defecto)
manipulador = ManipuladorTexto(estiloFormal=True)

# Crear el gestor vacío inicialmente
gestor = GestorAmigos([], manipulador)


def guardar_datos():
    """
    Guarda todos los amigos del gestor en el archivo JSON.
    
    Convierte cada amigo a un diccionario con sus datos y lo guarda.
    Se llama automáticamente después de agregar o modificar amigos.
    """
    datos = []
    
    for amigo in gestor.amigos:
        # Obtener el tipo de amigo
        tipo = type(amigo).__name__
        
        # Crear diccionario con los datos básicos
        amigo_dict = {
            "tipo": tipo,
            "nombre": amigo.nombre,
            "cumpleanos": amigo.cumpleanos,
            "gustos": amigo.gustos,
            "recuerdos": amigo.recuerdos.recuerdos,  # Lista de recuerdos
            "anecdotas": amigo.anecdotas
        }
        
        # Si es amigo cercano, agregar nivel de confianza
        if tipo == "AmigoCercano":
            amigo_dict["nivelConfianza"] = amigo.nivelConfianza
        
        datos.append(amigo_dict)
    
    # Guardar en el archivo JSON
    with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)
    
    print(f"✓ Datos guardados en {ARCHIVO_DATOS}")


def cargar_datos():
    """
    Carga los amigos desde el archivo JSON al gestor.
    
    Lee el archivo, reconstruye los objetos Amigo y los agrega al gestor.
    Se llama automáticamente al iniciar cada API.
    """
    # Si el archivo no existe, no hay nada que cargar
    if not os.path.exists(ARCHIVO_DATOS):
        print(f"ℹ No existe {ARCHIVO_DATOS}, iniciando con gestor vacío")
        return
    
    try:
        # Leer el archivo JSON
        with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        
        # Limpiar el gestor actual
        gestor.amigos = []
        
        # Reconstruir cada amigo
        for amigo_dict in datos:
            tipo = amigo_dict["tipo"]
            nombre = amigo_dict["nombre"]
            cumpleanos = amigo_dict["cumpleanos"]
            gustos = amigo_dict["gustos"]
            recuerdos = amigo_dict["recuerdos"]
            anecdotas = amigo_dict["anecdotas"]
            
            # Crear el objeto según el tipo
            if tipo == "AmigoCercano":
                nivelConfianza = amigo_dict["nivelConfianza"]
                amigo = AmigoCercano(nombre, cumpleanos, gustos, [], anecdotas, nivelConfianza)
                # Restaurar los recuerdos manualmente
                amigo.recuerdos.recuerdos = recuerdos
            else:  # AmigoRegular
                amigo = AmigoRegular(nombre, cumpleanos, gustos, [], anecdotas)
                # Restaurar los recuerdos manualmente
                amigo.recuerdos.recuerdos = recuerdos
            
            # Agregar al gestor (sin imprimir mensaje)
            gestor.amigos.append(amigo)
        
        print(f"✓ Cargados {len(datos)} amigos desde {ARCHIVO_DATOS}")
        
    except Exception as e:
        print(f"✗ Error al cargar datos: {e}")


def obtener_gestor():
    """
    Retorna el gestor con los datos actualizados desde el archivo.
    
    IMPORTANTE: Llama a esta función al inicio de cada endpoint para
    asegurarte de tener los datos más recientes.
    
    Returns:
        GestorAmigos: El gestor con los datos cargados
    """
    cargar_datos()
    return gestor


# Cargar datos al importar este módulo
cargar_datos()
