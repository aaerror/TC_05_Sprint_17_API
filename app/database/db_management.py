from app.database.config import DATABASE_PATH, DATABASE_SCHEME
from typing import List, Sequence

import sqlite3


class SQLiteManagement:
    def __init__(self, path: str = DATABASE_PATH):
        if path is None:
            raise ValueError("Path vacío o incompleto.")

        self.path = path
        self.__connection = None


    def __enter__(self):
        print(f"Abriendo conexión a '{self.path}'")
        self.__connection = sqlite3.connect(self.path)
        self.__connection.row_factory = sqlite3.Row

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if self.__connection:
            print("Cerrando la conexión a la base de datos.")
            self.__connection.close()
            self.__connection = None

        return False

    def _get_cursor(self) -> sqlite3.Cursor:
        if not self.__connection:
            msg = "Utilizar context manager para crear una conexión."
            raise ValueError(msg)

        return self.__connection.cursor()


    def initialize(self, path: str = DATABASE_SCHEME) -> None:
        if not path:
            msg = "Path sin especificar o inválido."
            raise ValueError(msg)

        try:
            with open(path, "r", encoding="utf-8") as f:
                script = f.read()

            cursor = self._get_cursor()
            cursor.executescript(script)
            self.__connection.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Error: {e}")


    def execute(self, query: str) -> None:
        """
        Data Definition Language
        """
        if not query:
            raise ValueError("Consulta vacía o inexistente.")

        try:
            cursor = self._get_cursor()
            cursor.execute(query)
            self.__connection.commit()
        except sqlite3.Error as e:
            raise ValueError(f"Error: {e}")


    def query(self, query: str, params: Sequence | None = None) -> List:
        if not query:
            raise ValueError("Consulta vacía o inexistente.")

        try:
            cursor = self._get_cursor()
            cursor.execute(query, params or ())
            rows = cursor.fetchall()

            # columns = [
            #     column[0] for column in cursor.description
            # ] if cursor.description else []

            # return [dict(row) for row in rows]
            # return cursor.rowcount()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            raise ValueError(f"Error al procesar la consulta: {e}")