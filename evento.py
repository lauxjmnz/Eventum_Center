from datetime import datetime ,timedelta

class Evento:
    def __init__(self,nombre,fecha, fecha_fin,hora_inicio,hora_fin,recursos):
        self.nombre=nombre
        self.fecha=fecha
        self.fecha_fin=fecha_fin
        self.hora_inicio=hora_inicio
        self.hora_fin=hora_fin
        self.recursos=recursos
        
    def inicio_datetime(self):
        return datetime.strptime(f"{self.fecha} {self.hora_inicio}", "%d/%m/%Y %H:%M")
    
    def fin_datetime(self):
        return datetime.strptime(f"{self.fecha_fin} {self.hora_fin}", "%d/%m/%Y %H:%M")
    
    def horas_solapadas(self,otro):
        return(self.inicio_datetime()< otro.fin_datetime() and otro.inicio_datetime()<self.fin_datetime())
    
    def to_dict(self):
        return{
            "nombre":self.nombre,
            "fecha": self.fecha,
            "fecha_fin":self.fecha_fin,
            "hora_inicio":self.hora_inicio,
            "hora_fin":self.hora_fin,
            "recursos":self.recursos
        }
    
    def copy(self):
        return Evento(
            self.nombre,
            self.fecha,
            self.fecha_fin,
            self.hora_inicio,
            self.hora_fin,
            list(self.recursos)
        )
    
    @staticmethod
    def from_dict(data):
        return Evento(
            data["nombre"],
            data["fecha"],
            data["fecha_fin"],
            data["hora_inicio"],
            data["hora_fin"],
            data["recursos"]
        )