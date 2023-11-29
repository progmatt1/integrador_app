from ast import List
import flet as ft
import mysql.connector


def main(page: ft.Page):
    # Definición de elementos de la interfaz de usuario
    titulo = ft.Text("Escuela")
    dniField = ft.TextField(text_align=ft.TextAlign.RIGHT, width=150, hint_text="DNI")
    nombreField = ft.TextField(text_align=ft.TextAlign.RIGHT, width=150, hint_text="Nombre")
    apellidoField = ft.TextField(text_align=ft.TextAlign.RIGHT, width=150, hint_text="Apellido")
    promedioField = ft.TextField(text_align=ft.TextAlign.RIGHT, width=150, hint_text="Promedio")
    cursoField = ft.TextField(text_align=ft.TextAlign.RIGHT, width=150, hint_text="Curso")
    buscarAlumnoField = ft.TextField(text_align=ft.TextAlign.RIGHT, width=150, hint_text="Nombre")
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    t = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        expand=1,
    )

    # Configuración de la conexión a la base de datos
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'escueladb',
    }
    
    # Función para abrir un diálogo con información del alumno
    def open_dlg(e):
        alumno = buscar_alumno_dni(dni=buscarAlumnoField.value)
        dlg = ft.AlertDialog(
            title=ft.Text(f"DNI: {alumno[0][1]}, Nombre: {alumno[0][1]} {alumno[0][2]}, Promedio: {alumno[0][3]}, Curso: {alumno[0][4]}")
        )
        if len(alumno) > 0:
            page.dialog = dlg
            dlg.open = True
            page.update()
        else:
            page.dialog = ft.AlertDialog(
                title=ft.Text("No se encontró al alumno")
            )
            dlg.open = True
            page.update()

    # Función para inscribir a un alumno en un curso
    def inscribir_alumno(e):
        try:
            # Conectar a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Inscribir al alumno en el curso
            dni = dniField.value
            nombre = nombreField.value
            apellido = apellidoField.value
            promedio = promedioField.value
            curso = cursoField.value
            cursor.execute("INSERT INTO alumno VALUES (%s, %s, %s, %s, %s)", (dni, nombre, apellido, promedio, curso))
            conn.commit()

            print(f"Alumno insertado correctamente")
            
            page.update()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Cerrar la conexión a la base de datos
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                
    
    # Función para borrar un alumno de la base de datos
    def borrar_alumno(dni):
        try:
            # Conectar a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute(f"DELETE FROM alumno WHERE dni = {dni}")
            conn.commit()

            print(f"Alumno borrado correctamente")
            
            page.update()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Cerrar la conexión a la base de datos
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()


    # Función para obtener el total de alumnos
    def total_alumnos():
        try:
            # Conectar a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Obtener el total de alumnos
            cursor.execute("SELECT * FROM alumno")
            alumnos = cursor.fetchall()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Cerrar la conexión a la base de datos
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

        return alumnos

    # Función para buscar un alumno por DNI
    def buscar_alumno_dni(dni):
        try:
            # Conectar a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Obtener el total de alumnos
            cursor.execute(f"SELECT * FROM alumno WHERE dni = '{dni}'")
            alumnos = cursor.fetchall()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Cerrar la conexión a la base de datos
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

        return alumnos

    # Función para obtener el total de alumnos en un curso específico
    def total_alumnos_curso(curso):
        try:
            # Conectar a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Obtener el total de alumnos
            cursor.execute(f"SELECT * FROM alumno WHERE curso = '{curso}'")
            alumnos = cursor.fetchall()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Cerrar la conexión a la base de datos
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

        return alumnos

    # Función para obtener el total de cursos
    def total_cursos():
        try:
            # Conectar a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Obtener los cursos únicos para cada alumno
            cursor.execute("SELECT DISTINCT curso FROM alumno")
            cursos = cursor.fetchall()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Cerrar la conexión a la base de datos
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

        return cursos

    # Contenido de la página principal
    homeContent = ft.Container(content=ft.Column(
        controls=[
            ft.Text("Buscar Alumno por DNI"),
            buscarAlumnoField,
            ft.ElevatedButton(text="Buscar", on_click=open_dlg),
            ft.Text("Importar Alumno"),
            dniField,
            nombreField,
            apellidoField,
            promedioField,
            cursoField,
            ft.IconButton(ft.icons.ADD, on_click=inscribir_alumno),

            ft.Text("Alumnos"),
            lv,
        ]
    ))

    t.tabs = [
        ft.Tab(
            text="Home",
            icon=ft.icons.HOME,
            content=homeContent,
        ),
    ]
    cursos = total_cursos()
    count = 0
    for curso in cursos:
        alumnosCurso = total_alumnos_curso(curso[0])
        t.tabs.append(ft.Tab(
            text=curso[0],
            icon=ft.icons.TABLE_CHART,
            content=cursoPage(alumnos=alumnosCurso, curso=curso[0])
        ))

    alumnos = total_alumnos()
    count = 0
    for alumno in alumnos:
        lv.controls.append(ft.Row(
            [
                ft.Container(
                    border_radius=10,
                    border=ft.border.all(2, ft.colors.GREY),
                    padding=ft.padding.all(10),
                    content=ft.Text(f"DNI: {alumno[0]}, Nombre: {alumno[1]} {alumno[2]}, Promedio: {alumno[3]}, Curso: {alumno[4]}")
                ),  # Ajustar índices según la estructura de tu tabla
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color="red400",
                    icon_size=20,
                    tooltip="",
                    on_click=borrar_alumno(dni=alumno[0])
                ),
                ft.IconButton(
                    icon=ft.icons.EDIT,
                ),
            ]
        ))
        count += 1
        
    # Contenido final de la página
    content = ft.Column(
        [
            t,
        ],
    )
    
    page.add(content)


def cursoPage(alumnos: List, curso):
    # Crear una lista de alumnos en un curso específico
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    count = 0
    for alumno in alumnos:
        print(f"{curso} ==? {alumno[4]}")
        print(curso == alumno[4])
        if curso == alumno[4]:
            lv.controls.append(ft.Column(
                [
                    ft.Container(
                        border_radius=10,
                        border=ft.border.all(2, ft.colors.GREY),
                        padding=ft.padding.all(10),
                        content=ft.Text(f"DNI: {alumno[0]}, Nombre: {alumno[1]} {alumno[2]}, Promedio: {alumno[3]}, Curso: {alumno[4]}")
                    ),
                ]
            ))
        count += 1
        
    # Contenido de la página de curso
    content = ft.Column(
        [
            lv
        ]
    )

    return content

# Iniciar la aplicación con la clase principal
ft.app(target=main)
