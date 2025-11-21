from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import date
import customtkinter as ctk

def main():
    fenetre = Tk()
    fenetre.title("Système de Réservation Sportive")
    fenetre.geometry("1100x700")
    fenetre.configure(bg="white")

    # ---------------- FRAME CHOIX TERRAIN ----------------
    frame1 = LabelFrame(fenetre, text="Choisissez un terrain/salle",
                        font=("Arial", 12, "bold"), bg="white")
    frame1.pack(pady=10, padx=10, fill="x")

    terrain = StringVar(value="")

    def create_terrain(parent, img_path, text, col):
        img = Image.open(img_path)
        img = img.resize((280, 220))
        img = ImageTk.PhotoImage(img)

        frame = Frame(parent, bg="#F77F00")
        frame.grid(row=0, column=col, padx=8, pady=10)

        Label(frame, image=img, bg="#F77F00").pack()
        Label(frame, text=text, font=("Arial", 10, "bold"),
              bg="#F77F00").pack(pady=2)

        rb = Radiobutton(frame, variable=terrain, value=text, bg="#F77F00")
        rb.pack(pady=3)

        frame.image = img

    terrains = [
        ("foot.jpg", "Terrain de Football"),
        ("basketball.jpg", "Terrain de Basketball"),
        ("tennis.jpg", "Terrain de Tennis"),
        ("handball.jpg", "Salle de Handball"),
        ("padel.jpg", "Terrain de Padel"),
    ]

    for i, (img, txt) in enumerate(terrains):
        create_terrain(frame1, img, txt, i)

    # ---------------- FRAME FORMULAIRE ----------------
    frame2 = LabelFrame(fenetre, text="Formulaire de Réservation",
                        font=("Arial", 12, "bold"), bg="white")
    frame2.pack(pady=10, padx=10, fill="x")

    Label(frame2, text="Nom complet :", font=("Arial", 11), bg="white")\
        .grid(row=0, column=0, padx=10, pady=5, sticky="w")

    nom_entry = ctk.CTkEntry(frame2, width=300, height=35, corner_radius=10,
                             fg_color="#f2f2f2", text_color="black",
                             placeholder_text="Nom complet")
    nom_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(frame2, text="Date de réservation :", font=("Arial", 11), bg="white")\
        .grid(row=1, column=0, padx=10, pady=5, sticky="w")

    date_entry = ctk.CTkEntry(frame2, width=300, height=35, corner_radius=10,
                              fg_color="#f2f2f2", text_color="black",
                              placeholder_text="JJ/MM/AAAA")
    date_entry.grid(row=1, column=1, padx=10, pady=5)
    date_entry.insert(0, date.today().strftime("%d/%m/%Y"))

    Label(frame2, text="Heure :", font=("Arial", 11), bg="white")\
        .grid(row=2, column=0, padx=10, pady=5, sticky="w")

    hours = ["08:00-10:00", "10:00-12:00", "14:00-16:00",
             "16:00-18:00", "18:00-20:00", "20:00-22:00", "23:00-01:00"]

    heure_combo = ctk.CTkComboBox(frame2, values=hours, width=300, height=35)
    heure_combo.grid(row=2, column=1, padx=10, pady=5)

    # ---------------- BUTTONS ----------------
    frame_btn = Frame(fenetre, bg="white")
    frame_btn.pack(pady=20)

    # CRUD fonctions (local only)
    def ajouter_reservation():
        nom = nom_entry.get()
        date_r = date_entry.get()
        heure = heure_combo.get()
        terr = terrain.get()

        if nom and heure and terr:
            tree.insert("", "end", values=(nom, date_r, heure, terr))
            nom_entry.delete(0, END)
            heure_combo.set("")
            terrain.set("")

    def modifier_reservation():
        selected = tree.selection()
        if selected:
            tree.item(selected, values=(
                nom_entry.get(),
                date_entry.get(),
                heure_combo.get(),
                terrain.get()
            ))

    def supprimer_reservation():
        selected = tree.selection()
        if selected:
            tree.delete(selected)

    # Buttons
    ctk.CTkButton(frame_btn, text="Ajouter", command=ajouter_reservation,
                  fg_color="#F77F00", text_color="black",
                  corner_radius=20, width=150, height=55)\
                  .grid(row=0, column=0, padx=15)

    ctk.CTkButton(frame_btn, text="Modifier", command=modifier_reservation,
                  fg_color="#F77F00", text_color="black",
                  corner_radius=20, width=150, height=55)\
                  .grid(row=0, column=1, padx=15)

    ctk.CTkButton(frame_btn, text="Supprimer", command=supprimer_reservation,
                  fg_color="#F77F00", text_color="black",
                  corner_radius=20, width=150, height=55)\
                  .grid(row=0, column=2, padx=15)

    # ---------------- TABLE ----------------
    frame3 = LabelFrame(fenetre, text="Liste des Réservations",
                        font=("Arial", 12, "bold"), bg="white")
    frame3.pack(pady=10, padx=10, fill="both", expand=True)

    columns = ("Nom", "Date", "Heure", "Terrain")
    tree = ttk.Treeview(frame3, columns=columns, show="headings", height=6)

    for col in columns:
        tree.heading(col, text=col)

    tree.pack(padx=10, pady=10, fill="both", expand=True)

    # Click on row = load data
    def selected_item(event):
        selected = tree.selection()
        if selected:
            val = tree.item(selected, "values")
            nom_entry.delete(0, END)
            nom_entry.insert(0, val[0])
            date_entry.delete(0, END)
            date_entry.insert(0, val[1])
            heure_combo.set(val[2])
            terrain.set(val[3])

    tree.bind("<<TreeviewSelect>>", selected_item)

    fenetre.mainloop()

if __name__ == "__main__":
    main()
