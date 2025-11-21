# payment.py
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import home

def main():
    fenetre = Tk()
    fenetre.title("Paiement - Système de Réservation Sportive")
    fenetre.configure(bg="white")
    fenetre.state("zoomed")

    # --- Retour button ---
    ctk.CTkButton(fenetre, text="← Retour", width=100, height=40,
                  fg_color="#F77F00", hover_color="#E57100", font=("Arial", 12, "bold"),
                  command=lambda: back_home(fenetre)).pack(pady=10, anchor="nw", padx=10)

    # --- Example Payment Boxes ---
    frame = Frame(fenetre, bg="white")
    frame.pack(pady=50)

    for i, plan in enumerate(["Forfait Standard - 10€", "Forfait Premium - 20€", "Forfait VIP - 30€"]):
        box = ctk.CTkButton(frame, text=plan, width=300, height=80,
                             fg_color="#F77F00", hover_color="#E57100",
                             font=("Arial", 16, "bold"), corner_radius=20,
                             command=lambda p=plan: pay(p))
        box.grid(row=i, column=0, pady=15)

    fenetre.mainloop()

def pay(plan):
    messagebox.showinfo("Paiement", f"Vous avez choisi : {plan} (UI seulement)")

def back_home(win):
    win.destroy()
    home.main()
