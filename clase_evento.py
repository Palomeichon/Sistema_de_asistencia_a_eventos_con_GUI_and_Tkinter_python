class Evento:
    def __init__(self, id_evento, nombre_evento, fecha, hora, capacidad, ubicacion):
        self.__id_evento = id_evento
        self.__nombre_evento = nombre_evento
        self.__fecha = fecha
        self.__hora = hora  # Nuevo atributo para la hora
        self.__capacidad = capacidad
        self.__ubicacion = ubicacion

    # Getters
    def get_id_evento(self):
        return self.__id_evento

    def get_nombre_evento(self):
        return self.__nombre_evento

    def get_fecha(self):
        return self.__fecha

    def get_hora(self):  # Nuevo getter para la hora
        return self.__hora

    def get_capacidad(self):
        return self.__capacidad

    def get_ubicacion(self):
        return self.__ubicacion

    # Setters
    def set_id_evento(self, id_evento):
        self.__id_evento = id_evento

    def set_nombre_evento(self, nombre_evento):
        self.__nombre_evento = nombre_evento

    def set_fecha(self, fecha):
        self.__fecha = fecha

    def set_hora(self, hora):  # Nuevo setter para la hora
        self.__hora = hora

    def set_capacidad(self, capacidad):
        self.__capacidad = capacidad

    def set_ubicacion(self, ubicacion):
        self.__ubicacion = ubicacion

    # Método para mostrar información del evento
    def mostrar_info(self):
        return f"""
        ID: {self.__id_evento}
        Nombre: {self.__nombre_evento}
        Fecha: {self.__fecha}
        Hora: {self.__hora}
        Capacidad: {self.__capacidad}
        Ubicación: {self.__ubicacion}
        """
