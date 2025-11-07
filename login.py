from tkinter import *  
import customtkinter as ctk  # pour des interfaces modernes 
from tkinter import messagebox  # affichage de boites de dialogue 
from PIL import Image, ImageTk  # manipulation d'images
import p2  # votre fichier p2.py avec la fonction main()
import mysql.connector
def connexion_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",         
            password="",         
            database="reservation_sportive"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur de connexion MySQL : {err}")
        return None
# Fonction de validation
def valider():
    utilisateur = entry_user.get().strip()
    mot_de_passe = entry_pass.get().strip()
    
    if utilisateur == "" or mot_de_passe == "":
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return
    
    conn = connexion_db()
    if conn is None:
        messagebox.showerror("Erreur", "Connexion à la base de données échouée.")
        return

    cursor = conn.cursor()
    
    try:
        # Vérifier si l'utilisateur existe déjà
        cursor.execute("SELECT * FROM utilisateurs WHERE nom_utilisateur = %s", (utilisateur,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
        else:
            # Insérer un nouvel utilisateur
            cursor.execute(
                "INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe) VALUES (%s, %s)",
                (utilisateur, mot_de_passe)
            )
            conn.commit()
            messagebox.showinfo("Succès", f"Utilisateur {utilisateur} enregistré avec succès !")

            fenetre.destroy()
            p2.main()

    except mysql.connector.Error as err:
        messagebox.showerror("Erreur SQL", f"Erreur : {err}")
    finally:
        cursor.close()
        conn.close()

# Initialisation de la fenêtre principale 
fenetre = Tk()
fenetre.title("Connexion - Réservation sportive")

# Plein écran automatique 
fenetre.state('zoomed')
fenetre.update_idletasks()

# Fond avec image 
try:
    image = Image.open("background.jpg")
    image = image.resize((fenetre.winfo_width(), fenetre.winfo_height()))  # redimensionne sans flou
    bg_photo = ImageTk.PhotoImage(image)
    
    bg_canvas = Canvas(fenetre, highlightthickness=0)
    bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
    bg_canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    bg_canvas.image = bg_photo

except:
    fenetre.configure(bg="white")

# Frame principal
frame = ctk.CTkFrame(
    fenetre,
    width=300,
    height=220,
    fg_color="white",
    border_width=1,
    border_color="lightgray"
)
frame.place(relx=0.5, rely=0.5, anchor="center")

# --- Titre ---
label_title = ctk.CTkLabel(
    frame,
    text="Connexion",
    text_color="black",
    font=("Arial", 16, "bold")
)
label_title.place(relx=0.5, y=25, anchor="center")

# Champ utilisateur
entry_user = ctk.CTkEntry(
    frame,
    width=220,
    height=38,
    placeholder_text="Nom d'utilisateur",
    placeholder_text_color="gray",
    corner_radius=15,
    border_width=1,
    border_color="lightgray",
    fg_color="#f2f2f2",
    text_color="black",
    font=("Arial", 12)
)
entry_user.place(relx=0.5, y=65, anchor="center")

# Champ mot de passe 
entry_pass = ctk.CTkEntry(
    frame,
    width=220,
    height=38,
    placeholder_text="Mot de passe",
    placeholder_text_color="gray",
    show="*",
    corner_radius=15,
    border_width=1,
    border_color="lightgray",
    fg_color="#f2f2f2",
    text_color="black",
    font=("Arial", 12)
)
entry_pass.place(relx=0.5, y=115, anchor="center")

# Bouton connexion 
bouton = ctk.CTkButton(
    frame,
    text="Se connecter",
    width=160,
    height=38,
    corner_radius=18,
    fg_color="#F77F00",
    hover_color="#E57100",
    text_color="white",
    font=("Arial", 12, "bold"),
    command=valider
)
bouton.place(relx=0.5, y=170, anchor="center")

# Touche Entrée
fenetre.bind("<Return>", lambda e: valider())

fenetre.mainloop()