from app.database.db_management import SQLiteManagement


def init_database():
    with SQLiteManagement() as db:
        print("🖫 Inicializando la base de datos...")
        db.initialize()
        print("🖫 Base de datos inicializada")