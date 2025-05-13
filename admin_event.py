import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime
from clase_evento import Evento
from tkcalendar import DateEntry  # Importamos DateEntry para el calendario

# ---------- Estilos Globales ----------
estilo_boton_rosa = {
    "bg": "#ffc0cb",  # Color rosa
    "fg": "black",  # Texto negro
    "font": ("Arial", 11),
    "width": 12,
    "height": 2,
    "bd": 0
}

estilo_boton_gris = {
    "bg": "lightgray",
    "fg": "black",  # Texto negro
    "font": ("Arial", 11),
    "width": 12,
    "height": 2,
    "bd": 0
}

estilo_boton_menu = {
    "bg": "#ffc0cb",  # Color rosa
    "fg": "black",  # Texto negro
    "font": ("Arial", 12),
    "width": 30,
    "height": 2,
    "bd": 0
}

# Estilo para el calendario
estilo_calendario = {
    "width": 12,
    "background": "#ffc0cb",
    "foreground": "black",
    "bordercolor": "#ffc0cb",
    "headersbackground": "#ffc0cb",
    "headersforeground": "black",
    "selectbackground": "#ff8da1",
    "font": ("Arial", 10)
}

# ---------- Funciones para archivo ----------
archivo = "eventos.txt"


def leer_eventos(archivo):
    eventos = []
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            for linea in f:
                if linea.strip():  # Verificar que la línea no esté vacía
                    datos = linea.strip().split(",")
                    if len(datos) >= 6:  # Verificar que tenga todos los campos (ahora son 6 con la hora)
                        evento = Evento(
                            datos[0],  # id_evento
                            datos[1],  # nombre_evento
                            datos[2],  # fecha
                            datos[3],  # hora (nuevo campo)
                            int(datos[4]),  # capacidad (como entero)
                            datos[5]  # ubicacion
                        )
                        eventos.append(evento)
    return eventos


def guardar_eventos(eventos, archivo):
    with open(archivo, "w") as f:
        for evento in eventos:
            f.write(
                f"{evento.get_id_evento()},{evento.get_nombre_evento()},{evento.get_fecha()},{evento.get_hora()},{evento.get_capacidad()},{evento.get_ubicacion()}\n")


def generar_id(eventos):
    if not eventos:
        return 1
    else:
        return max(int(e.get_id_evento()) for e in eventos) + 1


