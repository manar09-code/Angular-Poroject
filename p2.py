from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import date
import customtkinter as ctk
import mysql.connector  # ✅ Connexion MySQL (XAMPP)

def main():
    fenetre = Tk()
    fenetre.title("Système de Réservation Sportive")
    fenetre.geometry("1100x700")
    fenetre.configure(bg="white")

    # --- DATABASE SETUP ---
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Laisse vide si tu n’as pas mis de mot de passe
        database="reservations_sportive"  # ⚠️ Vérifie que le nom de la base correspond bien à ta base phpMyAdmin
    )
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(100),
        date_r VARCHAR(20),
        heure VARCHAR(20),
        terrain VARCHAR(50)
    )
    """)
    conn.commit()

    # --- FRAME 1 : Choix du terrain ---
    frame1 = LabelFrame(fenetre, text="Choisissez un terrain/salle", font=("Arial", 12, "bold"), bg="white")
    frame1.pack(pady=10, padx=10, fill="x")

    terrain = StringVar(value="")

    def create_terrain(parent, img_path, text, col):
        img = Image.open(img_path)
        img = img.resize((280, 220))
        img = ImageTk.PhotoImage(img)
        frame = Frame(parent, bg="#F77F00")
        frame.grid(row=0, column=col, padx=8, pady=10)

        lbl_img = Label(frame, image=img, bg="#F77F00")
        lbl_img.image = img
        lbl_img.pack()

        lbl_title = Label(frame, text=text, font=("Arial", 10, "bold"), bg="#F77F00")
        lbl_title.pack(pady=2)

        rb = Radiobutton(frame, variable=terrain, value=text, bg="#F77F00", text="")
        rb.pack(pady=3)

    create_terrain(frame1, "foot.jpg", "Terrain de Football", 0)
    create_terrain(frame1, "basketball.jpg", "Terrain de Basketball", 1)
    create_terrain(frame1, "tennis.jpg", "Terrain de Tennis", 2)
    create_terrain(frame1, "handball.jpg", "Salle de Handball", 3)
    create_terrain(frame1, "padel.jpg", "Terrain de Padel", 4)

    # --- FRAME 2 : Formulaire ---
    frame2 = LabelFrame(fenetre, text="Formulaire de Réservation", font=("Arial", 12, "bold"), bg="white")
    frame2.pack(pady=10, padx=10, fill="x")

    Label(frame2, text="Nom complet :", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    nom_entry = ctk.CTkEntry(frame2, width=300, height=35, corner_radius=10, fg_color="#f2f2f2",
                             text_color="black", placeholder_text="Nom complet", font=("Arial", 12))
    nom_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(frame2, text="Date de réservation :", font=("Arial", 11), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    date_entry = ctk.CTkEntry(frame2, width=300, height=35, corner_radius=10, fg_color="#f2f2f2",
                              text_color="black", placeholder_text="JJ/MM/AAAA", font=("Arial", 12))
    date_entry.grid(row=1, column=1, padx=10, pady=5)
    date_entry.insert(0, date.today().strftime("%d/%m/%Y"))

    Label(frame2, text="Heure :", font=("Arial", 11), bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    hours = ["08:00-10:00", "10:00-12:00", "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00", "23:00-01:00"]
    heure_combo = ctk.CTkComboBox(frame2, values=hours, width=300, height=35, corner_radius=10, font=("Arial", 12))
    heure_combo.grid(row=2, column=1, padx=10, pady=5)

    # --- FRAME boutons ---
    frame_btn = Frame(fenetre, bg="white")
    frame_btn.pack(pady=20)

    # --- FRAME 3 : Recherche centrée + Liste ---
    frame_search = Frame(fenetre, bg="white")
    frame_search.pack(pady=5, padx=10, fill="x")

    inner_search = Frame(frame_search, bg="white")
    inner_search.pack(anchor="center")

    Label(inner_search, text="Rechercher :", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=5, pady=5)
    search_entry = ctk.CTkEntry(inner_search, width=300, height=35, corner_radius=10, fg_color="#f2f2f2",
                                text_color="black", placeholder_text="Cherche par Nom ou Date", font=("Arial", 12))
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    def rechercher():
        search = search_entry.get()
        for item in tree.get_children():
            tree.delete(item)
        if search:
            cursor.execute("""
                SELECT nom, date_r, heure, terrain 
                FROM reservations 
                WHERE nom LIKE %s OR date_r LIKE %s
            """, (f"%{search}%", f"%{search}%"))
        else:
            cursor.execute("SELECT nom, date_r, heure, terrain FROM reservations")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    btn_search = ctk.CTkButton(inner_search, text="Rechercher", command=rechercher,
                               fg_color="#F77F00", text_color="black", corner_radius=15,
                               width=130, height=40, font=("Arial", 12, "bold"))
    btn_search.grid(row=0, column=2, padx=10, pady=5)

    frame3 = LabelFrame(fenetre, text="Liste des Réservations", font=("Arial", 12, "bold"), bg="white")
    frame3.pack(pady=10, padx=10, fill="both", expand=True)

    tree = ttk.Treeview(frame3, columns=("Nom", "Date", "Heure", "Terrain"), show="headings", height=6)
    tree.heading("Nom", text="Nom complet")
    tree.heading("Date", text="Date de réservation")
    tree.heading("Heure", text="Heure")
    tree.heading("Terrain", text="Terrain")
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    # --- FONCTIONS ---
    def load_data():
        for item in tree.get_children():
            tree.delete(item)
        cursor.execute("SELECT nom, date_r, heure, terrain FROM reservations")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def ajouter_reservation():
        nom = nom_entry.get()
        date_r = date_entry.get()
        heure = heure_combo.get()
        terr = terrain.get()

        if nom and heure and terr:
            cursor.execute("""
                INSERT INTO reservations (nom, date_r, heure, terrain)
                VALUES (%s, %s, %s, %s)
            """, (nom, date_r, heure, terr))
            conn.commit()
            print("✅ Données insérées :", nom, date_r, heure, terr)
            load_data()
            messagebox.showinfo("Succès", "Réservation ajoutée avec succès !")
            nom_entry.delete(0, END)
            heure_combo.set("")
            terrain.set("")
        else:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs avant d’ajouter une réservation.")

    def modifier_reservation():
        selected = tree.selection()
        if selected:
            nom = nom_entry.get()
            date_r = date_entry.get()
            heure = heure_combo.get()
            terr = terrain.get()
            old_values = tree.item(selected, "values")
            cursor.execute("""UPDATE reservations SET nom=%s, date_r=%s, heure=%s, terrain=%s 
                              WHERE nom=%s AND date_r=%s AND heure=%s AND terrain=%s""",
                           (nom, date_r, heure, terr, *old_values))
            conn.commit()
            load_data()

    def supprimer_reservation():
        selected = tree.selection()
        if selected:
            confirm = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette réservation ?")
            if confirm:
                values = tree.item(selected, "values")
                cursor.execute("DELETE FROM reservations WHERE nom=%s AND date_r=%s AND heure=%s AND terrain=%s", values)
                conn.commit()
                load_data()

    def selected_item(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected, "values")
            nom_entry.delete(0, END)
            nom_entry.insert(0, values[0])
            date_entry.delete(0, END)
            date_entry.insert(0, values[1])
            heure_combo.set(values[2])
            terrain.set(values[3])

    tree.bind("<<TreeviewSelect>>", selected_item)

    # --- BOUTONS ---
    btn_ajouter = ctk.CTkButton(frame_btn, text="Ajouter", command=ajouter_reservation,
        fg_color="#F77F00", text_color="black", corner_radius=20, width=150, height=55, font=("Arial", 14, "bold"))
    btn_ajouter.grid(row=0, column=0, padx=15)

    btn_modifier = ctk.CTkButton(frame_btn, text="Modifier", command=modifier_reservation,
        fg_color="#F77F00", text_color="black", corner_radius=20, width=150, height=55, font=("Arial", 14, "bold"))
    btn_modifier.grid(row=0, column=1, padx=15)

    btn_supprimer = ctk.CTkButton(frame_btn, text="Supprimer", command=supprimer_reservation,
        fg_color="#F77F00", text_color="black", corner_radius=20, width=150, height=55, font=("Arial", 14, "bold"))
    btn_supprimer.grid(row=0, column=2, padx=15)

    load_data()
    fenetre.protocol("WM_DELETE_WINDOW", lambda: (conn.close(), fenetre.destroy()))
    fenetre.mainloop()

if __name__ == "__main__":
    main()
