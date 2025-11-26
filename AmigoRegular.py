from Amigo import Amigo
from Recuerdo import Recuerdo

class AmigoRegular(Amigo):
    
    def __init__(self, nombre, cumpleanos, gustos, recuerdos_lista, anecdotas):
        self.nombre = nombre
        self.cumpleanos = cumpleanos
        self.gustos = gustos
        self.recuerdos = Recuerdo(recuerdos_lista, 1)
        self.anecdotas = anecdotas
    
    def agregarRecuerdo(self, nuevo_recuerdo):
        return self.recuerdos.agregarRecuerdo(nuevo_recuerdo)
    
    def obtenerInfo(self):
        info = "=== AMIGO REGULAR ===\n"
        info = info + "Nombre: " + self.nombre + "\n"
        info = info + "Cumpleaños: " + self.cumpleanos + "\n"
        
        gustos_texto = ""
        for i in range(len(self.gustos)):
            gustos_texto = gustos_texto + self.gustos[i]
            if i < len(self.gustos) - 1:
                gustos_texto = gustos_texto + ", "
        
        info = info + "Gustos: " + gustos_texto + "\n"
        info = info + "Anécdotas: " + str(len(self.anecdotas))
        return info
    
    def generarNotificacion(self):
        return "📢 Recordatorio: Contactar a " + self.nombre + " (Amigo Regular)"
