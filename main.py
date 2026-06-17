import json
import random
import os
import pygame
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ---------------------------------------------------------
# APP: InglesGo con Flash Cards
# Tecnología: Python + Tkinter
# Base de datos local: archivos JSON, txt
# ---------------------------------------------------------

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VERBS_FILE = DATA_DIR / "verbs.json"
PROGRESS_FILE = DATA_DIR / "progress.json"

BG = "#F2F7FF"
PRIMARY = "#3366FF"
SECONDARY = "#FFB703"
SUCCESS = "#2A9D8F"
DANGER = "#E63946"
TEXT = "#1D3557"


def load_json(path, default):
    """Carga un archivo JSON. Si no existe o falla, devuelve un valor por defecto."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return default


def save_json(path, data):
    """Guarda datos en formato JSON."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


class FlashCardApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Aprendiendo Inglés con Flash Cards")
        self.geometry("980x650")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.verbs = load_json(VERBS_FILE, [])
        self.progress = load_json(PROGRESS_FILE, {"correct": 0, "incorrect": 0, "verbs": {}})

        self.current_index = 0
        self.current_verb = None
        self.current_image = None

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)

        self.show_home()
        
        self.hints_left = 3 #contador de pistas en construciopn de oraciones

    # -------------------------
    # UTILIDADES DE INTERFAZ
    # -------------------------
    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def title_label(self, text):
        return tk.Label(
            self.container,
            text=text,
            font=("Arial", 28, "bold"),
            fg=TEXT,
            bg=BG
        )

    def normal_label(self, text, size=15):
        return tk.Label(
            self.container,
            text=text,
            font=("Arial", size),
            fg=TEXT,
            bg=BG
        )

    def big_button(self, text, command, color=PRIMARY):
        return tk.Button(
            self.container,
            text=text,
            command=command,
            font=("Arial", 16, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            width=22,
            height=2,
            relief="flat",
            cursor="hand2"
        )

    # -------------------------
    # PANTALLA DE INICIO
    # -------------------------
    def show_home(self):
        self.clear_screen()

        tk.Label(
            self.container,
            text="🧠 Aprendiendo Inglés",
            font=("Arial", 34, "bold"),
            fg=PRIMARY,
            bg=BG
        ).pack(pady=(55, 5))

        tk.Label(
            self.container,
            text="Flash Cards de verbos + constructor de oraciones",
            font=("Arial", 17),
            fg=TEXT,
            bg=BG
        ).pack(pady=10)

        tk.Label(
            self.container,
            text="Practica verbos en inglés, escucha la pronunciación y crea oraciones en presente, pasado y futuro.",
            font=("Arial", 13),
            fg="#444",
            bg=BG,
            wraplength=760,
            justify="center"
        ).pack(pady=15)

        self.big_button("Comenzar Flash Cards", self.show_flashcards, PRIMARY).pack(pady=12)
        self.big_button("Constructor de Oraciones", self.show_sentence_builder, SUCCESS).pack(pady=12)
        self.big_button("Mi Progreso", self.show_progress, SECONDARY).pack(pady=12)

        tk.Label(
            self.container,
            text="Proyecto Final - Taller de Programación",
            font=("Arial", 11),
            fg="#555",
            bg=BG
        ).pack(side="bottom", pady=22)

    # -------------------------
    # MÓDULO FLASH CARDS
    # -------------------------
    def show_flashcards(self):
        self.clear_screen()

        if not self.verbs:
            messagebox.showerror("Error", "No hay verbos cargados en data/verbs.json")
            self.show_home()
            return

        self.current_index = self.current_index % len(self.verbs)
        self.current_verb = self.verbs[self.current_index]

        self.title_label("Flash Cards").pack(pady=(22, 8))

        tk.Label(
            self.container,
            text="Observa la imagen, escucha el audio y escribe el verbo en inglés.",
            font=("Arial", 14),
            bg=BG,
            fg=TEXT
        ).pack(pady=5)

        self.image_label = tk.Label(self.container, bg=BG)
        self.image_label.pack(pady=12)
        self.load_card_image()

        self.answer_entry = tk.Entry(
            self.container,
            font=("Arial", 20),
            width=25,
            justify="center"
        )
        self.answer_entry.pack(pady=8)
        self.answer_entry.focus()

        self.feedback_label = tk.Label(
            self.container,
            text="",
            font=("Arial", 17, "bold"),
            bg=BG
        )
        self.feedback_label.pack(pady=8)

        buttons_frame = tk.Frame(self.container, bg=BG)
        buttons_frame.pack(pady=10)

        tk.Button(
            buttons_frame,
            text="Escuchar 🔊",
            command=self.speak_current_verb,
            font=("Arial", 14, "bold"),
            bg=SECONDARY,
            fg="white",
            width=14,
            height=2,
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            buttons_frame,
            text="Verificar",
            command=self.check_answer,
            font=("Arial", 14, "bold"),
            bg=SUCCESS,
            fg="white",
            width=14,
            height=2,
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            buttons_frame,
            text="Siguiente",
            command=self.next_card,
            font=("Arial", 14, "bold"),
            bg=PRIMARY,
            fg="white",
            width=14,
            height=2,
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            self.container,
            text="Volver al inicio",
            command=self.show_home,
            font=("Arial", 12, "bold"),
            bg="#6c757d",
            fg="white",
            width=18,
            relief="flat",
            cursor="hand2"
        ).pack(pady=14)

    def load_card_image(self):
        """Carga la imagen de la tarjeta actual."""
        image_path = BASE_DIR / self.current_verb.get("image", "")
        try:
            image = Image.open(image_path)
            image = image.resize((430, 275))
            self.current_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.current_image)
        except Exception:
            self.image_label.config(
                text="Imagen no encontrada",
                font=("Arial", 20),
                fg=DANGER
            )

    def speak_current_verb(self):

        audio_file = self.current_verb.get("audio")

        if not audio_file:
            messagebox.showerror("Error", "Este verbo no tiene audio")
            return

        audio_path = os.path.join(BASE_DIR, audio_file)

        try:
            pygame.mixer.init()

            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

        except Exception as e:
            messagebox.showinfo("Audio", f"No se pudo reproducir:\n{e}")

    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.current_verb["base"].lower()

        # Requisito: no distinguir mayúsculas/minúsculas.
        if user_answer == correct_answer:
            self.feedback_label.config(text="✅ Correcto", fg=SUCCESS)
            self.register_result(correct=True)
        else:
            self.feedback_label.config(
                text=f"❌ Incorrecto. Respuesta: {self.current_verb['base']}",
                fg=DANGER
            )
            self.register_result(correct=False)

    def register_result(self, correct):
        """Actualiza el progreso del usuario en el archivo progress.json."""
        verb = self.current_verb["base"]

        if verb not in self.progress["verbs"]:
            self.progress["verbs"][verb] = {"correct": 0, "incorrect": 0, "mastered": False}

        if correct:
            self.progress["correct"] += 1
            self.progress["verbs"][verb]["correct"] += 1
        else:
            self.progress["incorrect"] += 1
            self.progress["verbs"][verb]["incorrect"] += 1

        # Criterio simple: un verbo queda dominado con 3 aciertos.
        if self.progress["verbs"][verb]["correct"] >= 3:
            self.progress["verbs"][verb]["mastered"] = True

        save_json(PROGRESS_FILE, self.progress)

    def next_card(self):
        self.current_index += 1
        self.show_flashcards()

    # -------------------------
    # MÓDULO CONSTRUCTOR
    # -------------------------
    def show_sentence_builder(self):
        self.clear_screen()

        self.title_label("Constructor de Oraciones").pack(pady=(25, 5))

        tk.Label(
            self.container,
            text="Arma una oración con estructura básica: Sujeto + Verbo + Complemento.",
            font=("Arial", 14),
            fg=TEXT,
            bg=BG
        ).pack(pady=5)

        self.builder_verb = random.choice(self.verbs)

        card = tk.Frame(self.container, bg="white", padx=25, pady=20)
        card.pack(pady=18)

        tk.Label(
            card,
            text=f"Verbo base: {self.builder_verb['base']}  |  Español: {self.builder_verb['spanish']}",
            font=("Arial", 18, "bold"),
            fg=PRIMARY,
            bg="white"
        ).pack(pady=5)

        tk.Label(
            card,
            text=f"Complemento sugerido: {self.builder_verb['object']}",
            font=("Arial", 13),
            fg="#444",
            bg="white"
        ).pack(pady=5)

        self.entries = {}

        self.create_sentence_row(card, "Presente Simple", "present")
        self.create_sentence_row(card, "Pasado Simple", "past")
        self.create_sentence_row(card, "Futuro will", "future")

        self.builder_feedback = tk.Label(
            self.container,
            text="",
            font=("Arial", 15, "bold"),
            bg=BG
        )
        self.builder_feedback.pack(pady=8)

        tk.Button(
            self.container,
            text="Verificar oraciones",
            command=self.check_sentences,
            font=("Arial", 15, "bold"),
            bg=SUCCESS,
            fg="white",
            width=22,
            height=2,
            relief="flat",
            cursor="hand2"
        ).pack(pady=8)

        tk.Button(
            self.container,
            text="Nuevo verbo",
            command=self.show_sentence_builder,
            font=("Arial", 13, "bold"),
            bg=PRIMARY,
            fg="white",
            width=18,
            relief="flat",
            cursor="hand2"
        ).pack(pady=5)

        tk.Button(
            self.container,
            text="Volver al inicio",
            command=self.show_home,
            font=("Arial", 12, "bold"),
            bg="#6c757d",
            fg="white",
            width=18,
            relief="flat",
            cursor="hand2"
        ).pack(pady=8)
        
        tk.Button(
            self.container,
            text=f"Pista ({self.hints_left})",
            command=self.give_hint,
            font=("Arial", 13, "bold"),
            bg="#ff9800",
            fg="white",
            width=18,
            relief="flat",
            cursor="hand2"
        ).pack(pady=5)

    def create_sentence_row(self, parent, label, key):
        row = tk.Frame(parent, bg="white")
        row.pack(pady=8)

        tk.Label(
            row,
            text=label,
            font=("Arial", 13, "bold"),
            fg=TEXT,
            bg="white",
            width=17,
            anchor="w"
        ).grid(row=0, column=0, padx=5)

        entry = tk.Entry(row, font=("Arial", 15), width=42)
        entry.grid(row=0, column=1, padx=5)

        self.entries[key] = entry

    def check_sentences(self):
        subject = "i"
        obj = self.builder_verb["object"].lower()

        expected = {
            "present": f"{subject} {self.builder_verb['base'].lower()} {obj}",
            "past": f"{subject} {self.builder_verb['past'].lower()} {obj}",
            "future": f"{subject} {self.builder_verb['future'].lower()} {obj}",
        }

        results = []

        for key, expected_sentence in expected.items():
            user_sentence = self.entries[key].get().strip().lower()
            user_sentence = " ".join(user_sentence.split())

            if user_sentence == expected_sentence:
                results.append(True)
            else:
                results.append(False)

        if all(results):
            self.builder_feedback.config(text="✅ Correcto", fg=SUCCESS)
        else:
            self.builder_feedback.config(text="❌ Incorrecto", fg=DANGER)

    # -------------------------
    # PANTALLA DE PROGRESO
    # -------------------------
    def show_progress(self):
        self.clear_screen()

        self.title_label("Mi Progreso").pack(pady=(30, 10))

        total_verbs = len(self.verbs)
        mastered = 0

        for verb in self.verbs:
            info = self.progress["verbs"].get(verb["base"], {})
            if info.get("mastered"):
                mastered += 1

        percent = int((mastered / total_verbs) * 100) if total_verbs else 0

        tk.Label(
            self.container,
            text=f"Verbos dominados: {mastered}/{total_verbs}",
            font=("Arial", 20, "bold"),
            fg=PRIMARY,
            bg=BG
        ).pack(pady=5)

        tk.Label(
            self.container,
            text=f"Progreso general: {percent}%",
            font=("Arial", 18),
            fg=TEXT,
            bg=BG
        ).pack(pady=5)

        canvas = tk.Canvas(self.container, width=620, height=35, bg="white", highlightthickness=0)
        canvas.pack(pady=15)
        canvas.create_rectangle(0, 0, 620, 35, fill="#DDE7FF", outline="")
        canvas.create_rectangle(0, 0, int(620 * percent / 100), 35, fill=SUCCESS, outline="")
        canvas.create_text(310, 18, text=f"{percent}%", fill=TEXT, font=("Arial", 13, "bold"))

        tk.Label(
            self.container,
            text=f"Aciertos: {self.progress.get('correct', 0)}    Errores: {self.progress.get('incorrect', 0)}",
            font=("Arial", 15),
            fg=TEXT,
            bg=BG
        ).pack(pady=8)

        list_frame = tk.Frame(self.container, bg="white", padx=18, pady=15)
        list_frame.pack(pady=10)

        tk.Label(
            list_frame,
            text="Verbos por repasar",
            font=("Arial", 15, "bold"),
            fg=DANGER,
            bg="white"
        ).pack()

        weak_verbs = []
        for verb in self.verbs:
            info = self.progress["verbs"].get(verb["base"], {"correct": 0, "incorrect": 0, "mastered": False})
            if not info.get("mastered"):
                weak_verbs.append(f"{verb['base']}  |  aciertos: {info.get('correct', 0)}  errores: {info.get('incorrect', 0)}")

        if weak_verbs:
            text = "\n".join(weak_verbs[:10])
        else:
            text = "¡Excelente! Todos los verbos están dominados."

        tk.Label(
            list_frame,
            text=text,
            font=("Arial", 12),
            fg=TEXT,
            bg="white",
            justify="left"
        ).pack(pady=8)

        tk.Button(
            self.container,
            text="Reiniciar progreso",
            command=self.reset_progress,
            font=("Arial", 12, "bold"),
            bg=DANGER,
            fg="white",
            width=18,
            relief="flat",
            cursor="hand2"
        ).pack(pady=5)

        tk.Button(
            self.container,
            text="Volver al inicio",
            command=self.show_home,
            font=("Arial", 12, "bold"),
            bg="#6c757d",
            fg="white",
            width=18,
            relief="flat",
            cursor="hand2"
        ).pack(pady=8)

    def reset_progress(self):
        confirm = messagebox.askyesno("Confirmar", "¿Seguro que deseas reiniciar el progreso?")
        if confirm:
            self.progress = {"correct": 0, "incorrect": 0, "verbs": {}}
            save_json(PROGRESS_FILE, self.progress)
            self.show_progress()
            
    def give_hint(self): #Funcion de pistas para construccion de oraciones
        if self.hints_left <= 0:
            messagebox.showinfo("Pista", "Ya no tienes más pistas disponibles")
            return

        subject = "I"
        obj = self.builder_verb["object"]

        hints = {
            "present": f"{subject} {self.builder_verb['base']} {obj}",
            "past": f"{subject} {self.builder_verb['past']} {obj}",
            "future": f"{subject} {self.builder_verb['future']} {obj}",
        }

        # Mostrar pista parcial (solo la primera palabra clave)
        messagebox.showinfo(
            "Pista",
            f"Ejemplo:\n\n"
            f"Present: {hints['present']}\n"
            f"Past: {hints['past']}\n"
            f"Future: {hints['future']}"
        )

        self.hints_left -= 1


if __name__ == "__main__":
    app = FlashCardApp()
    app.mainloop()
