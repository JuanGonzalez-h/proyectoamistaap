from Recuerdo import Recuerdo

class Amigo:

    def __init__(self, nombre, cumpleanos, gustos, recuerdos_lista):
        self.nombre = nombre
        self.cumpleanos = cumpleanos
        self.gustos = gustos
        self.recuerdos = Recuerdo(recuerdos_lista, 1)

    def obtenerNombre(self):
        return self.nombre
    
    def obtenerCumpleanos(self):
        return self.cumpleanos
    
    def agregarRecuerdo(self, nuevo_recuerdo):
        return self.recuerdos.agregarRecuerdo(nuevo_recuerdo)
    
    def obtenerInfo(self):
        return "Nombre: " + self.nombre
    
    def generarNotificacion(self):
        return "Notificación para " + self.nombre
