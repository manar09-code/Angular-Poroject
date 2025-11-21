# stats.py
from tkinter import *
import customtkinter as ctk
import home

def main():
    fenetre = Tk()
    fenetre.title("Statistiques - Système de Réservation Sportive")
    fenetre.configure(bg="white")
    fenetre.state("zoomed")

    # --- Retour button ---
    ctk.CTkButton(fenetre, text="← Retour", width=100, height=40,
                  fg_color="#F77F00", hover_color="#E57100", font=("Arial", 12, "bold"),
                  command=lambda: back_home(fenetre)).pack(pady=10, anchor="nw", padx=10)

    # --- Example Stats Boxes ---
    frame = Frame(fenetre, bg="white")
    frame.pack(pady=50)

    stats_list = [
        "Réservations ce mois : 120",
        "Terrains disponibles : 5",
        "Abonnés Premium : 32"
    ]

    for stat in stats_list:
        box = ctk.CTkLabel(frame, text=stat, width=400, height=60, corner_radius=15,
                            fg_color="#F77F00", text_color="white",
                            font=("Arial", 14, "bold"))
        box.pack(pady=15)

    fenetre.mainloop()

def back_home(win):
    win.destroy()
    home.main()
