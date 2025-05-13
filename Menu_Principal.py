import tkinter as tk
from tkinter import messagebox

# -------- Estilo de botones del menú --------
estilo_boton_menu = {
    "bg": "#ffc0cb",  # Rosa
    "fg": "black",  # Texto negro
    "font": ("Arial", 12),
    "width": 20,
    "height": 2,
    "bd": 0
}


# -------- Centrar ventana --------
def centrar_ventana(ventana, width=400, height=300):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho - width) // 2
    y = (pantalla_alto - height) // 2
    ventana.geometry(f"{width}x{height}+{x}+{y}")


# -------- Salir del programa --------
def salir():
    messagebox.showinfo("Hasta pronto", "Muchas gracias por su visita!!")
    global root
    root.destroy()


# -------- Abrir ventana simulada para otros roles --------
def abrir_ventana(titulo, mensaje):
    global root
    root.destroy()

    ventana = tk.Tk()
    ventana.title(titulo)
    centrar_ventana(ventana, 400, 200)

    label = tk.Label(ventana, text=mensaje, font=("Arial", 14))
    label.pack(pady=30)

    def regresar():
        ventana.destroy()
        crear_menu_principal()

    boton_regresar = tk.Button(
        ventana,
        text="Regresar al menú principal",
        bg="#ffc0cb",
        fg="black",
        activebackground="gray",
        relief="groove",
        bd=2,
        font=("Arial", 10),
        width=25,
        height=2,
        command=regresar
    )
    boton_regresar.pack()

    ventana.mainloop()


# -------- Abrir submenu de administrador --------
def abrir_submenu_administrador():
    global root
    root.destroy()
    from sub_menu_administrador import crear_menu_administrador
    crear_menu_administrador()


# -------- Mostrar Menú Principal --------
def crear_menu_principal():
    global root
    root = tk.Tk()
    root.title("Menú Principal")
    centrar_ventana(root, 400, 400)

    label = tk.Label(root, text="Ingresa tu tipo de usuario", font=("Arial", 16))
    label.pack(pady=20)

    def crear_boton(texto, comando):
        boton = tk.Button(
            root,
            text=texto,
            width=25,
            height=2,
            bg="#ffc0cb",
            fg="black",
            activebackground="gray",
            relief="groove",
            bd=2,
            font=("Arial", 10),
            command=comando
        )
        boton.pack(pady=8)

    crear_boton("Administrador", abrir_submenu_administrador)
    crear_boton("Staff", lambda: abrir_ventana("Staff", "AQUÍ SE HACE LO DE STAFF"))

    # Ya no necesitamos esta función aquí
    # La funcionalidad de submenu de personas se moverá al submenu de administrador

    crear_boton("Público General", lambda: abrir_ventana("Público General", "Esta funcionalidad está desactivada"))
    crear_boton("Ponente", lambda: abrir_ventana("Ponente", "AQUÍ SE HACE LO DE PONENTE"))
    crear_boton("Salir", salir)

    root.mainloop()


# -------- Ejecutar --------
if __name__ == "__main__":
    crear_menu_principal()