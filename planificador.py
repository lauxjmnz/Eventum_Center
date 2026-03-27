from recursos import RECURSOS_DISPONIBLES
import json
from datetime import datetime,timedelta
from evento import Evento

class Planificador:
    def __init__(self):
        self.eventos=[]
        self.leer_datos()

    def pedir_nombre(self):
        while True:
            nombre=input("Introduzca el nombre del evento:").strip()
            if not nombre:
                print("Error:El nombre no puede estar vacio ")
                continue
            return nombre
    def leer_datos(self):
        try:
            with open("data.json","r",encoding="utf-8")as archivo:            
                contenido=archivo.read().strip()
                if not contenido:
                    self.eventos=[]
                    return
                datos=json.loads(contenido)
                if isinstance(datos,dict):
                    self.eventos= [ Evento.from_dict(e) for e in datos.get("eventos", [])]
                else:
                    print("Aviso:El formato del archivo data.json no es valido .Se iniciara vacio")
                    self.eventos =[]
        except FileNotFoundError:
            self.eventos=[]
        except json.JSONDecodeError:
            self.eventos=[]
            self.guardar_eventos()

    def guardar_eventos(self):
        datos={"eventos": [e.to_dict() for e in self.eventos]}
        with open("data.json","w",encoding="utf-8") as archivo:
            json.dump(datos,archivo,indent=4,ensure_ascii=False)

    #fechas en datetime
    def pedir_fecha(self):
        while True:
            fecha_texto=input("introduzca fecha en el formato(DD/MM/AAAA)")
            if not fecha_texto:
                print("La fecha no puede estar vacia")
                continue
            try:
                fecha=datetime.strptime(fecha_texto, "%d/%m/%Y")
                hoy= datetime.now()
                if fecha.date()<hoy.date():
                     print("no se permiten fechas pasadas")
                     continue
                return fecha_texto
            except ValueError:
                 print("El formato es incorrecto.Use DD/MM/AAAA")
            
    def pedir_hora(self):
        while True:
            hora_texto=input("introduzca la hora en el formato siguiente (HH:MM)")
            try:
                datetime.strptime(hora_texto,"%H:%M")
                return hora_texto
            except ValueError:
                print("El formato es incorrecto.Use HH:MM")

    def comprobar_madrugada(self,hora_inicio,hora_fin):
        inicio=datetime.strptime(hora_inicio, "%H:%M")
        fin=datetime.strptime(hora_fin, "%H:%M")

        if inicio==fin:
            print("Aviso :Ha introducido la misma hora de inicio y de fin")
            print("Esto creara un evento de 24 horas  ")
        return fin<=inicio
    
    def obtener_recurso(self,nombre):
        for recurso in RECURSOS_DISPONIBLES:
            if recurso["nombre"]==nombre:
                return recurso
        return None

    def validar_requiere(self,Recursos_seleccionados):
        for r in Recursos_seleccionados:
            recurso=self.obtener_recurso(r)
            requeridos =recurso["requiere"]

            for req in requeridos:
                if req not in Recursos_seleccionados:
                    print(f"El recurso '{r}' requiere '{req}' ")
                    return False
        return True

    def validar_excluye(self,Recursos_seleccionados):
        for r in Recursos_seleccionados:
            recurso=self.obtener_recurso(r)
            excluidos=recurso["excluye"]

            for ex in excluidos:
                if ex in Recursos_seleccionados:
                    print(f"El recurso'{r}' no puede usarse junto con '{ex}' ")
                    return False
        return True

    def pedir_recurso(self):
        seleccionados=[]

        while True:
            print("RECURSOS DISPONIBLES ")
            for i,recurso in enumerate(RECURSOS_DISPONIBLES,start=1):
                print(f"{i}. {recurso['nombre']}")

            opcion=input("Introduzca el numero del recurso que deseaa añadir (en caso de no querer añadir mas recursos pulse 'ENTER')")

            if opcion=="":
                break
            try:
                opcion=int(opcion)
            
                if opcion<1 or opcion>len(RECURSOS_DISPONIBLES):
                    print("Opcion fuera de rango")
                    continue

                recurso_elegido=RECURSOS_DISPONIBLES[opcion - 1]["nombre"]

                if recurso_elegido in seleccionados:
                    print("Ese recurso ya fue añadido")
                    continue
  
                seleccionados.append(recurso_elegido)
                print(f"El recurso '{recurso_elegido}' fue añadido")
            except ValueError:
                print("Debe introducir un numero")
                continue

        
        return seleccionados

    def recursos_ocupados(self,evento_nuevo,indice_actual=None):
        ocupados=set()
        for i,evento in enumerate(self.eventos):
            if indice_actual is not None and i ==indice_actual:
                continue

            recursos_comunes=set(evento.recursos) & set(evento_nuevo.recursos)
            if recursos_comunes:
                if evento.horas_solapadas(evento_nuevo):
                   ocupados.update(recursos_comunes)
        return list(ocupados) 

    def ver_agenda_recursos(self):
        if not self.eventos:
            print("No hay eventos guardados para buscar")
            return
        else:
            print("RECURSOS DISPONIBLES ")
            for i,recurso in enumerate(RECURSOS_DISPONIBLES,start=1):
                print(f"{i}. {recurso['nombre']}")
            try:
                opcion=input("Introduzca el numero del recurso que quisiera ver en la agenda")
                if not opcion:
                    return
        
                opcion=int(opcion)
            
                if 1<=opcion<=len(RECURSOS_DISPONIBLES):
                    recurso_elegido=RECURSOS_DISPONIBLES[opcion - 1]['nombre']

                    print(f"Agenda para {recurso_elegido} ")

                    encontrado=False
                    for e in self.eventos:
                        if recurso_elegido in e.recursos:
                            encontrado=True
                            print(f"Evento: {e.nombre}")
                            if e.fecha==e.fecha_fin:
                                print(f"Dia: {e.fecha} de {e.hora_inicio} a {e.hora_fin}")
                            else:
                                print(f"Desde:{e.fecha} de {e.hora_inicio} hasta {e.fecha_fin} {e.hora_fin}")
                    

                    if not encontrado:
                        print(f"No hay eventos programados para {recurso_elegido}")

                else:
                    print("Numero fuera del rango")

            except ValueError:
                print("Debe introducir un numero ")
            

    def buscar_huecos(self,evento_fallido):
        print("Buscando un espacio libre para estos recursos...")
        try:
            inicio_dt=datetime.strptime(f"{evento_fallido.fecha} {evento_fallido.hora_inicio}", "%d/%m/%Y %H:%M")
            fin_dt=datetime.strptime(f"{evento_fallido.fecha_fin} {evento_fallido.hora_fin}", "%d/%m/%Y %H:%M")
            duracion=fin_dt-inicio_dt

            for i in range(96):
                inicio_dt+=timedelta(minutes=30)
                nuevo_fin_dt=inicio_dt+duracion

                evento_prueba=evento_fallido.copy()
                evento_prueba.fecha=inicio_dt.strftime("%d/%m/%Y")
                evento_prueba.hora_inicio=inicio_dt.strftime("%H:%M")
                evento_prueba.fecha_fin=nuevo_fin_dt.strftime("%d/%m/%Y")
                evento_prueba.hora_fin=nuevo_fin_dt.strftime("%H:%M")

                if not self.recursos_ocupados(evento_prueba):
                    print("Encontramos un hueco.Podrias mover el evento al:")
                    print(f"{evento_prueba.fecha} de {evento_prueba.hora_inicio} al {evento_prueba.hora_fin}")
                    return
            print("No se encontro ningun hueco libre en las proximas 48 horas")
        except Exception as e:
            print(f"Error tecnico en la busqueda de {e}")

          
    def crear_evento(self):
        nombre=self.pedir_nombre()
        fecha=self.pedir_fecha()

        while True:
            print("Introduzca la hora de inicio")
            hora_inicio =self.pedir_hora()

            hoy=datetime.now()
            inicio_dt=datetime.strptime(f"{fecha} {hora_inicio}", "%d/%m/%Y %H:%M")
            if inicio_dt< hoy:
                print("Error :No puedes programar un evento para una hora que ya paso")
                continue

            print("Introduzca la hora en que culmina el evento")
            hora_fin =self.pedir_hora()
        
            fecha_f=fecha
            if self.comprobar_madrugada(hora_inicio,hora_fin):
                obj_f=datetime.strptime(fecha,"%d/%m/%Y")
                fecha_f=(obj_f+timedelta(days=1)).strftime("%d/%m/%Y")
                print(f"Fue detectado un evento de madrugada .El evento termina el {fecha_f}")
            break

        recursos =self.pedir_recurso()
     
        if not recursos:
            print("Atencion no has seleccionado ningun recurso")
            while True: 
                confirmar=input("Desea crear este evento solo como una anotacion en la agenda (si/no)").lower().strip()
                if confirmar=="si":
                    break
                elif confirmar=="no":
                    print("Operacion cancelada.El evento no ha sido guardado")
                    return
                else:
                     print("Por favor responda con 'si' o 'no' ")
            
        evento=Evento(
            nombre,
            fecha,
            fecha_f,
            hora_inicio,
            hora_fin,
            recursos
        )
            

        if not self.validar_requiere(recursos):
            print("Error en los recursos seleccionados(requiere)")
            return
        if not self.validar_excluye(recursos):
            print("Error en los recursos seleccionados(excluye)")
            return
        ocupados=self.recursos_ocupados(evento)
        if ocupados:
            print("No se puede crear el evento")
            print("Recursos ocupados en ese horario:")
            for r in ocupados:
                print("-", r)

            self.buscar_huecos(evento)
            return
        self.eventos.append(evento)
        self.guardar_eventos()
        print("Su evento se ha creado correctamente")



    def mostrar_evento(self):
        if not self.eventos:
            print("no hay eventos registrados")
            return
        else:
            for i,evento in enumerate(self.eventos,start=1):
                print(f"\n {i} {evento.nombre}")
                if evento.fecha !=evento.fecha_fin:
                    print(f"fecha:{evento.fecha} al {evento.fecha_fin}")
                else:
                    print(f"fecha:{evento.fecha}")

                print(f"hora:{evento.hora_inicio}-{evento.hora_fin}")
                if not evento.recursos:
                    print("recursos:(ninguno)")
                else:
                    print("Recursos")
                    for recurso in evento.recursos:
                       print(f"-{recurso}")


    def editar_evento(self):
        if not self.eventos:                     #hay eventos o no
            print("no hay eventos para editar")
            return
        else:
            print("Eventos disponibles")                         #mostrar eventos
            for i,evento in enumerate(self.eventos,start=1):          
                print(f"{i}. {evento.nombre} {evento.fecha} {evento.hora_inicio}- {evento.fecha_fin}{evento.hora_fin}")
                         
            try:                                                  #elegir evento
                opcion=int(input("elija el numero del evento a editar"))-1
                if opcion<0 or opcion>=len(self.eventos):
                    print("numero fuera del rango")
                    return
            except ValueError:
                print("debes escribir un numero")
                return

            evento_elegido=self.eventos[opcion]                             #trabajar con evento elegido
        
            while True:                                               #trabajar con menu interno de que editar en el evento elegido
                print("\n ¿Que desea editar?")
                print("1.Nombre")
                print(" 2.Fecha")
                print("3.Hora(inicio y fin)")
                print("4.Recursos")
                print("5.Guardar y salir")
            
                indice=input("Seleccione una opcion")
                if indice=="1":
                    nuevo_nombre=self.pedir_nombre()
                    if nuevo_nombre:
                        evento_elegido.nombre=nuevo_nombre
                        print("Nombre actualizado")
                    else:
                        print("El nombre no puede estar vacio")
                elif indice=="2":
                    nueva_fecha=self.pedir_fecha()
                    evento_prueba=evento_elegido.copy()
                    evento_prueba.fecha=nueva_fecha

                    if self.comprobar_madrugada(evento_prueba.hora_inicio,evento_prueba.hora_fin):
                        obj_fecha=datetime.strptime(nueva_fecha, "%d/%m/%Y")
                        evento_prueba.fecha_fin=(obj_fecha +timedelta(days=1)).strftime("%d/%m/%Y")
                    else:
                        evento_prueba.fecha_fin=nueva_fecha
                    ocupados=self.recursos_ocupados(evento_prueba,opcion)
                    if ocupados:
                        print("No se puede cambiar la fecha.Recursos ocupados:")
                        for r in ocupados:
                            print("-", r)
                        continue
                    evento_elegido.fecha=evento_prueba.fecha
                    evento_elegido.fecha_fin=evento_prueba.fecha_fin
                    print("Fecha actualizada correctamente")
                elif indice=="3":
                    print("Introduzca a continuacion la hora de inicio:")
                    nueva_inicio=self.pedir_hora()
                    
                    hoy=datetime.now()
                    inicio_dt=datetime.strptime(f"{evento_elegido.fecha} {nueva_inicio}", "%d/%m/%Y %H:%M")
                    if inicio_dt<hoy:
                        print("Error :La hora ya paso para el dia de hoy")
                        continue

                    print("Introduzca la hora en que culmina el evento:")
                    nueva_fin=self.pedir_hora()

                    nueva_fecha_f=evento_elegido.fecha
                    if self.comprobar_madrugada(nueva_inicio,nueva_fin):
                        obj_f=datetime.strptime(evento_elegido.fecha ,"%d/%m/%Y")
                        nueva_fecha_f=(obj_f+ timedelta(days=1)).strftime("%d/%m/%Y")

                    evento_temp=evento_elegido.copy()
                    evento_temp.hora_inicio=nueva_inicio
                    evento_temp.hora_fin=nueva_fin
                    evento_temp.fecha_fin=nueva_fecha_f

                    ocupados=self.recursos_ocupados(evento_temp,opcion)
                    if ocupados:
                        print("Nose puede editar el evento.")
                        print("Recursos ocupados en ese horario:")
                        for r in ocupados:
                            print("-", r)

                        self.buscar_huecos(evento_temp)
                        continue

                    evento_elegido.hora_inicio=nueva_inicio
                    evento_elegido.hora_fin=nueva_fin 
                    evento_elegido.fecha_fin=nueva_fecha_f
                
                    print("Horario actualizado  con exito")

                elif indice=="4":
                    if evento_elegido.recursos:
                        for i, r in enumerate(evento_elegido.recursos,start=1):
                            print(f"{i}. {r}")
                    else:
                        print("Este evento no tiene recursos")
                
                    opcion_agregar=len(evento_elegido.recursos)+1
                    opcion_volver=len(evento_elegido.recursos)+2

                    print("OTRAS OPCIONES ")
                    print(f"{opcion_agregar}.Agregar recursos")
                    print(f"{opcion_volver} .Volver")

                    print("Toque algun recurso si desea eliminarlo y en caso de querer añadir uno nuevo toque'agregar recurso' ")

                    while True:
                        opcion2=input("Seleccione una opcion:")
                        try:
                            opcion2=int(opcion2)
                            break
                        except ValueError:
                            print("Debe introducir un numero valido")
                            continue

                    if evento_elegido.recursos:
                        if opcion2>=1 and opcion2<=len(evento_elegido.recursos):             #eliminar recursos si  hay
                            recursos_temp=evento_elegido.recursos.copy()
                            r_eliminado=recursos_temp.pop(opcion2 -1)
                            if not self.validar_requiere(recursos_temp):
                                print("Opcion denegada .No puedes eliminar {r_eliminado} porque otro recurso depende de el")
                            else:
                                evento_elegido.recursos=recursos_temp
                                self.guardar_eventos()
                                print(f"El recurso {r_eliminado} fue eliminado correctamente")
                
                
                        elif opcion2==len(evento_elegido.recursos)+1:                #agregar recursos
                            recursos_nuevos=self.pedir_recurso()
                            
                            if recursos_nuevos:
                                recursos_combinados=list(evento_elegido.recursos)+ recursos_nuevos
                            if recursos_nuevos:
                                if not self.validar_requiere(recursos_combinados):
                                    continue
                                if not self.validar_excluye(recursos_combinados):
                                    continue

                                evento_prueba=evento_elegido.copy()
                                evento_prueba.recursos=recursos_combinados

                                ocupados=self.recursos_ocupados(evento_prueba,opcion)
                                if ocupados:
                                    print("No se pueden agregar los recursos")
                                    print("Recursos ocupados en ese horario:")
                                    for r in ocupados:
                                        print("-", r)
                                    continue
                                else:
                                    evento_elegido.recursos.extend(recursos_nuevos)
                                    evento_elegido.recursos=list(set(evento_elegido.recursos))  #eliminar duplicados
                                    print("Recursos agregados correctamente")

                        elif opcion2==len(evento_elegido.recursos)+2:                #volver
                           continue
           
                        else:
                            print("Opcion no valida")
                    else:
                        if opcion2==opcion_agregar:
                            recursos_nuevos=self.pedir_recurso()

                            if recursos_nuevos:
                                if not self.validar_requiere(recursos_nuevos):
                                    continue
                                if not self.validar_excluye(recursos_nuevos):
                                    continue

                                evento_prueba=evento_elegido.copy()
                                evento_prueba.recursos=evento_elegido.recursos+ recursos_nuevos

                                ocupados=self.recursos_ocupados(evento_prueba,opcion)
                                if ocupados:
                                    print("No se pueden agregar los recursos")
                                    print("Recursos ocupados en ese horario:")
                                    for r in ocupados:
                                        print("-", r)
                                    continue
                            
                                else:
                                    evento_elegido.recursos.extend(recursos_nuevos)
                                    evento_elegido.recursos=list(set(evento_elegido.recursos))
                                    print("Recursos agregados correctamente")  
                         
                        elif opcion2==opcion_volver:
                            break
                        else:
                            print("Opcion no valida")

                elif indice=="5":
                    self.guardar_eventos()
                    print("Su evento se ha editado correctamente")
                    break

                else:
                    print("Opcion no valida")
        
            
    def eliminar_evento(self):
        if not self.eventos:
            print("no hay eventos para poder eliminar")
            return  
        else:
            print("Eventos disponibles")
            for i,evento in enumerate(self.eventos,start=1):
                print(f"{i}. {evento.nombre}")
            while True:
                try:
                    opcion_evento=int(input("introduzca el numero del evento que desea eliminar"))
                    if opcion_evento<1 or opcion_evento>len(self.eventos):
                        print("numero fuera del rango")
                    else:
                        break
                except ValueError:
                    print("tiene que introducir un numero")
                
            evento_eliminado=self.eventos.pop(opcion_evento-1)
            self.guardar_eventos()
            print(f"Evento {evento_eliminado.nombre} fue eliminado correctamente")