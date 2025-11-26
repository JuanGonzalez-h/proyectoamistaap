class GestorAmigos:
    
    def __init__(self, amigos, manipulador):
        self.amigos = amigos
        self.manipulador = manipulador
    
    def agregarAmigo(self, amigo):
        self.amigos.append(amigo)
        print("✓ Amigo agregado: " + amigo.obtenerNombre())
        return amigo
    
    def buscarAmigo(self, nombre):
        for amigo in self.amigos:
            nombre_amigo = amigo.obtenerNombre()
            if nombre_amigo == nombre:
                return amigo
        return None
    
    def eliminarAmigo(self, nombre):
        amigo = self.buscarAmigo(nombre)
        if amigo:
            self.amigos.remove(amigo)
            print("✓ Amigo eliminado: " + nombre)
            return True
        else:
            print("✗ No se encontró el amigo: " + nombre)
            return False
    
    def obtenerAmigos(self):
        return self.amigos
    
    def contarAmigos(self):
        return len(self.amigos)
    
    def generarLista(self):
        if not self.amigos:
            return "No hay amigos registrados."
        
        lista = "\n" + "="*50 + "\n"
        lista = lista + "        LISTA DE AMIGOS\n"
        lista = lista + "="*50 + "\n\n"
        
        contador = 1
        for amigo in self.amigos:
            lista = lista + str(contador) + ". " + amigo.obtenerInfo() + "\n\n"
            contador = contador + 1
        
        return lista
    
    def generarNotificacion(self):
        if not self.amigos:
            return "No hay notificaciones."
        
        notificaciones = "\n" + "="*50 + "\n"
        notificaciones = notificaciones + "        NOTIFICACIONES\n"
        notificaciones = notificaciones + "="*50 + "\n\n"
        
        i = 0
        while i < len(self.amigos):
            amigo = self.amigos[i]
            notif = self.manipulador.formatearNotificacion(amigo)
            notificaciones = notificaciones + "• " + notif + "\n"
            i = i + 1
        
        return notificaciones
    
    def asignarManipulador(self, manipulador):
        self.manipulador = manipulador
        print("✓ Manipulador de texto actualizado")
