from Amigo import Amigo
from Recuerdo import Recuerdo

class AmigoCercano(Amigo):

    def __init__(self, nombre, cumpleanos, gustos, recuerdos_lista, anecdotas, nivelConfianza):
        self.nombre = nombre
        self.cumpleanos = cumpleanos
        self.gustos = gustos
        self.recuerdos = Recuerdo(recuerdos_lista, 2)
        self.anecdotas = anecdotas
        self.nivelConfianza = nivelConfianza

    def agregarRecuerdo(self, nuevo_recuerdo):
        return self.recuerdos.agregarRecuerdo(nuevo_recuerdo)
    
    def obtenerInfo(self):
        info = "=== AMIGO CERCANO ===\n"
        info = info + "Nombre: " + self.nombre + "\n"
        info = info + "Cumpleaños: " + self.cumpleanos + "\n"

        gustos_texto = ""
        for i in range(len(self.gustos)):
            gustos_texto = gustos_texto + self.gustos[i]
            if i < len(self.gustos) - 1:
                gustos_texto = gustos_texto + ", "
        
        info = info + "Gustos: " + gustos_texto + "\n"
        info = info + "Nivel de Confianza: " + str(self.nivelConfianza) + "/10\n"
        info = info + "Anécdotas: " + str(len(self.anecdotas))
        return info
    
    def generarNotificacion(self):
        return "💙 Importante: Recordar contactar a " + self.nombre + " (Amigo Cercano)"
    
    def compararMomento(self):
        cantidad = str(self.recuerdos.contarRecuerdos())
        return "Momentos compartidos con " + self.nombre + ": " + cantidad
