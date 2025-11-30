# home.py
from tkinter import *
from PIL import Image, ImageTk
import customtkinter as ctk
import os
import reservation, payment, news, stats

def main():
    fenetre = Tk()
    fenetre.title("Accueil - Système de Réservation Sportive")
    fenetre.configure(bg="white")
    fenetre.state("zoomed")

    # --- Background Image (with os path) ---
    current_dir = os.path.dirname(os.path.abspath(__file__))          # folder of home.py
    bg_path = os.path.join(current_dir, "background1.jpg")             # image in same folder

    bg_image = Image.open(bg_path)
    bg_image = bg_image.resize(
        (fenetre.winfo_screenwidth(), fenetre.winfo_screenheight())
    )
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(fenetre, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo  # Important: prevents garbage collection

    # --- Top Canvas for Animated Welcome ---
    canvas = Canvas(
        fenetre,
        width=fenetre.winfo_screenwidth(),
        height=200,
        bg="#133A5C",
        highlightthickness=0
    )
    canvas.pack(fill="x")

    welcome_text = canvas.create_text(
        0, 100,
        text="Bienvenue dans le Système de Réservation Sportive!",
        font=("Arial", 24, "bold"),
        fill="white",
        anchor="w"
    )

    def animate():
        canvas.move(welcome_text, 2, 0)
        pos = canvas.coords(welcome_text)
        if pos[0] > fenetre.winfo_screenwidth():
            canvas.coords(welcome_text, 0, 100)
        fenetre.after(20, animate)

    animate()

    # --- Frame for Menu Buttons ---
    frame_menu = Frame(fenetre, bg="white")
    frame_menu.pack(pady=30)

    button_width = 150
    button_height = 40

    ctk.CTkButton(
        frame_menu,
        text="Réservation",
        width=button_width,
        height=button_height,
        corner_radius=20,
        fg_color="#133A5C",
        hover_color="#F77F00",
        font=("Arial", 16, "bold"),
        command=lambda: open_page(reservation)
    ).grid(row=0, column=0, padx=20, pady=20)

    ctk.CTkButton(
        frame_menu,
        text="Paiement",
        width=button_width,
        height=button_height,
        corner_radius=20,
        fg_color="#133A5C",
        hover_color="#F77F00",
        font=("Arial", 16, "bold"),
        command=lambda: open_page(payment)
    ).grid(row=0, column=1, padx=20, pady=20)

    ctk.CTkButton(
        frame_menu,
        text="Actualités",
        width=button_width,
        height=button_height,
        corner_radius=20,
        fg_color="#133A5C",
        hover_color="#F77F00",
        font=("Arial", 16, "bold"),
        command=lambda: open_page(news)
    ).grid(row=1, column=0, padx=20, pady=20)

    ctk.CTkButton(
        frame_menu,
        text="Statistiques",
        width=button_width,
        height=button_height,
        corner_radius=20,
        fg_color="#133A5C",
        hover_color="#F77F00",
        font=("Arial", 16, "bold"),
        command=lambda: open_page(stats)
    ).grid(row=1, column=1, padx=20, pady=20)

    # --- Function to Open Pages ---
    def open_page(module):
        fenetre.destroy()
        module.main()

    fenetre.mainloop()

if __name__ == "__main__":
    main()
