class Historias:
    def __init__(self, connection):
        self.connection = connection

    def crear_historia(self, id_usuario, imagen_video, texto, duracion):
        """Crear una nueva historia"""
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO historias (id_usuario, imagen_video, texto, duracion)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_usuario, imagen_video, texto, duracion))
            self.connection.commit()
            print("Historia creada con éxito.")
        except Exception as e:
            print("Error al crear la historia:", e)

    def eliminar_historia(self, id_historia):
        """Eliminar una historia"""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM historias WHERE id_historia = %s"
            cursor.execute(query, (id_historia,))
            self.connection.commit()
            print("Historia eliminada con éxito.")
        except Exception as e:
            print("Error al eliminar la historia:", e)

    def ver_historias(self, id_usuario):
        """Ver las historias del usuario autenticado"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT 
                id_historia, 
                imagen_video, 
                texto, 
                duracion, 
                fecha_creacion
            FROM historias 
            WHERE id_usuario = %s
            ORDER BY fecha_creacion DESC
            """
            cursor.execute(query, (id_usuario,))
            historias = cursor.fetchall()

            # Validar si existen historias
            if historias:
                print(f"\nHistorias del usuario con ID {id_usuario}:")
                for historia in historias:
                    print(f"ID: {historia['id_historia']}")
                    print(f"Imagen/Video: {historia['imagen_video']}")
                    print(f"Texto: {historia['texto']}")
                    print(f"Duración: {historia['duracion']} segundos")
                    print(f"Fecha de creación: {historia['fecha_creacion']}\n")
            else:
                print(f"No existen historias para el usuario con ID {id_usuario}.")
        except Exception as e:
            print("Error al consultar las historias:", e)