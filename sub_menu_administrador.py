import tkinter as tk
from tkinter import messagebox

# -------- Estilo de botones del menú --------
estilo_boton_menu = {
    "bg": "#ffc0cb",  # Rosa
    "fg": "black",  # Texto negro
    "font": ("Arial", 10),
    "width": 25,
    "height": 2,
    "bd": 2,
    "relief": "groove",
    "activebackground": "gray"
}


# -------- Centrar ventana --------
def centrar_ventana(ventana, width=400, height=500):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho - width) // 2
    y = (pantalla_alto - height) // 2
    ventana.geometry(f"{width}x{height}+{x}+{y}")


# -------- Funciones de botones temporales --------
def funcion_temporal(titulo):
    messagebox.showinfo("Información", f"La función '{titulo}' será implementada próximamente.")


# -------- Abrir submenu de personas --------
def abrir_submenu_personas(ventana):
    ventana.destroy()
    from admin_persona import ejecutar_submenu
    ejecutar_submenu()

# -------- Abrir submenu de eventos --------
def abrir_submenu_eventos(ventana):
    ventana.destroy()
    from admin_event import ejecutar_submenu
    ejecutar_submenu()
# -------- Regresar al menú principal --------
def regresar_menu_principal(ventana):
    ventana.destroy()
    from Menu_Principal import crear_menu_principal
    crear_menu_principal()


# -------- Mostrar Menú de Administrador --------
def crear_menu_administrador():
    ventana_admin = tk.Tk()
    ventana_admin.title("Menú de Administrador")
    centrar_ventana(ventana_admin, 400, 500)

    # Título del menú
    label = tk.Label(ventana_admin, text="Panel de Administrador", font=("Arial", 16))
    label.pack(pady=20)

    # Crear botones para el menú de administrador
    opciones = [
        "Solicitudes de Activación de Cuenta",
        "Eventos",
        "Público",
        "Staff",
        "Ponentes",
        "Cambiar Contraseña",
        "Regresar al Menú Principal"
    ]

    for i, opcion in enumerate(opciones):
        if opcion == "Regresar al Menú Principal":
            boton = tk.Button(
                ventana_admin,
                text=opcion,
                **estilo_boton_menu,
                command=lambda: regresar_menu_principal(ventana_admin)
            )
        elif opcion == "Público":
            boton = tk.Button(
                ventana_admin,
                text=opcion,
                **estilo_boton_menu,
                command=lambda: abrir_submenu_personas(ventana_admin)
            )
        elif opcion == "Eventos":
            from admin_event import crear_menu as abrir_menu_eventos
            boton = tk.Button(
                ventana_admin,
                text=opcion,
                **estilo_boton_menu,
                command=lambda: abrir_submenu_eventos(ventana_admin)
            )

        else:
            boton = tk.Button(
                ventana_admin,
                text=opcion,
                **estilo_boton_menu,
                command=lambda titulo=opcion: funcion_temporal(titulo)
            )
        boton.pack(pady=8)

    ventana_admin.mainloop()


# -------- Ejecutar --------
if __name__ == "__main__":
    crear_menu_administrador()