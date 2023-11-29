import flet as ft
from flet_route import Params, Basket
from config import *
import mysql.connector
import json

titulo = ft.Text("Escuela")
dniField = ft.TextField(text_align=ft.TextAlign.RIGHT, width=150, hint_text="DNI")
nombreField = ft.TextField(text_align=ft.TextAlign.RIGHT, width=150, hint_text="Nombre")
apellidoField = ft.TextField(text_align=ft.TextAlign.RIGHT, width=150, hint_text="Apellido")
promedioField = ft.TextField(text_align=ft.TextAlign.RIGHT, width=150, hint_text="Promedio")
lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)


# Configuración de la conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '162534',
    'database': 'escueladb',
}

# Función para inscribir a un alumno en un curso
def inscribir_alumno(e):
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # # Verificar si el alumno ya existe
        # cursor.execute("SELECT * FROM alumno WHERE dni = %s", (dni,))
        # alumno_existente = cursor.fetchone()

        # if alumno_existente is not None:
        #     print(f"Error: El alumno con DNI {dni} ya existe.")
        #     return

        # Inscribir al alumno en el curso
        dni = dniField.value
        nombre = nombreField.value
        apellido = apellidoField.value
        promedio = promedioField.value
        cursor.execute("INSERT INTO alumno VALUES (%s, %s, %s, %s)", (dni, nombre, apellido, promedio))
        conn.commit()

        print(f"Alumno insertado correctamente")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Cerrar la conexión a la base de datos
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# Función para obtener el total de alumnos en la escuela y devolver un mensaje en formato JSON
def total_alumnos():
    result = {"success": False, "message": ""}
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Obtener el total de alumnos
        cursor.execute("SELECT * FROM alumno")
        total_alumnos = cursor.fetchall()

        result["success"] = True
        result["message"] = f"Total de alumnos en la escuela: {total_alumnos}"

    except mysql.connector.Error as err:
        result["message"] = f"Error: {err}"

    finally:
        # Cerrar la conexión a la base de datos
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return json.dumps(result)

# Función para obtener el promedio de un alumno específico y devolver un mensaje en formato JSON
def promedio_alumno(alumno_dni):
    result = {"success": False, "message": ""}
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verificar si el alumno existe
        cursor.execute("SELECT * FROM alumno WHERE dni = %s", (alumno_dni,))
        alumno_existente = cursor.fetchone()

        if alumno_existente is None:
            result["message"] = f"Error: El alumno con DNI {alumno_dni} no existe."
            return json.dumps(result)

        # Obtener el promedio del alumno
        cursor.execute("SELECT promedio FROM alumno WHERE dni = %s", (alumno_dni,))
        promedio_alumno = cursor.fetchone()[0]

        result["success"] = True
        result["message"] = f"Promedio del alumno con DNI {alumno_dni}: {promedio_alumno}"

    except mysql.connector.Error as err:
        result["message"] = f"Error: {err}"

    finally:
        # Cerrar la conexión a la base de datos
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return json.dumps(result)

# Función para obtener el listado de alumnos de un curso y devolver un mensaje en formato JSON
def listado_alumnos(curso_numero):
    result = {"success": False, "message": ""}
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verificar si el curso existe
        cursor.execute("SELECT * FROM curso WHERE numero = %s", (curso_numero,))
        curso_existente = cursor.fetchone()

        if curso_existente is None:
            result["message"] = f"Error: El curso con número {curso_numero} no existe."
            return json.dumps(result)

        # Obtener la lista de alumnos del curso
        cursor.execute("SELECT alumno.* FROM alumno JOIN inscripcion ON alumno.dni = inscripcion.alumno_dni WHERE inscripcion.curso_numero = %s", (curso_numero,))
        alumnos_curso = cursor.fetchall()

        if not alumnos_curso:
            result["message"] = f"No hay alumnos inscritos en el curso {curso_numero}."
            return json.dumps(result)

        # Construir la lista de alumnos en formato JSON
        alumnos_list = [{"dni": alumno[0], "nombre": alumno[1], "apellido": alumno[2], "promedio": float(alumno[3])} for alumno in alumnos_curso]

        result["success"] = True
        result["message"] = {"curso_numero": curso_numero, "alumnos": alumnos_list}

    except mysql.connector.Error as err:
        result["message"] = f"Error: {err}"

    finally:
        # Cerrar la conexión a la base de datos
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return json.dumps(result)

def buscar_alumno_por_dni(alumno_dni):
    result = {"success": False, "message": ""}
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Buscar al alumno por su DNI
        cursor.execute("SELECT * FROM alumno WHERE dni = %s", (alumno_dni,))
        alumno_encontrado = cursor.fetchone()

        if alumno_encontrado is None:
            result["message"] = f"No se encontró un alumno con DNI {alumno_dni}."
            return json.dumps(result)

        # Construir el objeto de alumno en formato JSON
        alumno_info = {"dni": alumno_encontrado[0], "nombre": alumno_encontrado[1], "apellido": alumno_encontrado[2], "promedio": float(alumno_encontrado[3])}

        result["success"] = True
        result["message"] = {"alumno": alumno_info}

    except mysql.connector.Error as err:
        result["message"] = f"Error: {err}"

    finally:
        # Cerrar la conexión a la base de datos
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return json.dumps(result)

# Función para actualizar la información de un alumno, profesor o director y devolver un mensaje en formato JSON
def actualizar_informacion(tipo, id, nueva_informacion):
    result = {"success": False, "message": ""}
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verificar el tipo de entidad (alumno, profesor, director)
        if tipo.lower() == "alumno":
            entidad = "alumno"
        elif tipo.lower() == "profesor":
            entidad = "profesor"
        elif tipo.lower() == "director":
            entidad = "director"
        else:
            result["message"] = f"Error: Tipo de entidad '{tipo}' no válido."
            return json.dumps(result)

        # Verificar si la entidad con el ID proporcionado existe
        cursor.execute(f"SELECT * FROM {entidad} WHERE dni = %s", (id,))
        entidad_existente = cursor.fetchone()

        if entidad_existente is None:
            result["message"] = f"No se encontró un(a) {tipo} con ID {id}."
            return json.dumps(result)

        # Construir la consulta de actualización
        set_clause = ", ".join([f"{column} = %s" for column in nueva_informacion.keys()])
        update_query = f"UPDATE {entidad} SET {set_clause} WHERE dni = %s"

        # Actualizar la información
        cursor.execute(update_query, tuple(nueva_informacion.values()) + (id,))
        conn.commit()

        result["success"] = True
        result["message"] = f"Información de {tipo} con ID {id} actualizada correctamente."

    except mysql.connector.Error as err:
        result["message"] = f"Error: {err}"

    finally:
        # Cerrar la conexión a la base de datos
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return result

alumnos = total_alumnos()
count = 0
for i in range(0, len(alumnos)):
    lv.controls.append(ft.Column(
        [
            ft.Text(alumnos[count]),
        ]
    ))
    count += 1

def inicio(page: ft.Page, params: Params, basket: Basket):   
    
    content = ft.Container(content=ft.Column(
        controls=[
            ft.Text("Importar Alumno"),
            dniField,
            nombreField,
            apellidoField,
            promedioField,
            ft.IconButton(ft.icons.ADD, on_click=inscribir_alumno),

            ft.Text("Alumnos"),
            ft.Text(alumnos),
            lv
        ]
    ))

    return content 