import tkinter as tk
from tkinter import messagebox, ttk
import pickle
import os
from clase_persona import Persona

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

# ---------- Funciones para archivo ----------
archivo = "personas.txt"



def leer_personas(archivo):
    personas = []
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) == 5:
                    codigo, nombre, sexo, correo, edad = partes
                    personas.append(Persona(codigo, nombre, sexo, correo, int(edad)))
    return personas


def guardar_personas(personas, archivo):
    with open(archivo, "w", encoding="utf-8") as f:
        for p in personas:
            f.write(f"{p.codigo},{p.nombre},{p.sexo},{p.correo},{p.edad}\n")



def generar_id(personas):
    if not personas:
        return 1
    else:
        return max(int(p.codigo) for p in personas) + 1


# ---------- Ventana Alta Persona ----------
def alta_persona_ventana(anterior):
    anterior.destroy()

    alta = tk.Tk()
    alta.title("Alta de Persona")

    ancho = 350
    alto = 400
    x = (alta.winfo_screenwidth() // 2) - (ancho // 2)
    y = (alta.winfo_screenheight() // 2) - (alto // 2)
    alta.geometry(f"{ancho}x{alto}+{x}+{y}")
    alta.resizable(False, False)

    personas = leer_personas(archivo)
    nuevo_id = generar_id(personas)

    nombre_var = tk.StringVar()
    sexo_var = tk.StringVar()
    correo_var = tk.StringVar()
    edad_var = tk.StringVar()

    def verificar_campos(*args):
        if all([nombre_var.get().strip(), sexo_var.get().strip(), correo_var.get().strip(), edad_var.get().isdigit()]):
            btn_guardar.config(state=tk.NORMAL, bg=estilo_boton_rosa["bg"], fg=estilo_boton_rosa["fg"])
        else:
            btn_guardar.config(state=tk.DISABLED, bg=estilo_boton_gris["bg"], fg=estilo_boton_gris["fg"])

    for var in [nombre_var, sexo_var, correo_var, edad_var]:
        var.trace_add('write', verificar_campos)

    tk.Label(alta, text=f"ID Asignado: {nuevo_id}", font=("Arial", 12)).pack(pady=10)

    tk.Label(alta, text="Nombre").pack()
    tk.Entry(alta, textvariable=nombre_var).pack()

    tk.Label(alta, text="Sexo").pack()
    sexo_combo = ttk.Combobox(alta, textvariable=sexo_var, values=["Femenino", "Masculino"], state="readonly")
    sexo_combo.pack()

    tk.Label(alta, text="Correo").pack()
    tk.Entry(alta, textvariable=correo_var).pack()

    tk.Label(alta, text="Edad").pack()
    tk.Entry(alta, textvariable=edad_var).pack()

    def guardar_persona():
        correo_ingresado = correo_var.get().strip().lower()

        for p in personas:
            if p.correo.lower() == correo_ingresado:
                messagebox.showerror("Error",
                                     "NO FUE POSIBLE REGISTRARLO YA QUE ESE CORREO YA ESTÁ EN USO, FAVOR DE AGREGAR OTRO CORREO")
                return  # Detiene el guardado

        persona = Persona(
            str(nuevo_id),
            nombre_var.get(),
            sexo_var.get(),
            correo_var.get(),
            int(edad_var.get())
        )
        personas.append(persona)
        guardar_personas(personas, archivo)
        messagebox.showinfo("Éxito", f"Persona con ID {nuevo_id} guardada correctamente.")
        alta.destroy()
        crear_menu()

    btn_guardar = tk.Button(alta, text="Completar Registro", command=guardar_persona, state=tk.DISABLED,
                            **estilo_boton_gris)
    btn_guardar.pack(pady=10)

    btn_regresar = tk.Button(alta, text="Regresar al Menú", command=lambda: [alta.destroy(), crear_menu()],
                             **estilo_boton_rosa)
    btn_regresar.pack()

    alta.mainloop()


# ---------- Modificar Persona ----------
def modificar_persona():
    personas = leer_personas(archivo)

    # Ventana para ingresar ID a modificar
    ventana_modificar = tk.Tk()
    ventana_modificar.title("Modificar Persona")

    ancho = 400
    alto = 250
    x = (ventana_modificar.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_modificar.winfo_screenheight() // 2) - (alto // 2)
    ventana_modificar.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana_modificar.resizable(False, False)

    tk.Label(ventana_modificar, text="Ingrese el ID de la persona a modificar:").pack(pady=10)

    id_var = tk.StringVar()

    tk.Entry(ventana_modificar, textvariable=id_var).pack(pady=5)

    def buscar_persona():
        id_buscar = id_var.get().strip()

        # Buscar si el ID existe
        persona_encontrada = next((p for p in personas if p.codigo == id_buscar), None)

        if persona_encontrada:
            messagebox.showinfo("ID Encontrado", f"El ID {id_buscar} existe. Puede proceder a modificar.")
            ventana_modificar.destroy()

            # Ventana de modificación
            ventana_modificacion = tk.Tk()
            ventana_modificacion.title(f"Modificar Persona {id_buscar}")

            ancho = 400
            alto = 300
            x = (ventana_modificacion.winfo_screenwidth() // 2) - (ancho // 2)
            y = (ventana_modificacion.winfo_screenheight() // 2) - (alto // 2)
            ventana_modificacion.geometry(f"{ancho}x{alto}+{x}+{y}")
            ventana_modificacion.resizable(False, False)

            # Texto inicial
            tk.Label(ventana_modificacion, text="Elige la opción que deseas modificar:", font=("Arial", 12)).pack(
                pady=10)

            # Barra de opciones (ComboBox)
            opciones = ["Modificar nombre", "Modificar correo"]
            opcion_var = tk.StringVar()

            combo_opciones = ttk.Combobox(ventana_modificacion, textvariable=opcion_var, values=opciones,
                                          state="readonly")
            combo_opciones.pack(pady=5)

            # Campo para ingresar el nuevo nombre o correo
            nuevo_valor_label = tk.Label(ventana_modificacion, text="Ingresa el nuevo valor: ")
            nuevo_valor_label.pack(pady=5)

            nuevo_valor_var = tk.StringVar()
            nuevo_valor_entry = tk.Entry(ventana_modificacion, textvariable=nuevo_valor_var)
            nuevo_valor_entry.pack(pady=5)

            # Deshabilitar el botón de modificar al principio
            btn_modificar = tk.Button(ventana_modificacion, text="Modificar",
                                      command=lambda: modificar_datos(persona_encontrada, opcion_var, nuevo_valor_var,
                                                                      ventana_modificacion), state=tk.DISABLED,
                                      **estilo_boton_gris)
            btn_modificar.pack(pady=10)

            # Verificar si el nuevo valor es válido para habilitar el botón
            def verificar_nuevo_valor(*args):
                if nuevo_valor_var.get().strip():
                    btn_modificar.config(state=tk.NORMAL, bg=estilo_boton_rosa["bg"], fg=estilo_boton_rosa["fg"])
                else:
                    btn_modificar.config(state=tk.DISABLED, bg=estilo_boton_gris["bg"], fg=estilo_boton_gris["fg"])

            nuevo_valor_var.trace_add('write', verificar_nuevo_valor)

            # Función para modificar los datos
            def modificar_datos(persona, opcion, nuevo_valor, ventana):
                # Leer las personas actualizadas desde el archivo
                personas = leer_personas(archivo)

                if opcion.get() == "Modificar nombre":
                    persona.nombre = nuevo_valor.get().strip()
                elif opcion.get() == "Modificar correo":
                    # Verificar si el correo ya existe
                    correo_nuevo = nuevo_valor.get().strip().lower()

                    # Verificar si ya hay otro usuario con el mismo correo
                    for p in personas:
                        if p.correo.lower() == correo_nuevo and p.codigo != persona.codigo:
                            messagebox.showerror("Error", "El correo ingresado ya está en uso.")
                            return  # Detiene el proceso de modificación si el correo ya existe

                    persona.correo = correo_nuevo

                # Guardar los cambios en el archivo
                for i, p in enumerate(personas):
                    if p.codigo == persona.codigo:
                        personas[i] = persona
                guardar_personas(personas, archivo)

                messagebox.showinfo("Éxito", f"{opcion.get()} de {persona.codigo} actualizada correctamente.")
                ventana.destroy()
                crear_menu()

            # Botón regresar al menú
            btn_regresar = tk.Button(ventana_modificacion, text="Regresar al Menú",
                                     command=lambda: [ventana_modificacion.destroy(), crear_menu()],
                                     **estilo_boton_rosa)
            btn_regresar.pack(pady=5)

            ventana_modificacion.mainloop()

        else:
            messagebox.showerror("Error", "El ID ingresado no existe.")

    # Botones en la misma línea
    frame_botones = tk.Frame(ventana_modificar)
    frame_botones.pack(pady=10)

    # Botón Siguiente (inicialmente deshabilitado)
    btn_siguiente = tk.Button(frame_botones, text="Siguiente", command=buscar_persona, state=tk.DISABLED,
                              **estilo_boton_gris)
    btn_siguiente.pack(side="left", padx=10)

    # Habilitar el botón solo si hay texto
    def verificar_id_modificar(*args):
        if id_var.get().strip():
            btn_siguiente.config(state=tk.NORMAL, bg=estilo_boton_rosa["bg"], fg=estilo_boton_rosa["fg"])
        else:
            btn_siguiente.config(state=tk.DISABLED, bg=estilo_boton_gris["bg"], fg=estilo_boton_gris["fg"])

    id_var.trace_add('write', verificar_id_modificar)

    # Botón Regresar al Menú
    tk.Button(frame_botones, text="Regresar al Menú", command=lambda: [ventana_modificar.destroy(), crear_menu()],
              **estilo_boton_rosa).pack(side="left", padx=10)

    ventana_modificar.mainloop()


# ---------- Mostrar Personas ----------
def mostrar_personas():
    personas = leer_personas(archivo)
    if not personas:
        messagebox.showinfo("Mostrar Personas", "No hay personas registradas.")
        return

    ventana = tk.Toplevel()
    ventana.title("Personas Registradas")

    frame = tk.Frame(ventana)
    frame.pack(fill='both', expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#d9d9d9", foreground="black")

    tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Sexo", "Correo", "Edad"), show="headings")
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

    for persona in personas:
        tree.insert("", "end", values=(persona.codigo, persona.nombre, persona.sexo, persona.correo, persona.edad))

    ventana.mainloop()


# ---------- Eliminar Persona ----------
def eliminar_persona():
    personas = leer_personas(archivo)

    # Ventana para ingresar ID a eliminar
    ventana_eliminar = tk.Tk()
    ventana_eliminar.title("Eliminar Persona")

    ancho = 400
    alto = 250
    x = (ventana_eliminar.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_eliminar.winfo_screenheight() // 2) - (alto // 2)
    ventana_eliminar.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana_eliminar.resizable(False, False)

    tk.Label(ventana_eliminar, text="Ingrese el ID de la persona a eliminar:").pack(pady=10)

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

    def buscar_persona():
        id_buscar = id_var.get().strip()

        # Buscar si el ID existe
        persona_encontrada = next((p for p in personas if p.codigo == id_buscar), None)

        if persona_encontrada:
            # Crear ventana de confirmación
            ventana_confirmar = tk.Toplevel(ventana_eliminar)
            ventana_confirmar.title("Confirmar eliminación")

            # Centrar ventana de confirmación
            ancho_confirmar = 400
            alto_confirmar = 150
            x_confirmar = (ventana_confirmar.winfo_screenwidth() // 2) - (ancho_confirmar // 2)
            y_confirmar = (ventana_confirmar.winfo_screenheight() // 2) - (alto_confirmar // 2)
            ventana_confirmar.geometry(f"{ancho_confirmar}x{alto_confirmar}+{x_confirmar}+{y_confirmar}")
            ventana_confirmar.resizable(False, False)

            # Mensaje de confirmación
            tk.Label(
                ventana_confirmar,
                text=f"¿Está seguro de eliminar a la persona con ID {id_buscar}?\n"
                     f"Una vez eliminada no podrá recuperarse su información.",
                wraplength=350
            ).pack(pady=15)

            # Frame para botones
            frame_botones_confirmar = tk.Frame(ventana_confirmar)
            frame_botones_confirmar.pack(pady=10)

            # Función para confirmar eliminación
            def confirmar_eliminacion():
                # Eliminar la persona de la lista
                personas.remove(persona_encontrada)
                guardar_personas(personas, archivo)

                ventana_confirmar.destroy()
                messagebox.showinfo("Eliminación Exitosa", f"La persona con ID {id_buscar} ha sido eliminada.")
                ventana_eliminar.destroy()
                crear_menu()

            # Función para cancelar eliminación
            def cancelar_eliminacion():
                ventana_confirmar.destroy()
                messagebox.showinfo("Operación Cancelada", "La persona no ha sido eliminada.\n REGRESANDO AL MENU PUBLICO GENERAL!!!")
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
    btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=buscar_persona, state=tk.DISABLED,
                             **estilo_boton_gris)
    btn_eliminar.pack(side="left", padx=10)

    # Botón Regresar al Menú
    tk.Button(frame_botones, text="Regresar al Menú", command=lambda: [ventana_eliminar.destroy(), crear_menu()],
              **estilo_boton_rosa).pack(side="left", padx=10)

    ventana_eliminar.mainloop()

# ---------- Volver al submenu administrador ----------
def volver_a_submenu_admin():
    # Importamos aquí para evitar dependencia circular
    from sub_menu_administrador import crear_menu_administrador
    crear_menu_administrador()


# ---------- Ventana Principal / Menú ----------
def crear_menu():
    ventana = tk.Tk()
    ventana.title("Gestión de Personas")

    ancho = 300
    alto = 400
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    tk.Label(ventana, text="--- MENÚ DE PERSONAS ---", font=("Arial", 14)).pack(pady=10)
    tk.Button(ventana, text="Alta persona", command=lambda: alta_persona_ventana(ventana), **estilo_boton_menu).pack(
        pady=5)
    tk.Button(ventana, text="Mostrar personas", command=mostrar_personas, **estilo_boton_menu).pack(pady=5)
    tk.Button(ventana, text="Modificar persona", command=lambda: [ventana.destroy(), modificar_persona()],
              **estilo_boton_menu).pack(pady=5)
    tk.Button(ventana, text="Eliminar persona", command=lambda: [ventana.destroy(), eliminar_persona()],
              **estilo_boton_menu).pack(pady=5)
    tk.Button(ventana, text="Regresar al submenu administrador",
              command=lambda: [ventana.destroy(), volver_a_submenu_admin()], **estilo_boton_menu).pack(pady=20)

    ventana.mainloop()


# ---------- Ejecutar Programa desde otro archivo ----------
def ejecutar_submenu():
    crear_menu()


# ---------- Ejecutar Programa ----------
if __name__ == "__main__":
    crear_menu()