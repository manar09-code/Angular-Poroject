# news_modern.py
from tkinter import *
import customtkinter as ctk
import home
from PIL import Image, ImageTk
import os

def main():
    fenetre = Tk()
    fenetre.title("Actualités - Système de Réservation Sportive")
    fenetre.configure(bg="#f2f2f2")
    fenetre.state("zoomed")

    # --- Retour button ---
    ctk.CTkButton(fenetre, text="← Retour", width=100, height=40,
                  fg_color="#F77F00", hover_color="#E57100", font=("Arial", 12, "bold"),
                  command=lambda: back_home(fenetre)).pack(pady=10, anchor="nw", padx=10)

    # --- Titre de la page ---
    ctk.CTkLabel(fenetre, text="Actualités Récentes", font=("Arial", 28, "bold"),
                 text_color="#1C9273").pack(pady=20)

    # --- Frame avec scroll ---
    frame_outer = Frame(fenetre, bg="#f2f2f2")
    frame_outer.pack(fill=BOTH, expand=True, padx=20, pady=10)

    canvas = Canvas(frame_outer, bg="#f2f2f2", highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(frame_outer, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame_news = Frame(canvas, bg="#f2f2f2")
    canvas.create_window((0, 0), window=frame_news, anchor="nw")

    # --- Liste des news avec images et couleurs ---
    news_list = [
        {"title": "Tournoi de Football ce weekend !", "img": "football.png", "color": "#F77F00"},
        {"title": "Nouvelle salle de Padel ouverte !", "img": "padel.png", "color": "#1C9273"},
        {"title": "Promotion spéciale abonnés Premium !", "img": "promo.png", "color": "#1F5061"},
        {"title": "Événement Handball le mois prochain", "img": "handball.png", "color": "#F7C59F"},
        {"title": "Championnat de Basketball régional", "img": "basketball.png", "color": "#FF6F61"},
        {"title": "Cours de Tennis pour débutants", "img": "tennis.png", "color": "#4ECDC4"},
        {"title": "Journée portes ouvertes au complexe", "img": "complex.png", "color": "#45B7D1"},
        {"title": "Réduction sur les abonnements annuels", "img": "reduction.png", "color": "#96CEB4"}
    ]

    def on_enter(e, frame):
        frame.configure(bg="#FFA500")  # couleur au survol
        frame.scale = 1.02
        frame.tkraise()

    def on_leave(e, frame, color):
        frame.configure(bg=color)
        frame.scale = 1.0

    for news in news_list:
        box_frame = Frame(frame_news, bg=news["color"], padx=10, pady=10)
        box_frame.pack(fill=X, pady=15, ipady=5)

        # Image si disponible
        img_path = os.path.join(os.path.dirname(__file__), "Pictures", news["img"])
        try:
            img = Image.open(img_path).resize((60, 60))
            img = ImageTk.PhotoImage(img)
            img_label = Label(box_frame, image=img, bg=news["color"])
            img_label.image = img
            img_label.pack(side=LEFT, padx=10)
        except:
            pass

        news_label = ctk.CTkLabel(box_frame, text=news["title"], font=("Arial", 16, "bold"),
                                  text_color="white", width=600, height=60, corner_radius=15)
        news_label.pack(side=LEFT, padx=10, fill=X, expand=True)

        # Hover effect
        box_frame.bind("<Enter>", lambda e, f=box_frame: on_enter(e, f))
        box_frame.bind("<Leave>", lambda e, f=box_frame, c=news["color"]: on_leave(e, f, c))
        news_label.bind("<Enter>", lambda e, f=box_frame: on_enter(e, f))
        news_label.bind("<Leave>", lambda e, f=box_frame, c=news["color"]: on_leave(e, f, c))

    frame_news.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    fenetre.mainloop()


def back_home(win):
    win.destroy()
    home.main()
