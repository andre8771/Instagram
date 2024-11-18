class Publicaciones:
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = conexion.cursor(dictionary=True)

    def hacer_publicacion(self, id_usuario, url_imagen, descripcion, etiquetas):
        try:
            # Insertar la publicación
            query_publicacion = """
            INSERT INTO publicaciones (id_usuario, url_imagen, descripcion)
            VALUES (%s, %s, %s)
            """
            self.cursor.execute(query_publicacion, (id_usuario, url_imagen, descripcion))
            self.conexion.commit()
            id_publicacion = self.cursor.lastrowid  # Obtener el ID de la publicación creada

            # Manejar las etiquetas
            for etiqueta in etiquetas:
                # Verificar si la etiqueta ya existe
                query_etiqueta = "SELECT id_etiqueta FROM etiquetas WHERE nombre_etiqueta = %s"
                self.cursor.execute(query_etiqueta, (etiqueta,))
                resultado = self.cursor.fetchone()

                if resultado:
                    id_etiqueta = resultado['id_etiqueta']
                else:
                    # Insertar nueva etiqueta
                    query_insert_etiqueta = "INSERT INTO etiquetas (nombre_etiqueta) VALUES (%s)"
                    self.cursor.execute(query_insert_etiqueta, (etiqueta,))
                    self.conexion.commit()
                    id_etiqueta = self.cursor.lastrowid

                # Relacionar la publicación con la etiqueta
                query_publicacion_etiqueta = """
                INSERT INTO publicacion_etiqueta (id_publicacion, id_etiqueta)
                VALUES (%s, %s)
                """
                self.cursor.execute(query_publicacion_etiqueta, (id_publicacion, id_etiqueta))

            self.conexion.commit()
            print("Publicación y etiquetas agregadas exitosamente.")
        except Exception as e:
            print("Error al hacer la publicación:", e)
