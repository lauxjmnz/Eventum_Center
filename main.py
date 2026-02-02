import planificador

print("Bienvenido a su organizador de eventos")
planificador.leer_datos()
 
def mostrar_menu():
    print("Menu")
    print("1.Crear evento")
    print("2.Mostrar evento")
    print("3.Editar evento")
    print("4.Eliminar evento")
    print("5.Ver en la agenda los recursos ocupados en los diferentes eventos")
    print("6.Salir")

while True:
    mostrar_menu()
    try:
        eleccion=int(input("elija una opcion"))
        if eleccion==1:
            planificador.crear_evento()
        elif eleccion==2:
            planificador.mostrar_evento()
        elif eleccion==3:
            planificador.editar_evento()
        elif eleccion==4:
            planificador.eliminar_evento()
        elif eleccion==5:
            planificador.ver_agenda_recursos()
        elif eleccion==6:
            print("Saliendo del programa...")
            break
        else:
            print("esa opcion no aparece")
    except ValueError:
        print("debe introducir un numero")    
        