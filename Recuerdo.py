class Recuerdo:
    
    def __init__(self, recuerdos, tipoRecuerdo):
        """
        Constructor de la clase Recuerdo
        recuerdos: Lista de strings con los recuerdos
        tipoRecuerdo: Entero que indica el tipo (1: Regular, 2: Cercano)
        """
        self.recuerdos = recuerdos if recuerdos else []
        self.tipoRecuerdo = tipoRecuerdo
    
    def obtenerRecuerdo(self):
        """Retorna todos los recuerdos como un string"""
        if not self.recuerdos:
            return "No hay recuerdos registrados"
        
        texto = ""
        for i in range(len(self.recuerdos)):
            texto = texto + "- " + self.recuerdos[i]
            if i < len(self.recuerdos) - 1:
                texto = texto + "\n"
        return texto
    
    def cambiarRecuerdo(self, indice, nuevo_recuerdo):
        """Cambia un recuerdo específico por índice"""
        if 0 <= indice < len(self.recuerdos):
            recuerdo_anterior = self.recuerdos[indice]
            self.recuerdos[indice] = nuevo_recuerdo
            return "Recuerdo modificado de '" + recuerdo_anterior + "' a '" + nuevo_recuerdo + "'"
        else:
            return "Índice inválido"
    
    def generarNotificacion(self):
        """Genera una notificación basada en la cantidad de recuerdos"""
        cantidad = len(self.recuerdos)
        if cantidad == 0:
            return "No hay recuerdos para notificar"
        elif cantidad < 3:
            return "Tienes " + str(cantidad) + " recuerdo(s) registrado(s)"
        else:
            return "¡Muchos recuerdos compartidos! Total: " + str(cantidad)
    
    def guardarNotificacion(self):
        """Guarda información de la notificación"""
        tipo_texto = "Regular" if self.tipoRecuerdo == 1 else "Cercano"
        return "Notificación guardada - Tipo: " + tipo_texto + ", Recuerdos: " + str(len(self.recuerdos))
    
    def agregarRecuerdo(self, nuevo_recuerdo):
        """Agrega un nuevo recuerdo a la lista"""
        prefijo = "[Regular] " if self.tipoRecuerdo == 1 else "[Cercano] "
        recuerdo_completo = prefijo + nuevo_recuerdo
        self.recuerdos.append(recuerdo_completo)
        return "Recuerdo agregado: " + nuevo_recuerdo
    
    def contarRecuerdos(self):
        """Retorna la cantidad de recuerdos"""
        return len(self.recuerdos)
