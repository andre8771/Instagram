#CREATE PUBLICACIONES:
class Publicaciones: 
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = conexion.cursor(dictionary=True)

    def hacer_publicacion(self, id_usuario, url_imagen, descripcion, hashtags):
        """
        Crea una nueva publicación para un usuario.
        
        """
        try:
            # Validaciones básicas
            if not descripcion.strip():
                print("La descripción no puede estar vacía.")
                return
            
            # Insertar la publicación en la base de datos
            query_publicacion = """
            INSERT INTO publicaciones (id_usuario, url_imagen, descripcion, hashtags, fecha_creacion)
            VALUES (%s, %s, %s, %s, NOW())
            """
            self.cursor.execute(query_publicacion, (id_usuario, url_imagen, descripcion, hashtags))
            self.conexion.commit()

            print("¡Publicación creada exitosamente!")

        except Exception as e:
            print("Error al hacer la publicación:", e)

#READ PUBLICACIONES:
    def ver_publicaciones(self, id_usuario):
        """
        Muestra todas las publicaciones de un perfil específico.
        
        """
        try:
            # Consulta para obtener las publicaciones
            query = """
            SELECT 
                url_imagen, 
                descripcion, 
                hashtags, 
                fecha_creacion
            FROM publicaciones
            WHERE id_usuario = %s
            ORDER BY fecha_creacion DESC
            """
            self.cursor.execute(query, (id_usuario,))
            publicaciones = self.cursor.fetchall()

            # Validar si existen publicaciones
            if publicaciones:
                print(f"\nPublicaciones del usuario con ID {id_usuario}:")
                for pub in publicaciones:
                    print(f"- Imagen/Video: {pub['url_imagen']}")
                    print(f"  Descripción: {pub['descripcion']}")
                    print(f"  Hashtags: {pub['hashtags']}")
                    print(f"  Fecha de creación: {pub['fecha_creacion']}\n")
            else:
                print(f"No existen publicaciones para el usuario con ID {id_usuario}.")
        except Exception as e:
            print("Error al consultar las publicaciones:", e)

#UPDATE PUBLICACIONES:
    def actualizar_publicacion(self, id_publicacion, nuevo_contenidos, nuevo_hashtags=None):
        """
        Actualiza una publicación existente.
       
        """
        try:
            # Verificar si la publicación existe
            query_existencia = "SELECT * FROM publicaciones WHERE id_publicacion = %s"
            self.cursor.execute(query_existencia, (id_publicacion,))
            publicacion = self.cursor.fetchone()

            if not publicacion:
                print(f"No existe una publicación con ID {id_publicacion}.")
                return

            # Construir la consulta de actualización
            query = "UPDATE publicaciones SET descripcion = %s"
            valores = [nuevo_contenidos]

            if nuevo_hashtags:
                query += ", hashtags = %s"
                valores.append(nuevo_hashtags)

            query += " WHERE id_publicacion = %s"
            valores.append(id_publicacion)

            # Ejecutar la actualización
            self.cursor.execute(query, tuple(valores))
            self.conexion.commit()

            print(f"Publicación con ID {id_publicacion} actualizada exitosamente.")
        except Exception as e:
            print(f"Error al actualizar la publicación: {e}")

#DELETE publicaciones
    def eliminar_publicacion(self, id_publicacion):
        """
        Elimina una publicación existente.
        
        """
        try:
            # Verificar si la publicación existe
            query_existencia = "SELECT * FROM publicaciones WHERE id_publicacion = %s"
            self.cursor.execute(query_existencia, (id_publicacion,))
            publicacion = self.cursor.fetchone()

            if not publicacion:
                print(f"No existe una publicación con ID {id_publicacion}.")
                return

            # Eliminar la publicación
            query_eliminar = "DELETE FROM publicaciones WHERE id_publicacion = %s"
            self.cursor.execute(query_eliminar, (id_publicacion,))
            self.conexion.commit()

            print(f"Publicación con ID {id_publicacion} eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la publicación: {e}")




     





