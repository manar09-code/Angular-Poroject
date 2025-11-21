# news.py
from tkinter import *
import customtkinter as ctk
import home

def main():
    fenetre = Tk()
    fenetre.title("Actualités - Système de Réservation Sportive")
    fenetre.configure(bg="white")
    fenetre.state("zoomed")

    # --- Retour button ---
    ctk.CTkButton(fenetre, text="← Retour", width=100, height=40,
                  fg_color="#F77F00", hover_color="#E57100", font=("Arial", 12, "bold"),
                  command=lambda: back_home(fenetre)).pack(pady=10, anchor="nw", padx=10)

    # --- News Content ---
    frame = Frame(fenetre, bg="white")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    news_list = [
        "Tournoi de Football ce weekend !",
        "Nouvelle salle de Padel ouverte !",
        "Promotion spéciale abonnés Premium !"
    ]

    for i, news in enumerate(news_list):
        box = ctk.CTkLabel(frame, text=news, width=600, height=60, corner_radius=15,
                            fg_color="#F77F00", text_color="white",
                            font=("Arial", 14, "bold"))
        box.pack(pady=10)

    fenetre.mainloop()

def back_home(win):
    win.destroy()
    home.main()
