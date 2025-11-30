# stats_interactive.py
from tkinter import *
import customtkinter as ctk
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import home
from datetime import datetime
from tkinter import filedialog, messagebox

def main():
    fenetre = Tk()
    fenetre.title("Statistiques Interactives - Réservations Sportives")
    fenetre.configure(bg="#f2f2f2")
    fenetre.state("zoomed")

    # --- Menu Bar ---
    menubar = Menu(fenetre)
    fenetre.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Fichier", menu=file_menu)
    file_menu.add_command(label="Exporter vers Excel", command=lambda: export_to_excel(df))
    file_menu.add_separator()
    file_menu.add_command(label="Quitter", command=fenetre.quit)

    # --- Retour button ---
    ctk.CTkButton(fenetre, text="← Retour", width=80, height=30,
                  fg_color="#F77F00", hover_color="#E57100", font=("Arial", 10, "bold"),
                  command=lambda: back_home(fenetre)).pack(pady=10, anchor="nw", padx=10)

    # --- Titre ---
    ctk.CTkLabel(fenetre, text="Statistiques des Réservations", font=("Arial", 28, "bold"),
                 text_color="#1C9273").pack(pady=20)

    # --- Chargement CSV ---
    csv_file = os.path.join(os.path.dirname(__file__), "reservations.csv")
    if os.path.isfile(csv_file):
        df = pd.read_csv(csv_file, parse_dates=["date"], dayfirst=True)
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors='coerce')
    else:
        df = pd.DataFrame(columns=["nom", "date", "heure", "terrain", "forfait", "abonnement"])

    # --- Filtres ---
    frame_filters = Frame(fenetre, bg="#f2f2f2")
    frame_filters.pack(pady=10)

    ctk.CTkLabel(frame_filters, text="Filtrer par mois :", font=("Arial", 12, "bold")).pack(side=LEFT, padx=5)
    month_var = StringVar(value=datetime.now().strftime("%m/%Y"))
    months = sorted(df['date'].dt.strftime("%m/%Y").dropna().unique()) if not df.empty else []
    month_combo = ctk.CTkComboBox(frame_filters, values=months, variable=month_var, width=120)
    month_combo.pack(side=LEFT, padx=5)

    ctk.CTkLabel(frame_filters, text="Filtrer par terrain :", font=("Arial", 12, "bold")).pack(side=LEFT, padx=5)
    terrain_var = StringVar(value="Tous")
    all_terrains = ["Tous","Terrain de Football", "Terrain de Basketball", "Terrain de Tennis", "Salle de Handball", "Terrain de Padel"]
    terrain_combo = ctk.CTkComboBox(frame_filters, values=all_terrains, variable=terrain_var, width=150)
    terrain_combo.pack(side=LEFT, padx=5)

    # Update button
    ctk.CTkButton(frame_filters, text="Actualiser", width=80, height=30,
                  fg_color="#1C9273", hover_color="#148F5F", font=("Arial", 10, "bold"),
                  command=reload_data).pack(side=LEFT, padx=10)

    # --- Frame pour stats ---
    frame_stats = Frame(fenetre, bg="#f2f2f2")
    frame_stats.pack(pady=10, padx=20, fill=X)

    # --- Frame pour graph ---
    frame_graph = Frame(fenetre, bg="#f2f2f2")
    frame_graph.pack(pady=20, fill=BOTH, expand=True)

    # --- Fonction pour recharger les données ---
    def reload_data():
        nonlocal df, months
        if os.path.isfile(csv_file):
            df = pd.read_csv(csv_file, parse_dates=["date"], dayfirst=True)
            df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors='coerce')
            months = sorted(df['date'].dt.strftime("%m/%Y").dropna().unique()) if not df.empty else []
            month_combo.configure(values=months)
        else:
            df = pd.DataFrame(columns=["nom", "date", "heure", "terrain", "forfait", "abonnement"])
        update_stats()

    # --- Fonction pour mettre à jour stats et graph ---
    def update_stats():
        for widget in frame_stats.winfo_children():
            widget.destroy()
        for widget in frame_graph.winfo_children():
            widget.destroy()

        # Filtrage
        filtered_df = df.copy()
        month_selected = month_var.get()
        if month_selected and month_selected != "":
            month_dt = datetime.strptime("01/" + month_selected, "%d/%m/%Y")
            filtered_df = filtered_df[(filtered_df["date"].dt.month == month_dt.month) &
                                      (filtered_df["date"].dt.year == month_dt.year)]
        terrain_selected = terrain_var.get()
        if terrain_selected != "Tous":
            filtered_df = filtered_df[filtered_df["terrain"] == terrain_selected]

        # Stats principales
        monthly_reservations = filtered_df.shape[0]
        reserved_today = filtered_df[filtered_df["date"].dt.date == datetime.now().date()]["terrain"].tolist()
        available_terrains = len(set(all_terrains[1:]) - set(reserved_today))
        abon_count = filtered_df[filtered_df["abonnement"] == 1].shape[0]

        stats_list = [
            ("Réservations ce mois", monthly_reservations, "#F77F00"),
            ("Terrains disponibles aujourd'hui", available_terrains, "#1C9273"),
            ("Abonnés mensuels", abon_count, "#1F5061")
        ]

        for title, value, color in stats_list:
            box = ctk.CTkLabel(frame_stats, text=f"{title}\n{value}", width=400, height=100,
                                corner_radius=20, fg_color=color, text_color="white",
                                font=("Arial", 16, "bold"))
            box.pack(side=LEFT, padx=20, pady=10, expand=True, fill=BOTH)

        # --- Graphiques ---
        if not filtered_df.empty:
            # Réservations par jour
            daily_counts = filtered_df['date'].dt.date.value_counts().sort_index()
            fig1, ax1 = plt.subplots(figsize=(6,4))
            daily_counts.plot(kind='bar', color="#F77F00", ax=ax1)
            ax1.set_title("Réservations par jour")
            ax1.set_ylabel("Réservations")
            ax1.set_xlabel("Date")
            ax1.set_xticklabels([d.strftime("%d/%m") for d in daily_counts.index], rotation=45)
            canvas1 = FigureCanvasTkAgg(fig1, master=frame_graph)
            canvas1.draw()
            canvas1.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True, padx=10)

            # Réservations par terrain
            terrain_counts = filtered_df['terrain'].value_counts()
            fig2, ax2 = plt.subplots(figsize=(6,4))
            terrain_counts.plot(kind='pie', autopct='%1.1f%%',
                                colors=["#F77F00","#1C9273","#1F5061","#FFA500","#FF6F61"], ax=ax2)
            ax2.set_ylabel("")
            ax2.set_title("Réservations par terrain")
            canvas2 = FigureCanvasTkAgg(fig2, master=frame_graph)
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True, padx=10)

            # Additional curve: Reservations by hour
            hour_counts = filtered_df['heure'].value_counts().sort_index()
            fig3, ax3 = plt.subplots(figsize=(6,4))
            hour_counts.plot(kind='line', marker='o', color="#1C9273", ax=ax3)
            ax3.set_title("Réservations par heure")
            ax3.set_ylabel("Réservations")
            ax3.set_xlabel("Heure")
            ax3.grid(True)
            canvas3 = FigureCanvasTkAgg(fig3, master=frame_graph)
            canvas3.draw()
            canvas3.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True, padx=10)

    # --- Mettre à jour au changement ---
    month_combo.configure(command=lambda _: update_stats())
    terrain_combo.configure(command=lambda _: update_stats())

    # Initial
    update_stats()

    fenetre.mainloop()

def back_home(win):
    win.destroy()
    home.main()

def export_to_excel(df):
    if df.empty:
        messagebox.showwarning("Avertissement", "Aucune donnée à exporter.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Succès", f"Données exportées vers {file_path}")
