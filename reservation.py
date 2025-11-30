# reservation.py
from tkinter import *
from tkinter import ttk, messagebox
from datetime import date
from PIL import Image, ImageTk, ImageOps
import customtkinter as ctk
import os
import csv
import payment
import home

def main():
    fenetre = Tk()
    fenetre.title("Système de Réservation Sportive")
    fenetre.configure(bg="white")
    fenetre.state("zoomed")
    fenetre.bind("<Escape>", lambda e: fenetre.attributes("-fullscreen", False))

    reservations_list = []

    # ------------------------------
    # BOUTON RETOUR
    # ------------------------------
    def go_back():
        fenetre.destroy()
        home.main()

    btn_retour = ctk.CTkButton(
        fenetre,
        text="⟵ Retour",
        fg_color="#1C9273",
        text_color="white",
        corner_radius=15,
        width=120,
        height=40,
        font=("Arial", 14, "bold"),
        command=go_back
    )
    btn_retour.pack(anchor="nw", padx=20, pady=20)

    # ------------------------------
    # FRAME 1 – Choix du terrain
    # ------------------------------
    frame1_outer = LabelFrame(
        fenetre, text="Choisissez un terrain/salle",
        font=("Arial", 12, "bold"), bg="white"
    )
    frame1_outer.pack(pady=10, padx=10, fill="x")

    canvas = Canvas(frame1_outer, height=260, bg="white", highlightthickness=0)
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

    photo_refs = []  # garder les images en mémoire

    # fonction de sélection avec surbrillance
    selected_frame = [None]  # variable mutable pour référence

    def select_terrain(name, frame_img):
        terrain.set(name)
        # retirer contour des anciens
        if selected_frame[0]:
            selected_frame[0].config(highlightthickness=0)
        # mettre contour vert
        frame_img.config(highlightbackground="green", highlightthickness=4)
        selected_frame[0] = frame_img

    # création des frames terrains
    for i, (name, filename) in enumerate(terrains):
        try:
            img_path = os.path.join(os.path.dirname(__file__), "Pictures", filename)
            img = Image.open(img_path).convert("RGBA").resize((220, 160), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        except:
            photo = None
        photo_refs.append(photo)

        frame_img = Frame(frame1, bg="#F77F00", padx=8, pady=8)
        frame_img.grid(row=0, column=i, padx=20, pady=10)

        if photo:
            lbl_img = Label(frame_img, image=photo, bg="#F77F00", cursor="hand2")
            lbl_img.image = photo
            lbl_img.pack()
        else:
            lbl_img = Label(frame_img, text="Image\nnon trouvée", bg="#F77F00", width=28, height=10)
            lbl_img.pack()

        rb = Radiobutton(
            frame_img, text="", variable=terrain, value=name,
            bg="#F77F00", fg="white", activebackground="#F77F00",
            selectcolor="#ffffff", indicatoron=1
        )
        rb.pack(pady=(8, 2))

        Label(frame_img, text=name, font=("Arial", 12, "bold"),
              bg="#F77F00", wraplength=220, justify="center").pack(pady=(2, 6))

        # clic sur image ou frame sélectionne le terrain
        def make_on_click(n=name, f=frame_img):
            return lambda e: select_terrain(n, f)

        lbl_img.bind("<Button-1>", make_on_click())
        frame_img.bind("<Button-1>", make_on_click())

    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # ------------------------------
    # FRAME 2 – Formulaire
    # ------------------------------
    frame2 = LabelFrame(
        fenetre, text="Formulaire de Réservation",
        font=("Arial", 12, "bold"), bg="white"
    )
    frame2.pack(pady=10, padx=10, fill="x")

    frame2.grid_columnconfigure(1, weight=1)

    Label(frame2, text="Nom complet :", font=("Arial", 11),
          bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    nom_entry = ctk.CTkEntry(
        frame2, width=300, height=35, corner_radius=10,
        fg_color="#f2f2f2", text_color="black",
        placeholder_text="Nom complet", font=("Arial", 12)
    )
    nom_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    Label(frame2, text="Date de réservation :", font=("Arial", 11),
          bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    date_entry = ctk.CTkEntry(
        frame2, width=300, height=35, corner_radius=10,
        fg_color="#f2f2f2", text_color="black",
        placeholder_text="JJ/MM/AAAA", font=("Arial", 12)
    )
    date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    date_entry.insert(0, date.today().strftime("%d/%m/%Y"))

    Label(frame2, text="Heure :", font=("Arial", 11),
          bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    hours = ["08:00-10:00", "10:00-12:00", "14:00-16:00",
             "16:00-18:00", "18:00-20:00", "20:00-22:00", "23:00-01:00"]
    heure_combo = ctk.CTkComboBox(frame2, values=hours, width=300, height=35,
                                  corner_radius=10, font=("Arial", 12))
    heure_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    Label(frame2, text="Forfait :", font=("Arial", 11), bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    forfait_var = StringVar(value="Standard")
    forfait_combo = ctk.CTkComboBox(frame2, values=["Standard", "Premium", "VIP"],
                                     width=300, height=35, corner_radius=10, variable=forfait_var)
    forfait_combo.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    Label(frame2, text="Abonnement mensuel :", font=("Arial", 11), bg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    abonnement_var = IntVar(value=0)
    ctk.CTkCheckBox(frame2, text="", variable=abonnement_var, onvalue=1, offvalue=0).grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # Frame boutons à droite
    frame_btn = Frame(frame2, bg="white")
    frame_btn.grid(row=0, column=2, rowspan=5, padx=20, sticky="n")

    def make_ctk_button(parent, **kwargs):
        btn = ctk.CTkButton(parent, **kwargs)
        btn.pack(fill="x", pady=8)
        return btn

    btn_ajouter = make_ctk_button(frame_btn, text="Ajouter", command=lambda: ajouter_reservation(),
                                  fg_color="#1C9273", text_color="white", corner_radius=20, height=40,
                                  font=("Arial", 12, "bold"))
    btn_modifier = make_ctk_button(frame_btn, text="Modifier", command=lambda: modifier_reservation(),
                                   fg_color="#F7A400", text_color="white", corner_radius=20, height=40,
                                   font=("Arial", 12, "bold"))
    btn_supprimer = make_ctk_button(frame_btn, text="Supprimer", command=lambda: supprimer_reservation(),
                                    fg_color="#D90429", text_color="white", corner_radius=20, height=40,
                                    font=("Arial", 12, "bold"))
    btn_paiement = make_ctk_button(frame_btn, text="Passer au Paiement", command=lambda: payment.main(get_selected_reservation()),
                                   fg_color="#1C9273", text_color="white", corner_radius=20, height=40,
                                   font=("Arial", 12, "bold"))

    # ------------------------------
    # FRAME 3 – Liste des réservations
    # ------------------------------
    frame3 = LabelFrame(fenetre, text="Liste des Réservations", font=("Arial", 12, "bold"), bg="white")
    frame3.pack(pady=10, padx=10, fill="both", expand=True)

    tree = ttk.Treeview(frame3,
                        columns=("Nom", "Date", "Heure", "Terrain", "Forfait", "Abonnement"),
                        show="headings", height=12)
    tree.column("Nom", width=180, anchor="center")
    tree.column("Date", width=110, anchor="center")
    tree.column("Heure", width=120, anchor="center")
    tree.column("Terrain", width=180, anchor="center")
    tree.column("Forfait", width=120, anchor="center")
    tree.column("Abonnement", width=120, anchor="center")
    for col in tree["columns"]:
        tree.heading(col, text=col, anchor="center")
    tree.pack(padx=6, pady=6, fill="both", expand=True)

    csv_file = os.path.join(os.path.dirname(__file__), "reservations.csv")

    # ------------------------------
    # FONCTIONS CRUD
    # ------------------------------
    def load_data():
        tree.delete(*tree.get_children())
        for res in reservations_list:
            tree.insert("", "end", values=(res["nom"], res["date"], res["heure"],
                                           res["terrain"], res["forfait"], res["abonnement"]))

    def ajouter_reservation():
        nom = nom_entry.get().strip()
        date_r = date_entry.get().strip()
        heure = heure_combo.get().strip()
        terr = terrain.get().strip()
        forfait = forfait_var.get().strip()
        abonnement = abonnement_var.get()

        if not nom or not date_r or not heure or not terr:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        for res in reservations_list:
            if res["date"] == date_r and res["heure"] == heure and res["terrain"] == terr:
                messagebox.showerror("Indisponible", f"Le terrain {terr} est déjà réservé.")
                return

        new_res = {
            "nom": nom, "date": date_r, "heure": heure,
            "terrain": terr, "forfait": forfait, "abonnement": abonnement
        }
        reservations_list.append(new_res)

        load_data()
        nom_entry.delete(0, END)
        heure_combo.set("")
        terrain.set("")
        messagebox.showinfo("Succès", "Réservation ajoutée !")

        # Ask to proceed to payment
        proceed = messagebox.askyesno("Paiement", "Voulez-vous procéder au paiement maintenant ?")
        if proceed:
            fenetre.destroy()
            payment.main(new_res)

        file_exists = os.path.isfile(csv_file)
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nom", "date", "heure", "terrain", "forfait", "abonnement"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({"nom": nom, "date": date_r, "heure": heure,
                             "terrain": terr, "forfait": forfait, "abonnement": abonnement})

    def get_selected_reservation():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Sélectionner", "Veuillez sélectionner une réservation.")
            return None
        values = tree.item(selected[0], "values")
        return {"nom": values[0], "date": values[1], "heure": values[2],
                "terrain": values[3], "forfait": values[4], "abonnement": int(values[5])}

    def modifier_reservation():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Sélectionner", "Veuillez sélectionner une réservation à modifier.")
            return

        index = tree.index(selected[0])
        res = reservations_list[index]

        nom_entry.delete(0, END)
        nom_entry.insert(0, res["nom"])
        date_entry.delete(0, END)
        date_entry.insert(0, res["date"])
        heure_combo.set(res["heure"])
        terrain.set(res["terrain"])
        forfait_var.set(res["forfait"])
        abonnement_var.set(res["abonnement"])

        del reservations_list[index]
        load_data()

    def supprimer_reservation():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Sélectionner", "Veuillez sélectionner une réservation à supprimer.")
            return

        index = tree.index(selected[0])
        res = reservations_list[index]
        confirm = messagebox.askyesno("Confirmer", f"Supprimer la réservation de {res['nom']} ?")
        if confirm:
            del reservations_list[index]
            load_data()
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["nom", "date", "heure", "terrain", "forfait", "abonnement"])
                writer.writeheader()
                for r in reservations_list:
                    writer.writerow(r)

    # ------------------------------
    # CHARGEMENT CSV
    # ------------------------------
    if os.path.isfile(csv_file):
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                reservations_list.append({
                    "nom": row["nom"],
                    "date": row["date"],
                    "heure": row["heure"],
                    "terrain": row["terrain"],
                    "forfait": row["forfait"],
                    "abonnement": int(row["abonnement"])
                })
        load_data()

    fenetre.mainloop()


if __name__ == "__main__":
    main()
