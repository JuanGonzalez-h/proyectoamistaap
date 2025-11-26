from Amigo import Amigo
from AmigoRegular import AmigoRegular
from AmigoCercano import AmigoCercano
from ManipuladorTexto import ManipuladorTexto
from GestorAmigos import GestorAmigos


def mostrar_menu():
    print("\n" + "="*50)
    print("    SISTEMA DE GESTIÓN DE AMIGOS")
    print("="*50)
    print("1. Agregar Amigo Regular")
    print("2. Agregar Amigo Cercano")
    print("3. Ver todos los amigos")
    print("4. Buscar amigo")
    print("5. Generar notificaciones")
    print("6. Agregar recuerdo a un amigo")
    print("7. Eliminar amigo")
    print("8. Cambiar estilo de notificaciones (Formal/Informal)")
    print("9. Salir")
    print("="*50)


def obtener_lista(mensaje):
    print(mensaje)
    print("(Ingrese los elementos separados por coma)")
    entrada = input("➤ ")
    
    elementos = []
    elemento_actual = ""
    
    for caracter in entrada:
        if caracter == ",":
            if elemento_actual:
                elementos.append(elemento_actual.strip())
            elemento_actual = ""
        else:
            elemento_actual = elemento_actual + caracter
    
    if elemento_actual:
        elementos.append(elemento_actual.strip())
    
    return elementos


def agregar_amigo_regular(gestor):
    print("\n--- AGREGAR AMIGO REGULAR ---")
    nombre = input("Nombre: ")
    cumpleanos = input("Cumpleaños (ej: 15/03/1995): ")
    gustos = obtener_lista("Gustos del amigo:")
    recuerdos = obtener_lista("Recuerdos compartidos:")
    anecdotas = obtener_lista("Anécdotas:")
    
    nuevo_amigo = AmigoRegular(nombre, cumpleanos, gustos, recuerdos, anecdotas)
    gestor.agregarAmigo(nuevo_amigo)


def agregar_amigo_cercano(gestor):
    print("\n--- AGREGAR AMIGO CERCANO ---")
    nombre = input("Nombre: ")
    cumpleanos = input("Cumpleaños (ej: 15/03/1995): ")
    gustos = obtener_lista("Gustos del amigo:")
    recuerdos = obtener_lista("Recuerdos compartidos:")
    anecdotas = obtener_lista("Anécdotas:")
    
    while True:
        try:
            nivelConfianza = int(input("Nivel de confianza (1-10): "))
            if 1 <= nivelConfianza and nivelConfianza <= 10:
                break
            else:
                print("Por favor ingrese un número entre 1 y 10")
        except ValueError:
            print("Por favor ingrese un número válido")
    
    nuevo_amigo = AmigoCercano(nombre, cumpleanos, gustos, recuerdos, anecdotas, nivelConfianza)
    gestor.agregarAmigo(nuevo_amigo)


def buscar_y_mostrar_amigo(gestor):
    nombre = input("\nIngrese el nombre del amigo a buscar: ")
    amigo = gestor.buscarAmigo(nombre)
    
    if amigo:
        print("\n✓ Amigo encontrado:")
        print(amigo.obtenerInfo())
    else:
        print("\n✗ No se encontró ningún amigo con el nombre: " + nombre)


def agregar_recuerdo_amigo(gestor):
    nombre = input("\nIngrese el nombre del amigo: ")
    amigo = gestor.buscarAmigo(nombre)
    
    if amigo:
        nuevo_recuerdo = input("Ingrese el recuerdo: ")
        resultado = amigo.agregarRecuerdo(nuevo_recuerdo)
        print("✓ " + resultado)
    else:
        print("\n✗ No se encontró ningún amigo con el nombre: " + nombre)


def cambiar_estilo_notificaciones(gestor):
    print("\n--- CAMBIAR ESTILO DE NOTIFICACIONES ---")
    print("1. Formal")
    print("2. Informal")
    opcion = input("Seleccione el estilo: ")
    
    if opcion == "1":
        nuevo_manipulador = ManipuladorTexto(estiloFormal=True)
        gestor.asignarManipulador(nuevo_manipulador)
        print("✓ Estilo cambiado a: FORMAL")
    elif opcion == "2":
        nuevo_manipulador = ManipuladorTexto(estiloFormal=False)
        gestor.asignarManipulador(nuevo_manipulador)
        print("✓ Estilo cambiado a: INFORMAL")
    else:
        print("✗ Opción no válida")


def main():
    print("\n╔═══════════════════════════════════════════════╗")
    print("║   BIENVENIDO AL GESTOR DE AMIGOS              ║")
    print("╚═══════════════════════════════════════════════╝")
    
    manipulador = ManipuladorTexto(estiloFormal=True)
    gestor = GestorAmigos([], manipulador)
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            agregar_amigo_regular(gestor)
            
        elif opcion == "2":
            agregar_amigo_cercano(gestor)
            
        elif opcion == "3":
            print(gestor.generarLista())
            print("\nTotal de amigos: " + str(gestor.contarAmigos()))
            
        elif opcion == "4":
            buscar_y_mostrar_amigo(gestor)
            
        elif opcion == "5":
            print(gestor.generarNotificacion())
            
        elif opcion == "6":
            agregar_recuerdo_amigo(gestor)
            
        elif opcion == "7":
            nombre = input("\nIngrese el nombre del amigo a eliminar: ")
            gestor.eliminarAmigo(nombre)
            
        elif opcion == "8":
            cambiar_estilo_notificaciones(gestor)
            
        elif opcion == "9":
            print("\n¡Hasta pronto! 👋")
            break
            
        else:
            print("\n✗ Opción no válida. Por favor intente de nuevo.")
        
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()      
