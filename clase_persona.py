class Persona:
    def __init__(self, codigo, nombre, sexo, correo, edad):
        self.codigo = codigo
        self.nombre = nombre
        self.sexo = sexo
        self.correo = correo
        self.edad = edad

    def get_codigo(self):
        return self.codigo

    def get_nombre(self):
        return self.nombre

    def get_sexo(self):
        return self.sexo

    def get_correo(self):
        return self.correo

    def get_edad(self):
        return self.edad

    def set_codigo(self, codigo):
        self.codigo = codigo

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_sexo(self, sexo):
        self.sexo = sexo

    def set_correo(self, correo):
        self.correo = correo

    def set_edad(self, edad):
        self.edad = edad

    def __str__(self):
        return f"ID: {self.codigo} | Nombre: {self.nombre} | Sexo: {self.sexo} | Correo: {self.correo} | Edad: {self.edad}"