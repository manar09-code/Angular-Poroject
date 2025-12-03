from tkinter import *
from tkinter import ttk, messagebox
from datetime import date
from PIL import Image, ImageTk
import customtkinter as ctk
import os
from pymongo import MongoClient

import home
import payment

# ---------------- MongoDB ----------------
try:
    client = MongoClient(
        "mongodb+srv://mahmoudsaadaui55_db_user:admin21@cluster0.otk3rx1.mongodb.net/sports_reservation?retryWrites=true&w=majority",
        serverSelectionTimeoutMS=5000
    )
    db = client["sports_reservation"]
    reservations_collection = db["reservations"]
    client.server_info()  # Vérifie la connexion
except Exception as e:
    messagebox.showerror("Erreur DB", f"Impossible de se connecter à la base de données : {e}")
    exit()


def main(user=None):
    fenetre = Tk()
    fenetre.title("Système de Réservation Sportive")
    fenetre.configure(bg="white")
    fenetre.state("zoomed")
    fenetre.bind("<Escape>", lambda e: fenetre.attributes("-fullscreen", False))

    reservations_list = []

    # ---------------- BOUTON RETOUR ----------------
    def go_back():
        fenetre.destroy()
        home.main(user)

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

    # ---------------- FRAME 1 – Choix du terrain ----------------
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
    selected_frame = [None]  # référence pour surbrillance

    def select_terrain(name, frame_img):
        terrain.set(name)
        if selected_frame[0]:
            selected_frame[0].config(highlightthickness=0)
        frame_img.config(highlightbackground="green", highlightthickness=4)
        selected_frame[0] = frame_img

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

        def make_on_click(n=name, f=frame_img):
            return lambda e: select_terrain(n, f)

        lbl_img.bind("<Button-1>", make_on_click())
        frame_img.bind("<Button-1>", make_on_click())

    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # ---------------- CONTAINER FOR FRAME 2 AND BUTTONS ----------------
    container = Frame(fenetre, bg="white")
    container.pack(pady=10, padx=10, fill="x")

    # ---------------- FRAME 2 – Formulaire (Inputs only) ----------------
    frame2 = LabelFrame(
        container, text="Formulaire de Réservation",
        font=("Arial", 12, "bold"), bg="white"
    )
    frame2.pack(side=LEFT, fill="both", expand=True, padx=(0,10))
    frame2.grid_columnconfigure(1, weight=1)

    Label(frame2, text="Nom complet :", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=10, pady=2, sticky="w")
    nom_entry = ctk.CTkEntry(frame2, width=300, height=35, corner_radius=10, fg_color="#f2f2f2", text_color="black",
                             placeholder_text="Nom complet", font=("Arial", 12))
    nom_entry.grid(row=0, column=1, padx=10, pady=2, sticky="w")

    Label(frame2, text="Date de réservation :", font=("Arial", 11), bg="white").grid(row=1, column=0, padx=10, pady=2, sticky="w")
    date_entry = ctk.CTkEntry(frame2, width=300, height=35, corner_radius=10, fg_color="#f2f2f2", text_color="black",
                              placeholder_text="JJ/MM/AAAA", font=("Arial", 12))
    date_entry.grid(row=1, column=1, padx=10, pady=2, sticky="w")
    date_entry.insert(0, date.today().strftime("%d/%m/%Y"))

    Label(frame2, text="Heure :", font=("Arial", 11), bg="white").grid(row=2, column=0, padx=10, pady=2, sticky="w")
    hours = ["08:00-10:00", "10:00-12:00", "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00", "23:00-01:00"]
    heure_combo = ctk.CTkComboBox(frame2, values=hours, width=300, height=35, corner_radius=10, font=("Arial", 12))
    heure_combo.grid(row=2, column=1, padx=10, pady=2, sticky="w")

    Label(frame2, text="Forfait :", font=("Arial", 11), bg="white").grid(row=3, column=0, padx=10, pady=2, sticky="w")
    forfait_var = StringVar(value="Standard")
    forfait_combo = ctk.CTkComboBox(frame2, values=["Standard", "Premium", "VIP"], width=300, height=35,
                                     corner_radius=10, variable=forfait_var)
    forfait_combo.grid(row=3, column=1, padx=10, pady=2, sticky="w")

    # ---------------- FRAME 2 BUTTONS – Buttons and Options ----------------
    frame2_buttons = LabelFrame(
        container, text="Actions et Options",
        font=("Arial", 12, "bold"), bg="white"
    )
    frame2_buttons.pack(side=RIGHT, fill="y", padx=(10,0))

    # Frame boutons horizontaux
    buttons_frame = Frame(frame2_buttons, bg="white")
    buttons_frame.pack(pady=10)

    btn_ajouter = ctk.CTkButton(buttons_frame, text="Ajouter", fg_color="#1C9273", text_color="white",
                                corner_radius=20, height=40, font=("Arial", 12, "bold"))
    btn_ajouter.pack(side=LEFT, padx=5, pady=5)

    btn_modifier = ctk.CTkButton(buttons_frame, text="Modifier", fg_color="#F7A400", text_color="white",
                                 corner_radius=20, height=40, font=("Arial", 12, "bold"), state="disabled")
    btn_modifier.pack(side=LEFT, padx=5, pady=5)

    btn_update = ctk.CTkButton(buttons_frame, text="Update", fg_color="#F7A400", text_color="white",
                               corner_radius=20, height=40, font=("Arial", 12, "bold"), state="disabled")
    btn_update.pack(side=LEFT, padx=5, pady=5)

    btn_paiement = ctk.CTkButton(buttons_frame, text="Passer au Paiement", fg_color="#1C9273", text_color="white",
                                 corner_radius=20, height=40, font=("Arial", 12, "bold"), state="disabled")
    btn_paiement.pack(side=LEFT, padx=5, pady=5)

    # Options supplémentaires
    options_container = Frame(frame2_buttons, bg="white")
    options_container.pack(pady=10)

    Label(options_container, text="Options supplémentaires :", font=("Arial", 11), bg="white").pack(anchor="w")
    options_frame = Frame(options_container, bg="white")
    options_frame.pack(anchor="w")

    equipment_var = IntVar()
    coaching_var = IntVar()
    abonnement_var = IntVar(value=0)

    ctk.CTkCheckBox(options_frame, text="Location d'équipement (+5 TND)", variable=equipment_var, text_color="black").pack(anchor="w")
    ctk.CTkCheckBox(options_frame, text="Coaching personnel (+10 TND)", variable=coaching_var, text_color="black").pack(anchor="w")

    # ---------------- FONCTIONS CRUD ----------------
    def find_alternatives(date_r, heure, terr):
        alternatives = []
        current_index = hours.index(heure) if heure in hours else 0
        for i in range(current_index + 1, len(hours)):
            next_heure = hours[i]
            conflict = reservations_collection.find_one({"date": date_r, "heure": next_heure, "terrain": terr})
            if not conflict:
                alternatives.append(f"{terr} à {next_heure}")
                break
        terrains_list = [t[0] for t in terrains]
        for alt_terr in terrains_list:
            if alt_terr != terr:
                conflict = reservations_collection.find_one({"date": date_r, "heure": heure, "terrain": alt_terr})
                if not conflict:
                    alternatives.append(f"{alt_terr} à {heure}")
                    break
        return alternatives

    # ---------------- FRAME 3 – Liste des réservations ----------------
    frame3 = LabelFrame(fenetre, text="Vos Réservations", font=("Arial", 12, "bold"), bg="white")
    frame3.pack(pady=10, padx=10, fill="both", expand=True)

    columns = ("Nom", "Date", "Heure", "Terrain", "Forfait", "Abonnement", "Équipement", "Coaching")
    tree = ttk.Treeview(frame3, columns=columns, show="headings", height=10)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def update_reservations_table():
        for item in tree.get_children():
            tree.delete(item)
        query = {"user": user} if user else {}
        for row in reservations_collection.find(query):
            tree.insert("", "end", values=(
                row["nom"], row["date"], row["heure"], row["terrain"],
                row.get("forfait", "Standard"), "Oui" if row.get("abonnement", 0) else "Non",
                "Oui" if row.get("equipment", 0) else "Non",
                "Oui" if row.get("coaching", 0) else "Non"
            ))

    # ---------------- Ajouter réservation ----------------
    def ajouter_reservation():
        nom = nom_entry.get().strip()
        date_r = date_entry.get().strip()
        heure = heure_combo.get().strip()
        terr = terrain.get().strip()
        forfait = forfait_var.get().strip()
        abonnement = abonnement_var.get()
        equipment = equipment_var.get()
        coaching = coaching_var.get()

        if not nom or not date_r or not heure or not terr:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        conflict = reservations_collection.find_one({"date": date_r, "heure": heure, "terrain": terr})
        if conflict:
            alternatives = find_alternatives(date_r, heure, terr)
            msg = f"Le terrain {terr} est déjà réservé à {heure}.\n\nSuggestions AI :\n"
            if alternatives:
                msg += "\n".join(f"- {alt}" for alt in alternatives)
                msg += "\n\nVoulez-vous réessayer avec une alternative ?"
                retry = messagebox.askyesno("Conflit détecté", msg)
                if retry:
                    return
            else:
                msg += "Aucune alternative disponible pour cette date."
                messagebox.showerror("Indisponible", msg)
            return

        new_res = {
            "nom": nom, "date": date_r, "heure": heure, "terrain": terr,
            "forfait": forfait, "abonnement": abonnement,
            "equipment": equipment, "coaching": coaching, "user": user
        }
        reservations_collection.insert_one(new_res)
        messagebox.showinfo("Succès", "Réservation ajoutée !")
        update_reservations_table()

        nom_entry.delete(0, END)
        heure_combo.set("")
        terrain.set("")
        equipment_var.set(0)
        coaching_var.set(0)

        proceed = messagebox.askyesno("Paiement", "Voulez-vous procéder au paiement maintenant ?")
        if proceed:
            fenetre.destroy()
            payment.main(new_res)

    btn_ajouter.configure(command=ajouter_reservation)

    # Charger initialement
    update_reservations_table()
    fenetre.mainloop()


if __name__ == "__main__":
    main("TestUser")