# ---------- Ventana Registrar Evento ----------
def registrar_evento_ventana(anterior):
    anterior.destroy()

    registrar = tk.Tk()
    registrar.title("Registrar Nuevo Evento")

    ancho = 350
    alto = 500  # Aumentamos la altura para acomodar el selector de hora
    x = (registrar.winfo_screenwidth() // 2) - (ancho // 2)
    y = (registrar.winfo_screenheight() // 2) - (alto // 2)
    registrar.geometry(f"{ancho}x{alto}+{x}+{y}")
    registrar.resizable(False, False)

    eventos = leer_eventos(archivo)
    nuevo_id = generar_id(eventos)

    nombre_var = tk.StringVar()
    hora_var = tk.StringVar(value="12:00")  # Valor predeterminado para la hora
    capacidad_var = tk.StringVar()
    ubicacion_var = tk.StringVar()

    tk.Label(registrar, text=f"ID Asignado: {nuevo_id}", font=("Arial", 12)).pack(pady=10)

    tk.Label(registrar, text="Nombre del Evento").pack()
    tk.Entry(registrar, textvariable=nombre_var).pack()

    tk.Label(registrar, text="Fecha").pack()
    # Usamos DateEntry en lugar de Entry para la fecha
    cal = DateEntry(registrar,
                    width=estilo_calendario["width"],
                    background=estilo_calendario["background"],
                    foreground=estilo_calendario["foreground"],
                    bordercolor=estilo_calendario["bordercolor"],
                    headersbackground=estilo_calendario["headersbackground"],
                    headersforeground=estilo_calendario["headersforeground"],
                    selectbackground=estilo_calendario["selectbackground"],
                    font=estilo_calendario["font"],
                    date_pattern="dd/MM/yyyy")  # Formato DD/MM/AAAA
    cal.pack(pady=5)

    # Agregamos el selector de hora
    tk.Label(registrar, text="Hora").pack()

    # Frame para contener el selector de hora
    frame_hora = tk.Frame(registrar)
    frame_hora.pack(pady=5)

    # Spinbox para la hora (0-23)
    tk.Label(frame_hora, text="Hora:").pack(side=tk.LEFT, padx=5)
    hora_spin = tk.Spinbox(frame_hora, from_=0, to=23, width=3, format="%02.0f")
    hora_spin.pack(side=tk.LEFT, padx=5)
    hora_spin.delete(0, tk.END)
    hora_spin.insert(0, "12")  # Valor predeterminado

    tk.Label(frame_hora, text="Min:").pack(side=tk.LEFT, padx=5)
    min_spin = tk.Spinbox(frame_hora, from_=0, to=59, width=3, format="%02.0f")
    min_spin.pack(side=tk.LEFT, padx=5)
    min_spin.delete(0, tk.END)
    min_spin.insert(0, "00")  # Valor predeterminado

    # Función para actualizar la variable hora_var cuando cambian los spinbox
    def actualizar_hora(*args):
        hora = hora_spin.get().zfill(2)
        minuto = min_spin.get().zfill(2)
        hora_var.set(f"{hora}:{minuto}")

    hora_spin.config(command=actualizar_hora)
    min_spin.config(command=actualizar_hora)
    # Llamamos a actualizar_hora inicialmente para establecer el valor predeterminado
    actualizar_hora()

    tk.Label(registrar, text="Capacidad (personas)").pack()
    tk.Entry(registrar, textvariable=capacidad_var).pack()

    tk.Label(registrar, text="Ubicación").pack()
    tk.Entry(registrar, textvariable=ubicacion_var).pack()

    def guardar_evento():
        try:
            # Validar capacidad
            if not capacidad_var.get().strip().isdigit():
                messagebox.showerror("Error", "La capacidad debe ser un número entero")
                return

            # Obtener la fecha del calendario en formato DD/MM/AAAA
            fecha_seleccionada = cal.get_date().strftime("%d/%m/%Y")

            # Obtener la hora seleccionada
            hora_seleccionada = hora_var.get()

            # Crear evento con la nueva hora
            evento = Evento(
                str(nuevo_id),
                nombre_var.get().strip(),
                fecha_seleccionada,
                hora_seleccionada,  # Nueva hora
                int(capacidad_var.get().strip()),
                ubicacion_var.get().strip()
            )
            eventos.append(evento)
            guardar_eventos(eventos, archivo)
            messagebox.showinfo("Éxito", f"Evento con ID {nuevo_id} registrado correctamente.")
            registrar.destroy()
            crear_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar el evento: {str(e)}")

    # IMPORTANTE: Primero crear el botón y luego definir la función verificar_campos
    btn_guardar = tk.Button(registrar, text="Registrar Evento", command=guardar_evento, state=tk.DISABLED,
                            **estilo_boton_gris)
    btn_guardar.pack(pady=10)

    btn_regresar = tk.Button(registrar, text="Regresar al Menú", command=lambda: [registrar.destroy(), crear_menu()],
                             **estilo_boton_rosa)
    btn_regresar.pack()

    # Ahora definimos la función verificar_campos después de crear btn_guardar
    def verificar_campos(*args):
        try:
            capacidad_valida = capacidad_var.get().strip().isdigit()

            if (nombre_var.get().strip() and
                    hora_var.get().strip() and  # Verificamos también la hora
                    capacidad_var.get().strip() and capacidad_valida and
                    ubicacion_var.get().strip()):
                btn_guardar.config(state=tk.NORMAL, bg=estilo_boton_rosa["bg"], fg=estilo_boton_rosa["fg"])
            else:
                btn_guardar.config(state=tk.DISABLED, bg=estilo_boton_gris["bg"], fg=estilo_boton_gris["fg"])
        except Exception as e:
            print(f"Error en verificar_campos: {e}")
            btn_guardar.config(state=tk.DISABLED, bg=estilo_boton_gris["bg"], fg=estilo_boton_gris["fg"])

    # Añadimos los trace después de definir la función
    for var in [nombre_var, hora_var, capacidad_var, ubicacion_var]:
        var.trace_add('write', verificar_campos)

    # Verificar campos iniciales
    verificar_campos()

    registrar.mainloop()


# ---------- Modificar Evento ----------
def modificar_evento():
    eventos = leer_eventos(archivo)
    if not eventos:
        messagebox.showinfo("Modificar Evento", "No hay eventos registrados.")
        crear_menu()
        return

    # Ventana para ingresar ID a modificar
    ventana_modificar = tk.Tk()
    ventana_modificar.title("Modificar Evento")

    ancho = 400
    alto = 250
    x = (ventana_modificar.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_modificar.winfo_screenheight() // 2) - (alto // 2)
    ventana_modificar.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana_modificar.resizable(False, False)

    tk.Label(ventana_modificar, text="Ingrese el ID del evento a modificar:").pack(pady=10)

    id_var = tk.StringVar()
    tk.Entry(ventana_modificar, textvariable=id_var).pack(pady=5)

    def buscar_evento():
        id_buscar = id_var.get().strip()

        # Buscar si el ID existe
        evento_encontrado = next((e for e in eventos if e.get_id_evento() == id_buscar), None)

        if evento_encontrado:
            messagebox.showinfo("ID Encontrado", f"El ID {id_buscar} existe. Puede proceder a modificar.")
            ventana_modificar.destroy()

            # Ventana de modificación
            ventana_modificacion = tk.Tk()
            ventana_modificacion.title(f"Modificar Evento {id_buscar}")

            ancho = 400
            alto = 550  # Aumentamos altura para el selector de hora
            x = (ventana_modificacion.winfo_screenwidth() // 2) - (ancho // 2)
            y = (ventana_modificacion.winfo_screenheight() // 2) - (alto // 2)
            ventana_modificacion.geometry(f"{ancho}x{alto}+{x}+{y}")
            ventana_modificacion.resizable(False, False)

            # Variables para los campos
            nombre_var = tk.StringVar(value=evento_encontrado.get_nombre_evento())
            hora_var = tk.StringVar(value=evento_encontrado.get_hora())  # Valor actual de la hora
            capacidad_var = tk.StringVar(value=str(evento_encontrado.get_capacidad()))
            ubicacion_var = tk.StringVar(value=evento_encontrado.get_ubicacion())

            # Campos de entrada
            tk.Label(ventana_modificacion, text="Nombre del Evento:").pack(pady=5)
            tk.Entry(ventana_modificacion, textvariable=nombre_var).pack(pady=2)

            tk.Label(ventana_modificacion, text="Fecha:").pack(pady=5)

            # Convertir la fecha del evento a objeto datetime para el calendario
            fecha_actual = datetime.strptime(evento_encontrado.get_fecha(), "%d/%m/%Y")

            # Usar DateEntry para la fecha
            cal = DateEntry(ventana_modificacion,
                            width=estilo_calendario["width"],
                            background=estilo_calendario["background"],
                            foreground=estilo_calendario["foreground"],
                            bordercolor=estilo_calendario["bordercolor"],
                            headersbackground=estilo_calendario["headersbackground"],
                            headersforeground=estilo_calendario["headersforeground"],
                            selectbackground=estilo_calendario["selectbackground"],
                            font=estilo_calendario["font"],
                            date_pattern="dd/MM/yyyy",  # Formato DD/MM/AAAA
                            year=fecha_actual.year,
                            month=fecha_actual.month,
                            day=fecha_actual.day)
            cal.pack(pady=2)

            # Agregamos el selector de hora para modificación
            tk.Label(ventana_modificacion, text="Hora:").pack(pady=5)

            # Frame para contener el selector de hora
            frame_hora = tk.Frame(ventana_modificacion)
            frame_hora.pack(pady=2)

            # Extraer hora y minutos actuales
            try:
                hora_actual, min_actual = evento_encontrado.get_hora().split(":")
            except:
                hora_actual, min_actual = "12", "00"  # Valores predeterminados si hay error

            # Spinbox para la hora (0-23)
            tk.Label(frame_hora, text="Hora:").pack(side=tk.LEFT, padx=5)
            hora_spin = tk.Spinbox(frame_hora, from_=0, to=23, width=3, format="%02.0f")
            hora_spin.pack(side=tk.LEFT, padx=5)
            hora_spin.delete(0, tk.END)
            hora_spin.insert(0, hora_actual)  # Valor actual

            tk.Label(frame_hora, text="Min:").pack(side=tk.LEFT, padx=5)
            min_spin = tk.Spinbox(frame_hora, from_=0, to=59, width=3, format="%02.0f")
            min_spin.pack(side=tk.LEFT, padx=5)
            min_spin.delete(0, tk.END)
            min_spin.insert(0, min_actual)  # Valor actual

            # Función para actualizar la variable hora_var cuando cambian los spinbox
            def actualizar_hora(*args):
                hora = hora_spin.get().zfill(2)
                minuto = min_spin.get().zfill(2)
                hora_var.set(f"{hora}:{minuto}")

            hora_spin.config(command=actualizar_hora)
            min_spin.config(command=actualizar_hora)
            # Llamamos a actualizar_hora inicialmente para establecer el valor actual
            actualizar_hora()

            tk.Label(ventana_modificacion, text="Capacidad:").pack(pady=5)
            tk.Entry(ventana_modificacion, textvariable=capacidad_var).pack(pady=2)

            tk.Label(ventana_modificacion, text="Ubicación:").pack(pady=5)
            tk.Entry(ventana_modificacion, textvariable=ubicacion_var).pack(pady=2)

            def guardar_modificaciones():
                try:
                    # Validar capacidad
                    if not capacidad_var.get().strip().isdigit():
                        messagebox.showerror("Error", "La capacidad debe ser un número entero")
                        return

                    # Obtener fecha seleccionada del calendario
                    fecha_seleccionada = cal.get_date().strftime("%d/%m/%Y")

                    # Obtener hora seleccionada
                    hora_seleccionada = hora_var.get()

                    # Actualizar datos del evento
                    eventos_actualizados = leer_eventos(archivo)
                    for i, e in enumerate(eventos_actualizados):
                        if e.get_id_evento() == id_buscar:
                            e.set_nombre_evento(nombre_var.get().strip())
                            e.set_fecha(fecha_seleccionada)
                            e.set_hora(hora_seleccionada)  # Actualizar hora
                            e.set_capacidad(int(capacidad_var.get().strip()))
                            e.set_ubicacion(ubicacion_var.get().strip())
                            break

                    guardar_eventos(eventos_actualizados, archivo)
                    messagebox.showinfo("Éxito", f"Evento con ID {id_buscar} modificado correctamente.")
                    ventana_modificacion.destroy()
                    crear_menu()
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrió un error al modificar el evento: {str(e)}")

            # Primero creamos el botón
            btn_guardar = tk.Button(ventana_modificacion, text="Guardar Cambios", command=guardar_modificaciones,
                                    **estilo_boton_rosa)
            btn_guardar.pack(pady=10)

            btn_regresar = tk.Button(ventana_modificacion, text="Regresar al Menú",
                                     command=lambda: [ventana_modificacion.destroy(), crear_menu()],
                                     **estilo_boton_rosa)
            btn_regresar.pack(pady=5)

            # Ahora definimos la función verificar_campos después de crear btn_guardar
            def verificar_campos(*args):
                try:
                    capacidad_valida = capacidad_var.get().strip().isdigit()

                    if (nombre_var.get().strip() and
                            hora_var.get().strip() and  # Verificamos también la hora
                            capacidad_var.get().strip() and capacidad_valida and
                            ubicacion_var.get().strip()):
                        btn_guardar.config(state=tk.NORMAL, bg=estilo_boton_rosa["bg"], fg=estilo_boton_rosa["fg"])
                    else:
                        btn_guardar.config(state=tk.DISABLED, bg=estilo_boton_gris["bg"], fg=estilo_boton_gris["fg"])
                except Exception as e:
                    print(f"Error en verificar_campos (modificar): {e}")
                    btn_guardar.config(state=tk.DISABLED, bg=estilo_boton_gris["bg"], fg=estilo_boton_gris["fg"])

            # Añadimos el tracer después de definir la función
            for var in [nombre_var, hora_var, capacidad_var, ubicacion_var]:
                var.trace_add('write', verificar_campos)

            # Verificar campos iniciales
            verificar_campos()

            ventana_modificacion.mainloop()
        else:
            messagebox.showerror("Error", "El ID ingresado no existe.")

    # Botones en la misma línea
    frame_botones = tk.Frame(ventana_modificar)
    frame_botones.pack(pady=10)

    # Botón Siguiente (inicialmente deshabilitado)
    btn_siguiente = tk.Button(frame_botones, text="Siguiente", command=buscar_evento, state=tk.DISABLED,
                              **estilo_boton_gris)
    btn_siguiente.pack(side="left", padx=10)

    # Verificar si se ha ingresado un ID para habilitar el botón
    def verificar_id(*args):
        if id_var.get().strip():
            btn_siguiente.config(state=tk.NORMAL, bg=estilo_boton_rosa["bg"], fg=estilo_boton_rosa["fg"])
        else:
            btn_siguiente.config(state=tk.DISABLED, bg=estilo_boton_gris["bg"], fg=estilo_boton_gris["fg"])

    # Activar la verificación cuando el texto cambia
    id_var.trace_add('write', verificar_id)

    # Botón Regresar al Menú
    tk.Button(frame_botones, text="Regresar al Menú", command=lambda: [ventana_modificar.destroy(), crear_menu()],
              **estilo_boton_rosa).pack(side="left", padx=10)

    ventana_modificar.mainloop()


# ---------- Mostrar Eventos ----------
def mostrar_eventos():
    eventos = leer_eventos(archivo)
    if not eventos:
        messagebox.showinfo("Mostrar Eventos", "No hay eventos registrados.")
        crear_menu()
        return

    ventana = tk.Toplevel()
    ventana.title("Eventos Registrados")

    frame = tk.Frame(ventana)
    frame.pack(fill='both', expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#d9d9d9", foreground="black")

    # Agregamos la columna "Hora" al treeview
    tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Fecha", "Hora", "Capacidad", "Ubicación"), show="headings")
    tree.pack(side="left", fill="both", expand=True)

    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_y.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = ttk.Scrollbar(ventana, orient="horizontal", command=tree.xview)
    scrollbar_x.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=scrollbar_x.set)

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    for evento in eventos:
        tree.insert("", "end", values=(
            evento.get_id_evento(),
            evento.get_nombre_evento(),
            evento.get_fecha(),
            evento.get_hora(),  # Agregamos la hora
            evento.get_capacidad(),
            evento.get_ubicacion()
        ))

    # Botón para cerrar
    tk.Button(ventana, text="Cerrar", command=ventana.destroy, **estilo_boton_rosa).pack(pady=10)

    ventana.mainloop()

# ---------- Eliminar Evento ----------
def eliminar_evento():
    eventos = leer_eventos(archivo)

    if not eventos:
        messagebox.showinfo("Eliminar Evento", "No hay eventos registrados.")
        crear_menu()
        return

    # Ventana para ingresar ID a eliminar
    ventana_eliminar = tk.Tk()
    ventana_eliminar.title("Eliminar Evento")

    ancho = 400
    alto = 250
    x = (ventana_eliminar.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_eliminar.winfo_screenheight() // 2) - (alto // 2)
    ventana_eliminar.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana_eliminar.resizable(False, False)

    tk.Label(ventana_eliminar, text="Ingrese el ID del evento a eliminar:").pack(pady=10)

    id_var = tk.StringVar()
    entry_id = tk.Entry(ventana_eliminar, textvariable=id_var)
    entry_id.pack(pady=5)

    # Verificar si se ha ingresado un ID para habilitar el botón
    def verificar_id(*args):
        if id_var.get().strip():
            btn_eliminar.config(state=tk.NORMAL, bg=estilo_boton_rosa["bg"], fg=estilo_boton_rosa["fg"])
        else:
            btn_eliminar.config(state=tk.DISABLED, bg=estilo_boton_gris["bg"], fg=estilo_boton_gris["fg"])

    id_var.trace_add('write', verificar_id)

    def buscar_evento():
        id_buscar = id_var.get().strip()

        # Buscar si el ID existe
        evento_encontrado = next((e for e in eventos if e.get_id_evento() == id_buscar), None)

        if evento_encontrado:
            # Crear ventana de confirmación
            ventana_confirmar = tk.Toplevel(ventana_eliminar)
            ventana_confirmar.title("Confirmar eliminación")

            # Centrar ventana de confirmación
            ancho_confirmar = 400
            alto_confirmar = 200
            x_confirmar = (ventana_confirmar.winfo_screenwidth() // 2) - (ancho_confirmar // 2)
            y_confirmar = (ventana_confirmar.winfo_screenheight() // 2) - (alto_confirmar // 2)
            ventana_confirmar.geometry(f"{ancho_confirmar}x{alto_confirmar}+{x_confirmar}+{y_confirmar}")
            ventana_confirmar.resizable(False, False)

            # Mensaje de confirmación con detalles del evento (incluida la hora)
            mensaje = f"""¿Está seguro de eliminar el evento con ID {id_buscar}?
Nombre: {evento_encontrado.get_nombre_evento()}
Fecha: {evento_encontrado.get_fecha()}
Hora: {evento_encontrado.get_hora()}
Ubicación: {evento_encontrado.get_ubicacion()}

Una vez eliminado no podrá recuperarse su información."""

            tk.Label(ventana_confirmar, text=mensaje, wraplength=350, justify="left").pack(pady=10)

            # Frame para botones
            frame_botones_confirmar = tk.Frame(ventana_confirmar)
            frame_botones_confirmar.pack(pady=10)

            # Función para confirmar eliminación
            def confirmar_eliminacion():
                eventos.remove(evento_encontrado)
                guardar_eventos(eventos, archivo)
                ventana_confirmar.destroy()
                messagebox.showinfo("Eliminación Exitosa", f"El evento con ID {id_buscar} ha sido eliminado.")
                ventana_eliminar.destroy()
                crear_menu()

            # Función para cancelar eliminación
            def cancelar_eliminacion():
                ventana_confirmar.destroy()
                messagebox.showinfo("Operación Cancelada",
                                    "El evento no ha sido eliminado.\n REGRESANDO AL MENU PRINCIPAL!!!")
                ventana_eliminar.destroy()
                crear_menu()

            # Botones de confirmar y cancelar
            tk.Button(
                frame_botones_confirmar,
                text="Sí",
                command=confirmar_eliminacion,
                **estilo_boton_rosa
            ).pack(side="left", padx=10)

            tk.Button(
                frame_botones_confirmar,
                text="No",
                command=cancelar_eliminacion,
                **estilo_boton_rosa
            ).pack(side="left", padx=10)

            # Modal (hacer que la ventana de confirmación sea modal)
            ventana_confirmar.transient(ventana_eliminar)
            ventana_confirmar.grab_set()
            ventana_eliminar.wait_window(ventana_confirmar)
        else:
            messagebox.showerror("Error", "El ID ingresado no existe.")

    # Botones en la misma línea
    frame_botones = tk.Frame(ventana_eliminar)
    frame_botones.pack(pady=10)

    # Botón Eliminar (inicialmente deshabilitado)
    btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=buscar_evento, state=tk.DISABLED,
                             **estilo_boton_gris)
    btn_eliminar.pack(side="left", padx=10)

    # Botón Regresar al Menú
    tk.Button(frame_botones, text="Regresar al Menú", command=lambda: [ventana_eliminar.destroy(), crear_menu()],
              **estilo_boton_rosa).pack(side="left", padx=10)

    ventana_eliminar.mainloop()

# ---------- Volver al submenu administrador ----------
def volver_a_submenu_admin():
    import sub_menu_administrador
    sub_menu_administrador.crear_menu_administrador()





# ---------- Ventana Principal / Menú ----------
def crear_menu():
    ventana = tk.Tk()
    ventana.title("Gestión de Eventos")

    ancho = 300
    alto = 400
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.resizable(False, False)

    tk.Label(ventana, text="--- MENÚ DE EVENTOS ---", font=("Arial", 14)).pack(pady=10)
    tk.Button(ventana, text="Registrar nuevo evento", command=lambda: registrar_evento_ventana(ventana),
              **estilo_boton_menu).pack(
        pady=5)
    tk.Button(ventana, text="Mostrar eventos", command=mostrar_eventos, **estilo_boton_menu).pack(pady=5)
    tk.Button(ventana, text="Modificar evento", command=lambda: [ventana.destroy(), modificar_evento()],
              **estilo_boton_menu).pack(pady=5)
    tk.Button(ventana, text="Eliminar evento", command=lambda: [ventana.destroy(), eliminar_evento()],
              **estilo_boton_menu).pack(pady=5)
    tk.Button(ventana, text="Regresar al submenu administrador",
              command=lambda: [ventana.destroy(), volver_a_submenu_admin()], **estilo_boton_menu).pack(pady=20)

    ventana.mainloop()


# ---------- Ejecutar Programa desde otro archivo ----------
def ejecutar_submenu():
    crear_menu()


# ---------- Ejecutar Programa ----------
if __name__ == "__main__":
    # Asegurarse de que el archivo de eventos exista
    if not os.path.exists(archivo):
        with open(archivo, "w") as f:
            pass  # Crear archivo vacío
    crear_menu()

# si no tengo eventos y quiero eliminar me parece un mensaje de rror y al darle en acptar no veo de nuevo el menu
#de opcines, ademas que cuando voy al menu de administrador y luego quiero regresar ya no puedo porque no esta activada la opcion en el menu
#del administrador
