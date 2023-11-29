import json

class Director:
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def toJson(self):
        return json.dumps(self.__dict__)

    @classmethod
    def fromJson(cls, json_string):
        json_data = json.loads(json_string)
        return cls(**json_data)

class Profesor:
    def __init__(self, dni, nombre, apellido, area):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.area = area

    def toJson(self):
        return json.dumps(self.__dict__)

    @classmethod
    def fromJson(cls, json_string):
        json_data = json.loads(json_string)
        return cls(**json_data)

class Alumno:
    def __init__(self, dni, nombre, apellido, promedio):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.promedio = promedio

    def toJson(self):
        return json.dumps(self.__dict__)

    @classmethod
    def fromJson(cls, json_string):
        json_data = json.loads(json_string)
        return cls(**json_data)

class Curso:
    def __init__(self, numero, nombre_profesor, capacidad):
        self.numero = numero
        self.nombre_profesor = nombre_profesor
        self.capacidad = capacidad

    def toJson(self):
        return json.dumps(self.__dict__)

    @classmethod
    def fromJson(cls, json_string):
        json_data = json.loads(json_string)
        return cls(**json_data)

class Escuela:
    def __init__(self, nombre, director_dni):
        self.nombre = nombre
        self.director_dni = director_dni

    def toJson(self):
        return json.dumps(self.__dict__)

    @classmethod
    def fromJson(cls, json_string):
        json_data = json.loads(json_string)
        return cls(**json_data)

class Inscripcion:
    def __init__(self, alumno_dni, curso_numero):
        self.alumno_dni = alumno_dni
        self.curso_numero = curso_numero

    def toJson(self):
        return json.dumps(self.__dict__)

    @classmethod
    def fromJson(cls, json_string):
        json_data = json.loads(json_string)
        return cls(**json_data)
