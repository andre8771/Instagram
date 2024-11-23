import mysql.connector
from mysql.connector import Error
from usuarios import Usuario  # Importamos la clase Usuario
from seguidores import Seguir
from publicaciones import Publicaciones
from historias import Historias  # Importamos la clase Historias

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
        print("4. Crear historia")  # Nueva opción para crear historia
        print("5. Cerrar sesión")
        
    def mostrar_menu_seguidores(self):
        """Muestra el menú de seguidores."""
        print("Menu seguidores")
        print("1. Seguir a alguien")
        print("2. Ver perfil")
        print("3. Salir")
        
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

    def ejecutar_menu_historia(self):
        """Ejecuta el menú de Historias"""
        historia_obj = Historias(self.connection)

        while True:
            print("\n--- Menú de Historias ---")
            print("1. Ingresar datos para la historia")
            print("2. Volver al menú anterior")
            
            opcion = input("Selecciona una opción: ")
            
            if opcion == "1":
                # Crear historia
                id_usuario = self.usuario_actual["id_usuario"]
                imagen_video = input("URL de la imagen/video: ")
                texto = input("Texto opcional: ")
                duracion = int(input("Duración (en segundos, por defecto 15): ") or 15)
                historia_obj.crear_historia(id_usuario, imagen_video, texto, duracion)

            elif opcion == "2":
                # Regresar al menú anterior
                break

            else:
                print("Opción no válida, intenta de nuevo.")

    def ejecutar_menu_seguidores(self):
        while True:
            self.mostrar_menu_seguidores()
            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                seguir = Seguir(self.connection)
                usuario_seguido = input("Ingrese el ID del usuario a seguir: ")
                seguir.seguir_usuario(self.usuario_actual["id_usuario"], usuario_seguido)
            elif opcion == "2":
                id_perfil = input("Ingrese el ID del perfil que desea ver: ")
                publicaciones = Publicaciones(self.connection)
                publicaciones.ver_publicaciones(id_usuario=id_perfil)
                historias = Historias(self.connection)
                historias.ver_historias(id_usuario=id_perfil)
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
                while True:
                    print("\n--- Editar Perfil ---")
                    print("1. Editar información del perfil")
                    print("2. Editar una publicación")
                    print("3. Eliminar una publicación")
                    print("4. Eliminar historias")  # Nueva opción para eliminar historias
                    print("5. Regresar al menú anterior")

                    subopcion = input("Elige una opción: ")

                    if subopcion == '1':  # Editar información del perfil
                        nuevo_nombre_usuario = input("Ingrese el nuevo nombre de usuario (opcional): ").strip()
                        nueva_foto_perfil = input("Ingrese la URL de la nueva foto de perfil (opcional): ").strip()
                        nueva_biografia = input("Ingrese la nueva biografía (opcional): ").strip()

                        usuario = Usuario(self.connection)
                        usuario.actualizar_perfil(
                            id_usuario=self.usuario_actual["id_usuario"],
                            nuevo_nombre_usuario=nuevo_nombre_usuario if nuevo_nombre_usuario else None,
                            nueva_foto_perfil=nueva_foto_perfil if nueva_foto_perfil else None,
                            nueva_biografia=nueva_biografia if nueva_biografia else None
                        )
                    elif subopcion == '2':  # Editar una publicación
                         print("\n--- Editar Publicación ---")
                         id_publicacion = input("Ingrese el ID de la publicación que desea actualizar: ")
                         nuevo_contenidos = input("Ingrese el nuevo contenido (descripción): ")
                         nuevos_hashtags = input("Ingrese los nuevos hashtags (separados por comas, opcional): ").strip()

                         publicaciones = Publicaciones(self.connection)
                         publicaciones.actualizar_publicacion(
                             id_publicacion=id_publicacion,
                             nuevo_contenidos=nuevo_contenidos,
                             nuevo_hashtags=nuevos_hashtags if nuevos_hashtags else None
                        )
                        
                    elif subopcion == '3':  # Eliminar una publicación
                        try:
                              print("\n--- Eliminar Publicación ---")
                              id_publicacion = input("Ingrese el ID de la publicación que desea eliminar: ")

                              publicaciones = Publicaciones(self.connection)
                              publicaciones.eliminar_publicacion(id_publicacion)
                        except Exception as e:
                              print(f"Error inesperado al intentar eliminar la publicación: {e}")

                    elif subopcion == '4':  # Eliminar historias
                        historia_obj = Historias(self.connection)
                        id_historia = int(input("ID de la historia a eliminar: "))
                        historia_obj.eliminar_historia(id_historia)
                    elif subopcion == '5':  # Regresar al menú anterior
                        break
                    else:
                        print("Opción no válida, intenta de nuevo.")

            elif opcion == '3':  # Hacer una publicación
                print("\n--- Crear Publicación ---")
                url_imagen = input("URL de la imagen (opcional): ")
                descripcion = input("Descripción: ")
                hashtags = input("Hashtags (separados por comas): ")
                
                publicaciones = Publicaciones(self.connection)
                publicaciones.hacer_publicacion(
                    id_usuario=self.usuario_actual["id_usuario"],
                    url_imagen=url_imagen,
                    descripcion=descripcion,
                    hashtags=hashtags.strip()  
                )
            elif opcion == '4':  # Crear historia
                self.ejecutar_menu_historia()  # Llamar al menú de historias
            elif opcion == '5':  # cerrar sesión
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
Instagram = InstagramApp()
Instagram.run()