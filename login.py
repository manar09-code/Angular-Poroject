from tkinter import *  
import customtkinter as ctk  
from tkinter import messagebox  
from PIL import Image, ImageTk  
import p2  # votre fichier p2.py avec la fonction main()

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

# Clear the frame (used for switching between login/register/forgot)
def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

# ---------------- LOGIN ----------------
def show_login():
    clear_frame()
    
    # Title
    ctk.CTkLabel(frame, text="Connexion", text_color="black", font=("Arial", 16, "bold")).place(relx=0.5, y=25, anchor="center")
    
    # Entries
    global entry_user, entry_pass
    entry_user = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Nom d'utilisateur",
                              placeholder_text_color="gray", corner_radius=15,
                              border_width=1, border_color="lightgray",
                              fg_color="#f2f2f2", text_color="black", font=("Arial", 12))
    entry_user.place(relx=0.5, y=65, anchor="center")

    entry_pass = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Mot de passe",
                              placeholder_text_color="gray", show="*",
                              corner_radius=15, border_width=1, border_color="lightgray",
                              fg_color="#f2f2f2", text_color="black", font=("Arial", 12))
    entry_pass.place(relx=0.5, y=115, anchor="center")

    # Buttons
    ctk.CTkButton(frame, text="Se connecter", width=160, height=38,
                  corner_radius=18, fg_color="#F77F00", hover_color="#E57100",
                  text_color="white", font=("Arial", 12, "bold"),
                  command=valider).place(relx=0.5, y=170, anchor="center")

    ctk.CTkButton(frame, text="Créer un compte", fg_color="transparent",
                  text_color="#0077CC", hover_color="#e0e0e0",
                  command=show_register).place(relx=0.5, y=215, anchor="center")

    ctk.CTkButton(frame, text="Mot de passe oublié ?", fg_color="transparent",
                  text_color="#CC0000", hover_color="#e0e0e0",
                  command=show_forgot).place(relx=0.5, y=255, anchor="center")

def valider():
    utilisateur = entry_user.get().strip()
    mot_de_passe = entry_pass.get().strip()
    
    if utilisateur == "" or mot_de_passe == "":
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
    else:
        messagebox.showinfo("Connexion réussie", f"Bienvenue {utilisateur} !")
        fenetre.destroy()
        p2.main()

# ---------------- REGISTER ----------------
def show_register():
    clear_frame()

    ctk.CTkLabel(frame, text="Créer un compte", text_color="black", font=("Arial", 16, "bold")).place(relx=0.5, y=25, anchor="center")

    global reg_name, reg_email, reg_user, reg_pass, reg_confirm
    reg_name = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Nom complet", fg_color="#f2f2f2", text_color="black")
    reg_name.place(relx=0.5, y=65, anchor="center")

    reg_email = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Email", fg_color="#f2f2f2", text_color="black")
    reg_email.place(relx=0.5, y=105, anchor="center")

    reg_user = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Nom d'utilisateur", fg_color="#f2f2f2", text_color="black")
    reg_user.place(relx=0.5, y=145, anchor="center")

    reg_pass = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Mot de passe", show="*", fg_color="#f2f2f2", text_color="black")
    reg_pass.place(relx=0.5, y=185, anchor="center")

    reg_confirm = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Confirmer le mot de passe", show="*", fg_color="#f2f2f2", text_color="black")
    reg_confirm.place(relx=0.5, y=225, anchor="center")

    ctk.CTkButton(frame, text="Créer le compte", width=160, height=38,
                  corner_radius=18, fg_color="#F77F00", hover_color="#E57100",
                  text_color="white", font=("Arial", 12, "bold"),
                  command=register_action).place(relx=0.5, y=275, anchor="center")

    ctk.CTkButton(frame, text="← Retour", fg_color="transparent", text_color="#0077CC",
                  hover_color="#e0e0e0", command=show_login).place(relx=0.5, y=315, anchor="center")

def register_action():
    if not reg_name.get() or not reg_email.get() or not reg_user.get() or not reg_pass.get() or not reg_confirm.get():
        messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
        return
    if reg_pass.get() != reg_confirm.get():
        messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
        return
    messagebox.showinfo("Succès", "Compte créé (UI seulement).")
    show_login()

# ---------------- FORGOT PASSWORD ----------------
def show_forgot():
    clear_frame()

    ctk.CTkLabel(frame, text="Mot de passe oublié", text_color="black", font=("Arial", 16, "bold")).place(relx=0.5, y=25, anchor="center")

    global fp_email, fp_code, fp_new, fp_confirm, fp_step
    fp_step = 1
    fp_email = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Entrez votre email", fg_color="#f2f2f2", text_color="black")
    fp_email.place(relx=0.5, y=65, anchor="center")

    fp_code = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Code reçu par email", fg_color="#f2f2f2", text_color="black")
    fp_new = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Nouveau mot de passe", show="*", fg_color="#f2f2f2", text_color="black")
    fp_confirm = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Confirmer le mot de passe", show="*", fg_color="#f2f2f2", text_color="black")

    ctk.CTkButton(frame, text="Continuer", width=160, height=38, corner_radius=18,
                  fg_color="#F77F00", hover_color="#E57100", text_color="white",
                  command=forgot_action).place(relx=0.5, y=115, anchor="center")

    ctk.CTkButton(frame, text="← Retour", fg_color="transparent", text_color="#0077CC",
                  hover_color="#e0e0e0", command=show_login).place(relx=0.5, y=155, anchor="center")

def forgot_action():
    global fp_step
    code_sent = "1234"  # fake code
    if fp_step == 1:
        if fp_email.get() == "":
            messagebox.showerror("Erreur", "Veuillez saisir votre email.")
            return
        messagebox.showinfo("Code envoyé", f"Un code vous a été envoyé (test={code_sent}).")
        fp_email.place_forget()
        fp_code.place(relx=0.5, y=65, anchor="center")
        fp_step = 2
    elif fp_step == 2:
        if fp_code.get() != "1234":
            messagebox.showerror("Erreur", "Code incorrect.")
            return
        fp_code.place_forget()
        fp_new.place(relx=0.5, y=65, anchor="center")
        fp_confirm.place(relx=0.5, y=105, anchor="center")
        fp_step = 3
    elif fp_step == 3:
        if fp_new.get() == "" or fp_confirm.get() == "":
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return
        if fp_new.get() != fp_confirm.get():
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return
        messagebox.showinfo("Succès", "Mot de passe réinitialisé (UI seulement).")
        show_login()

# -------------------- Window Initialization --------------------
fenetre = Tk()
fenetre.title("Connexion - Réservation sportive")
fenetre.state('zoomed')
fenetre.update_idletasks()

try:
    image = Image.open("background.jpg")
    image = image.resize((fenetre.winfo_width(), fenetre.winfo_height()))
    bg_photo = ImageTk.PhotoImage(image)
    
    bg_canvas = Canvas(fenetre, highlightthickness=0)
    bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
    bg_canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    bg_canvas.image = bg_photo

except:
    fenetre.configure(bg="white")

frame = ctk.CTkFrame(fenetre, width=320, height=300,
                     fg_color="white", border_width=1, border_color="lightgray")
frame.place(relx=0.5, rely=0.5, anchor="center")

show_login()
fenetre.bind("<Return>", lambda e: valider())
fenetre.mainloop()
