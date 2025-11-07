import mysql.connector

def connexion_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          # par défaut sous XAMPP
            password="",          # vide sauf si tu as défini un mot de passe
            database="reservation_sportive"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur de connexion MySQL : {err}")
        return None