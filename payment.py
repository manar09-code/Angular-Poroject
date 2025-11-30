# payment.py
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import customtkinter as ctk
import home
import os

# Taux de conversion Euro -> TND
EURO_TO_TND = 3.3  # 1€ = 3.3 TND

def main(reservation_info=None):
    if reservation_info is None:
        messagebox.showerror("Erreur", "Aucune réservation sélectionnée !")
        return

    fenetre = Tk()
    fenetre.title("Paiement - Système de Réservation Sportive")
    fenetre.state("zoomed")
    fenetre.configure(bg="white")
    fenetre.bind("<Escape>", lambda e: fenetre.attributes("-fullscreen", False))

    # --- Background image ---
    try:
        img_path = os.path.join(os.path.dirname(__file__), "payement.jpg")
        bg_image = Image.open(img_path)
        bg_image = bg_image.resize((fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(fenetre, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        fenetre.configure(bg="white")

    # --- Retour Button ---
    ctk.CTkButton(
        fenetre,
        text="⟵ Retour",
        width=120,
        height=40,
        fg_color="#1C9273",
        hover_color="#14625C",
        font=("Arial", 14, "bold"),
        command=lambda: back_home(fenetre)
    ).pack(anchor="nw", padx=20, pady=20)

    # --- Résumé de la réservation ---
    frame_summary = Frame(fenetre, bg="white")
    frame_summary.pack(pady=20)

    nom = reservation_info.get("nom", "Non spécifié")
    terrain = reservation_info.get("terrain", "Non spécifié")
    date_r = reservation_info.get("date", "Non spécifié")
    heure = reservation_info.get("heure", "Non spécifié")
    summary_text = (
        f"Résumé de votre réservation :\n\n"
        f"Nom : {nom}\n"
        f"Terrain : {terrain}\n"
        f"Date : {date_r}\n"
        f"Créneau : {heure}"
    )

    # Détecter weekend
    try:
        day_of_week = datetime.strptime(date_r, "%d/%m/%Y").weekday()
        is_weekend = day_of_week >= 5
    except:
        is_weekend = False

    ctk.CTkLabel(frame_summary, text=summary_text, font=("Arial", 16), text_color="#333").pack()

    # --- Choix du plan ---
    frame_plans = Frame(fenetre, bg="white")
    frame_plans.pack(pady=20)

    plans = [
        {"nom": "Forfait Standard", "prix": 10, "details": "1h de réservation, 2 joueurs inclus", "color": "#F77F00"},
        {"nom": "Forfait Premium", "prix": 20, "details": "2h de réservation, 4 joueurs inclus", "color": "#1C9273"},
        {"nom": "Forfait VIP", "prix": 30, "details": "3h de réservation, 6 joueurs inclus", "color": "#1F5061"}
    ]

    abonnement_var = IntVar(value=0)
    ctk.CTkCheckBox(
        fenetre,
        text="Abonnement mensuel (-10%)",
        variable=abonnement_var,
        onvalue=1,
        offvalue=0,
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    for i, plan in enumerate(plans):
        ctk.CTkButton(
            frame_plans,
            text=f"{plan['nom']} - {plan['prix']*EURO_TO_TND:.2f} TND\n{plan['details']}",
            width=350,
            height=100,
            fg_color=plan["color"],
            hover_color="#E57100",
            font=("Arial", 14, "bold"),
            corner_radius=20,
            command=lambda p=plan: pay(fenetre, p, reservation_info, abonnement_var.get(), is_weekend)
        ).grid(row=i, column=0, pady=15)

    fenetre.mainloop()


def pay(parent, plan, reservation_info, abonnement, is_weekend):
    """Fenêtre de paiement qui s'ouvre correctement"""
    if reservation_info is None:
        messagebox.showerror("Erreur", "Aucune réservation sélectionnée !")
        return

    pay_win = Toplevel(parent)
    pay_win.title("Paiement")
    pay_win.geometry("500x450")
    pay_win.configure(bg="white")
    pay_win.grab_set()  # modal
    pay_win.transient(parent)  # focus on top

    nom = reservation_info.get("nom", "Non spécifié")
    terrain = reservation_info.get("terrain", "Non spécifié")
    date_r = reservation_info.get("date", "Non spécifié")
    heure = reservation_info.get("heure", "Non spécifié")

    prix = plan["prix"] * EURO_TO_TND
    reductions = []

    if is_weekend:
        prix *= 0.9
        reductions.append("Réduction weekend (-10%)")
    if abonnement:
        prix *= 0.9
        reductions.append("Réduction abonnement (-10%)")

    summary_text = (
        f"Plan choisi : {plan['nom']} - {plan['prix']*EURO_TO_TND:.2f} TND\n\n"
        f"Nom : {nom}\nTerrain : {terrain}\nDate : {date_r}\nCréneau : {heure}\n\n"
        f"Prix final : {prix:.2f} TND"
    )
    if reductions:
        summary_text += "\n" + "\n".join(reductions)

    ctk.CTkLabel(pay_win, text=summary_text, font=("Arial", 14), text_color="#333").pack(pady=20, padx=20)

    frame_buttons = Frame(pay_win, bg="white")
    frame_buttons.pack(pady=10)

    ctk.CTkButton(
        frame_buttons,
        text="Payer par Carte e-Dinar",
        fg_color="#F77F00",
        hover_color="#E57100",
        font=("Arial", 12, "bold"),
        width=200,
        height=40,
        command=lambda: messagebox.showinfo("Paiement", f"Paiement de {prix:.2f} TND réussi par e-Dinar !")
    ).pack(pady=10)

    ctk.CTkButton(
        frame_buttons,
        text="Payer par Carte Bancaire",
        fg_color="#1C9273",
        hover_color="#14625C",
        font=("Arial", 12, "bold"),
        width=200,
        height=40,
        command=lambda: messagebox.showinfo("Paiement", f"Paiement de {prix:.2f} TND réussi par Carte Bancaire !")
    ).pack(pady=10)

    ctk.CTkButton(
        pay_win,
        text="Fermer",
        fg_color="#D90429",
        hover_color="#B5001F",
        font=("Arial", 12, "bold"),
        width=200,
        height=40,
        command=pay_win.destroy
    ).pack(pady=20)


def back_home(win):
    win.destroy()
    home.main()


if __name__ == "__main__":
    main({
        "nom": "Test User",
        "terrain": "Terrain de Football",
        "date": "25/11/2025",
        "heure": "10:00-12:00"
    })
