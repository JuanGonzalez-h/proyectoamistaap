class ManipuladorTexto:

    def __init__(self, estiloFormal=True):
        """
        Constructor con estilo formal por defecto
        estiloFormal: Boolean que indica si el estilo es formal o informal
        """
        self.estiloFormal = estiloFormal

    def manipularTexto(self, texto):
        """Método para manipular texto genérico"""
        return texto

    def formatearNotificacion(self, amigo):
        """
        Formatea la notificación según el estilo definido
        amigo: Objeto de tipo Amigo
        """
        nombre = amigo.nombre
        if self.estiloFormal:
            return "Estimado usuario, le recordamos contactar a: " + nombre
        else:
            return "Hey! No olvides hablar con " + nombre + " 😊"
    
    def cambiarEstiloFormal(self, nuevo_estilo):
        """
        Cambia el estilo de las notificaciones
        nuevo_estilo: Boolean (True para formal, False para informal)
        """
        self.estiloFormal = nuevo_estilo
        if nuevo_estilo:
            return "Estilo cambiado a: Formal"
        else:
            return "Estilo cambiado a: Informal"
