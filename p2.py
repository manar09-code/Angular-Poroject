from tkinter import *  # biblio principale
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import date
import customtkinter as ctk  # biblio pour les coins arrondis des boutons

def main():
    #fenetre principale
    fenetre = Tk()
    fenetre.title("Systeme de Reservation Sportive")
    fenetre.geometry("1100x700")
    fenetre.configure(bg="white")

    #frame 1 : Choix du terrain ou salle
    frame1 = LabelFrame(fenetre, text="Choississez un terrain/salle", font=("Arial", 12, "bold"), bg="white")
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

    #frame 2 : Formulaire 
    frame2 = LabelFrame(fenetre, text="Formulaire de Reservation", font=("Arial", 12, "bold"), bg="white")
    frame2.pack(pady=10, padx=10, fill="x")

    Label(frame2, text="Nom complet :", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    nom_entry = ctk.CTkEntry(
        frame2,
        width=300,
        height=35,
        corner_radius=10,
        fg_color="#f2f2f2",
        text_color="black",
        placeholder_text="Nom complet",
        font=("Arial", 12)
    )
    nom_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(frame2, text="Date de reservation :", font=("Arial", 11), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    date_entry = ctk.CTkEntry(
        frame2,
        width=300,
        height=35,
        corner_radius=10,
        fg_color="#f2f2f2",
        text_color="black",
        placeholder_text="JJ/MM/AAAA",
        font=("Arial", 12)
    )
    date_entry.grid(row=1, column=1, padx=10, pady=5)
    date_entry.insert(0, date.today().strftime("%d/%m/%Y"))

    Label(frame2, text="Heure :", font=("Arial", 11), bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    hours = ["08:00-10:00", "10:00-12:00", "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00", "23:00-01:00"]
    heure_combo = ctk.CTkComboBox(
        frame2,
        values=hours,
        width=300,
        height=35,
        corner_radius=10,
        font=("Arial", 12)
    )
    heure_combo.grid(row=2, column=1, padx=10, pady=5)

    #Frame des Boutons (coins arrondis) 
    frame_btn = Frame(fenetre, bg="white")
    frame_btn.pack(pady=20)

    # Fonctions des boutons 
    def ajouter_reservation():
        nom = nom_entry.get()
        date_r = date_entry.get()
        heure = heure_combo.get()
        terr = terrain.get()

        if nom and heure and terr:
            selected = tree.selection()
            if selected:
                tree.item(selected, values=(nom, date_r, heure, terr))
            else:
                tree.insert("", "end", values=(nom, date_r, heure, terr))
            nom_entry.delete(0, END)
            heure_combo.set("")
            terrain.set("")

    def modifier_reservation():
        selected = tree.selection()
        if selected:
            nom = nom_entry.get()
            date_r = date_entry.get()
            heure = heure_combo.get()
            terr = terrain.get()
            if nom and heure and terr:
                tree.item(selected, values=(nom, date_r, heure, terr))

    def supprimer_reservation():
        selected = tree.selection()
        if selected:
            tree.delete(selected)

    #Rounded Buttons corners using CustomTkinter 
    btn_ajouter = ctk.CTkButton(frame_btn, text="Ajouter", command=ajouter_reservation,
    fg_color="#F77F00", text_color="black", corner_radius=20, width=150, height=55, font=("Arial", 14, "bold"))
    btn_ajouter.grid(row=0, column=0, padx=15)

    btn_modifier = ctk.CTkButton(frame_btn, text="Modifier", command=modifier_reservation,
    fg_color="#F77F00", text_color="black", corner_radius=20, width=150,height=55, font=("Arial", 14, "bold"))
    btn_modifier.grid(row=0, column=1, padx=15)

    btn_supprimer = ctk.CTkButton(frame_btn, text="Supprimer", command=supprimer_reservation,
    fg_color="#F77F00", text_color="black", corner_radius=20, width=150, height=55, font=("Arial", 14, "bold"))
    btn_supprimer.grid(row=0, column=2, padx=15)

    #frame 3 : Liste des réservations 
    frame3 = LabelFrame(fenetre, text="Liste des Reservations", 
    font=("Arial", 12, "bold"), bg="white")
    frame3.pack(pady=10, padx=10, fill="both", expand=True)

    tree = ttk.Treeview(frame3, columns=("Nom", "Date", "Heure", "Terrain"),
    show="headings", height=6)
    tree.heading("Nom", text="Nom complet")
    tree.heading("Date", text="Date de réservation")
    tree.heading("Heure", text="Heure")
    tree.heading("Terrain", text="Terrain")
    tree.pack(padx=10, pady=10, fill="both", expand=True)

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

    fenetre.mainloop()

# Permet d'exécuter p2.py directement
if __name__ == "__main__":
    main()
