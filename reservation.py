from tkinter import *
from tkinter import ttk, messagebox
from datetime import date
from PIL import Image, ImageTk
import customtkinter as ctk
import os

def main():
    fenetre = Tk()
    fenetre.title("Système de Réservation Sportive")
    fenetre.configure(bg="white")
    fenetre.state("zoomed")
    fenetre.bind("<Escape>", lambda e: fenetre.attributes("-fullscreen", False))

    reservations_list = []

    # ------------------- FRAME 1: Choisir terrain avec scroll -------------------
    frame1_outer = LabelFrame(fenetre, text="Choisissez un terrain/salle", font=("Arial", 12, "bold"), bg="white")
    frame1_outer.pack(pady=10, padx=10, fill="x")

    canvas = Canvas(frame1_outer, height=250, bg="white", highlightthickness=0)
    canvas.pack(side=LEFT, fill=X, expand=True)

    scrollbar = Scrollbar(frame1_outer, orient=HORIZONTAL, command=canvas.xview)
    scrollbar.pack(side=BOTTOM, fill=X)

    canvas.configure(xscrollcommand=scrollbar.set)

    frame1 = Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=frame1, anchor="nw")

    terrain = StringVar(value="")

    terrains = [
        ("Terrain de Football", "foot.jpg"),
        ("Terrain de Basketball", "basketball.jpg"),
        ("Terrain de Tennis", "tennis.jpg"),
        ("Salle de Handball", "handball.jpg"),
        ("Terrain de Padel", "padel.jpg")
    ]

    left_pad = Frame(frame1, width=50, bg="white")
    left_pad.grid(row=0, column=0)

    def select_terrain(name):
        terrain.set(name)

    for i, (name, filename) in enumerate(terrains):
        try:
            img_path = os.path.join(os.path.dirname(__file__), "Pictures", filename)
            img = Image.open(img_path)
            img = img.resize((220, 160))  # smaller images so radio buttons appear
            img = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Erreur image {filename}: {e}")
            img = None

        # Main frame for each terrain
        frame_img = Frame(frame1, bg="#F77F00", padx=5, pady=5)
        frame_img.grid(row=0, column=i+1, padx=30, pady=20)

        # Make frame clickable to select terrain
        def on_click(event, name=name):
            select_terrain(name)

        frame_img.bind("<Button-1>", on_click)

        if img:
            lbl_img = Label(frame_img, image=img, bg="#F77F00")
            lbl_img.image = img
            lbl_img.pack()
            lbl_img.bind("<Button-1>", on_click)

        Label(frame_img, text=name, font=("Arial", 12, "bold"), bg="#F77F00").pack(pady=5)

        # Radio button visible
        rb = Radiobutton(
            frame_img,
            text="",  # empty, just circle
            variable=terrain,
            value=name,
            bg="#F77F00",
            fg="white",
            activebackground="#F77F00",
            indicatoron=1,
            highlightthickness=0
        )
        rb.pack(pady=5)

    right_pad = Frame(frame1, width=50, bg="white")
    right_pad.grid(row=0, column=len(terrains)+2)

    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # ------------------- FRAME 2: Formulaire -------------------
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

    # ------------------- FRAME 3: Boutons -------------------
    frame_btn = Frame(fenetre, bg="white")
    frame_btn.pack(pady=20)

    # ------------------- FRAME 4: Liste des réservations -------------------
    frame3 = LabelFrame(fenetre, text="Liste des Réservations", font=("Arial", 12, "bold"), bg="white")
    frame3.pack(pady=10, padx=10, fill="both", expand=True)

    tree = ttk.Treeview(frame3, columns=("Nom", "Date", "Heure", "Terrain"), show="headings", height=6)
    tree.heading("Nom", text="Nom complet")
    tree.heading("Date", text="Date de réservation")
    tree.heading("Heure", text="Heure")
    tree.heading("Terrain", text="Terrain")
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    # ------------------- FONCTIONS -------------------
    def load_data():
        tree.delete(*tree.get_children())
        for res in reservations_list:
            tree.insert("", "end", values=(res["nom"], res["date"], res["heure"], res["terrain"]))

    def ajouter_reservation():
        nom = nom_entry.get()
        date_r = date_entry.get()
        heure = heure_combo.get()
        terr = terrain.get()

        if not nom or not date_r or not heure or not terr:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        for res in reservations_list:
            if res["date"] == date_r and res["heure"] == heure and res["terrain"] == terr:
                messagebox.showerror("Indisponible", f"Le terrain {terr} est déjà réservé.")
                return

        reservations_list.append({"nom": nom, "date": date_r, "heure": heure, "terrain": terr})
        load_data()
        nom_entry.delete(0, END)
        heure_combo.set("")
        terrain.set("")
        messagebox.showinfo("Succès", "Réservation ajoutée !")

    def modifier_reservation():
        selected = tree.selection()
        if selected:
            nom = nom_entry.get()
            date_r = date_entry.get()
            heure = heure_combo.get()
            terr = terrain.get()
            old_values = tree.item(selected, "values")

            for res in reservations_list:
                if res["date"] == date_r and res["heure"] == heure and res["terrain"] == terr and \
                   (res["nom"], res["date"], res["heure"], res["terrain"]) != old_values:
                    messagebox.showerror("Indisponible", f"Le terrain {terr} est déjà réservé.")
                    return

            for res in reservations_list:
                if (res["nom"], res["date"], res["heure"], res["terrain"]) == old_values:
                    res["nom"] = nom
                    res["date"] = date_r
                    res["heure"] = heure
                    res["terrain"] = terr
                    break

            tree.item(selected, values=(nom, date_r, heure, terr))

    def supprimer_reservation():
        selected = tree.selection()
        if selected:
            confirm = messagebox.askyesno("Confirmation", "Voulez-vous supprimer cette réservation ?")
            if confirm:
                values = tree.item(selected, "values")
                for res in reservations_list:
                    if (res["nom"], res["date"], res["heure"], res["terrain"]) == values:
                        reservations_list.remove(res)
                        break
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

    # ------------------- BOUTONS -------------------
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
    fenetre.mainloop()

if __name__ == "__main__":
    main()
