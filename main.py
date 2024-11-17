import mysql.connector
from mysql.connector import Error
import usuarios  # Importamos el módulo de usuarios

# Conexión a la base de datos
def conectar_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Cambia esto si tu base de datos está en otro host
            database='instagram',  # Reemplaza con el nombre de tu base de datos
            user='root',  # Reemplaza con tu usuario
            password='',  # Reemplaza con tu contraseña
            port="3306"
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Función para cerrar la conexión
def cerrar_conexion(connection):
    if connection and connection.is_connected():
        connection.close()
        print("Conexión cerrada.")

# Función para mostrar el menú principal
def mostrar_menu():
    print("\nMenú de opciones:")
    print("1. Crear Usuario")
    print("2. Mostrar Usuarios")
    print("3. Actualizar Usuario")
    print("4. Eliminar Usuario")
    print("5. Salir")

def main():
    connection = conectar_db()
    if not connection:
        return

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == '1':  # Crear Usuario
            print("\n--- Crear Usuario ---")
            nombre_usuario = input("Nombre de usuario: ")
            correo_electronico = input("Correo electrónico: ")
            contraseña_hash = input("Contraseña (en formato hash): ")
            nombre_completo = input("Nombre completo: ")
            biografia = input("Biografía (opcional): ")
            url_imagen_perfil = input("URL de la imagen de perfil (opcional): ")

            try:
                usuarios.crear_usuario(connection, nombre_usuario, correo_electronico, contraseña_hash, nombre_completo, biografia, url_imagen_perfil)
                print("Usuario creado exitosamente.")
            except Error as e:
                print("Error al crear el usuario:", e)

        elif opcion == '2':  # Mostrar Usuarios
            print("\n--- Lista de Usuarios ---")
            try:
                usuarios_list = usuarios.mostrar_usuarios(connection)
                if usuarios_list:
                    for usuario in usuarios_list:
                        print(f"ID: {usuario[0]}, Usuario: {usuario[1]}, Correo: {usuario[2]}, Nombre: {usuario[4]}")
                else:
                    print("No hay usuarios registrados.")
            except Error as e:
                print("Error al mostrar usuarios:", e)

        elif opcion == '3':  # Actualizar Usuario
            print("\n--- Actualizar Usuario ---")
            try:
                id_usuario = int(input("ID del usuario a actualizar: "))
                nuevo_nombre_usuario = input("Nuevo nombre de usuario (dejar vacío para no cambiar): ")
                nuevo_correo_electronico = input("Nuevo correo electrónico (dejar vacío para no cambiar): ")
                nueva_biografia = input("Nueva biografía (dejar vacío para no cambiar): ")
                nueva_url_imagen = input("Nueva URL de imagen (dejar vacío para no cambiar): ")

                # Si no hay cambios, no se realiza la actualización
                if not any([nuevo_nombre_usuario, nuevo_correo_electronico, nueva_biografia, nueva_url_imagen]):
                    print("No se realizaron cambios.")
                else:
                    usuarios.actualizar_usuario(connection, id_usuario, nuevo_nombre_usuario, nuevo_correo_electronico, nueva_biografia, nueva_url_imagen)
                    print("Usuario actualizado exitosamente.")
            except Error as e:
                print("Error al actualizar el usuario:", e)

        elif opcion == '4':  # Eliminar Usuario
            print("\n--- Eliminar Usuario ---")
            try:
                id_usuario = int(input("ID del usuario a eliminar: "))
                confirmacion = input(f"¿Estás seguro de eliminar al usuario con ID {id_usuario}? (s/n): ").lower()
                if confirmacion == 's':
                    usuarios.eliminar_usuario(connection, id_usuario)
                    print("Usuario eliminado exitosamente.")
                else:
                    print("Operación cancelada.")
            except Error as e:
                print("Error al eliminar el usuario:", e)

        elif opcion == '5':  # Salir
            cerrar_conexion(connection)
            break

        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()
