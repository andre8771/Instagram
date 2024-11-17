class Usuario:
    def __init__(self, conexion):
        self.conexion = conexion

    # Crear un nuevo perfil
    def crear_perfil(self, nombre_usuario, correo_electronico, contraseña_hash, url_imagen_perfil):
        try:
            cursor = self.conexion.cursor()
            query = """
            INSERT INTO usuarios (nombre_usuario, correo_electronico, contraseña_hash, url_imagen_perfil)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre_usuario, correo_electronico, contraseña_hash, url_imagen_perfil))
            self.conexion.commit()
            print(f"Perfil '{nombre_usuario}' creado exitosamente.")
        except Exception as e:
            print("Error al crear el perfil:", e)

    # Ver todos los perfiles con filtros
    def ver_perfiles(self, filtro_nombre=None, ordenar_por_popularidad=False):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            query = """
            SELECT id_usuario, nombre_usuario, url_imagen_perfil,
                   (SELECT COUNT(*) FROM seguidores WHERE id_seguido = usuarios.id_usuario) AS seguidores,
                   (SELECT COUNT(*) FROM publicaciones WHERE id_usuario = usuarios.id_usuario) AS publicaciones
            FROM usuarios
            """
            if filtro_nombre:
                query += " WHERE nombre_usuario LIKE %s"
                cursor.execute(query, (f"%{filtro_nombre}%",))
            else:
                cursor.execute(query)

            perfiles = cursor.fetchall()
            if ordenar_por_popularidad:
                perfiles.sort(key=lambda x: x['seguidores'], reverse=True)

            if perfiles:
                print("\nLista de perfiles:")
                for perfil in perfiles:
                    print(f"ID: {perfil['id_usuario']}, Usuario: {perfil['nombre_usuario']}, "
                          f"Seguidores: {perfil['seguidores']}, Publicaciones: {perfil['publicaciones']}")
            else:
                print("No se encontraron perfiles.")
        except Exception as e:
            print("Error al visualizar los perfiles:", e)

    # Actualizar un perfil
    def actualizar_perfil(self, id_usuario, nuevo_nombre_usuario=None, nueva_foto_perfil=None, nueva_biografia=None):
        try:
            cursor = self.conexion.cursor()
            campos = []
            valores = []

            if nuevo_nombre_usuario:
                campos.append("nombre_usuario = %s")
                valores.append(nuevo_nombre_usuario)
            if nueva_foto_perfil:
                campos.append("url_imagen_perfil = %s")
                valores.append(nueva_foto_perfil)
            if nueva_biografia:
                campos.append("biografia = %s")
                valores.append(nueva_biografia)

            if campos:
                query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = %s"
                valores.append(id_usuario)
                cursor.execute(query, valores)
                self.conexion.commit()
                print(f"Perfil con ID {id_usuario} actualizado exitosamente.")
            else:
                print("No se proporcionaron datos para actualizar.")
        except Exception as e:
            print("Error al actualizar el perfil:", e)

    # Eliminar un perfil
    def eliminar_perfil(self, id_usuario):
        try:
            cursor = self.conexion.cursor()
            # Verificar si el perfil existe
            query_check = "SELECT * FROM usuarios WHERE id_usuario = %s"
            cursor.execute(query_check, (id_usuario,))
            perfil = cursor.fetchone()

            if perfil:
                query = "DELETE FROM usuarios WHERE id_usuario = %s"
                cursor.execute(query, (id_usuario,))
                self.conexion.commit()
                print(f"Perfil con ID {id_usuario} eliminado exitosamente.")
            else:
                print(f"No se encontró un perfil con ID {id_usuario}.")
        except Exception as e:
            print("Error al eliminar el perfil:", e)
