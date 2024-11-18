import mysql.connector
from mysql.connector import Error
from usuarios import Usuario  # Importamos la clase Usuario
from seguidores import Seguir
class InstagramApp:
    def __init__(self):
        self.connection = None
        self.usuario_actual = None  # Variable para guardar el usuario autenticado
       
    def conectar_db(self):
        # Establecemos conexión con la BD
        try:
            self.connection = mysql.connector.connect(
                host='localhost',  
                database='instagram',
                user='root',  
                password='',  
                port="3306"
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
        except Error as e:
            print("Error al conectar a la base de datos:", e)
            self.connection = None

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")

    def mostrar_menu_principal(self):
        """Muestra el menú principal."""
        print("\nMenú Principal:")
        print("1. Iniciar Sesión")
        print("2. Crear Cuenta")
        print("3. Salir")

    def mostrar_menu_usuario(self):
        """Muestra el menú para usuarios autenticados."""
        print(f"\nBienvenido, {self.usuario_actual['nombre_usuario']}!")
        print("Opciones:")
        print("1. Ver perfiles")
        print("2. Editar perfil")
        print("3. Hacer una publicación")
        print("4. Cerrar sesión")
        
    def mostrar_menu_seguidores(self):
        print("Menu seguidores")
        print("1.Seguir a alguien")
        print("2.Ver perfil")
        print("3.Salir")
        
    def iniciar_sesion(self):
        """Permite a un usuario iniciar sesión."""
        try:
            usuario = input("Nombre de usuario: ")
            contraseña = input("Contraseña: ")

            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña_hash = %s"
            cursor.execute(query, (usuario, contraseña))
            resultado = cursor.fetchone()

            if resultado:
                
                self.usuario_actual = resultado  # Guarda el usuario autenticado
                return True
            else:
                print("Nombre de usuario o contraseña incorrectos.")
        except Exception as e:
            print("Error al iniciar sesión:", e)
        return False

    def crear_cuenta(self):
        """Permite crear un nuevo usuario."""
        try:
            nombre_usuario = input("Nombre de usuario: ")
            correo_electronico = input("Correo electrónico: ")
            contraseña_hash = input("Contraseña: ")  # En un entorno real, deberías encriptarla.
            url_imagen_perfil = input("URL de la imagen de perfil (opcional): ")

            usuario = Usuario(self.connection)
            usuario.crear_perfil(
                nombre_usuario=nombre_usuario,
                correo_electronico=correo_electronico,
                contraseña_hash=contraseña_hash,
                url_imagen_perfil=url_imagen_perfil
            )
        except Exception as e:
            print("Error al crear la cuenta:", e)
    def ejecutar_menu_seguidores(self):
        while True:
            self.mostrar_menu_seguidores()
            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                seguir=Seguir(self.connection)
                usuario_seguido=input("ingrese el ID del usuario ")
                seguir.seguir_usuario(self.usuario_actual["id_usuario"],usuario_seguido)
            elif opcion == "2":
                pass
            elif opcion == "3":
                self.ejecutar_menu_usuario()
                break
    
    def ejecutar_menu_usuario(self):
        """Ejecuta el menú del usuario autenticado."""
        while True:
            self.mostrar_menu_usuario()
            opcion = input("Elige una opción: ")

            if opcion == '1':  # Ver perfiles
                usuario = Usuario(self.connection)
                usuario.ver_perfiles()
                self.ejecutar_menu_seguidores()
                break
            elif opcion == '2':  # Editar perfil
                print("Función de edición de perfil no implementada todavía.")
            elif opcion == '3':  #publicar
                pass
            elif opcion == '4':  # Cerrar sesión
                print(f"Sesión cerrada. Adiós, {self.usuario_actual['nombre_usuario']}!")
                self.usuario_actual = None
                break
            else:
                print("Opción no válida, intenta de nuevo.")

    def ejecutar_opcion_de_menu_principal(self, opcion):
        """Ejecuta la opción seleccionada del menú principal."""
        if opcion == '1':  # Iniciar Sesión
            if self.iniciar_sesion():
                self.ejecutar_menu_usuario()
        elif opcion == '2':  # Crear Cuenta
            self.crear_cuenta()
        elif opcion == '3':  # Salir
            self.cerrar_conexion()
            return False
        else:
            print("Opción no válida, intenta de nuevo.")
        return True

    def run(self):
        self.conectar_db()
        if not self.connection:
            return

        while True:
            if self.usuario_actual:  # Si el usuario está autenticado
                self.ejecutar_menu_usuario()
            else:
                self.mostrar_menu_principal()
                opcion = input("Elige una opción: ")
                if not self.ejecutar_opcion_de_menu_principal(opcion):
                    break

Instagram=InstagramApp()
Instagram.run()

