from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

from utils import load_json, save_json, BASE_DIR, BG, PRIMARY, SECONDARY, SUCCESS, DANGER, TEXT, GRAY, VERBS_FILE
from palabra import Palabra
from usuario import Usuario
from progreso import Progreso
from leccion import Leccion
from ejercicios import FlashCard, EjercicioSeleccion, EjercicioOracion


class InglesGoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("InglesGo")
        self.geometry("980x650")
        self.minsize(980, 650)
        self.configure(bg=BG)
        self.resizable(True, True)

        self.usuario_actual: Usuario | None = None
        self.progreso: Progreso | None = None

        verbs_data = load_json(VERBS_FILE, [])
        self.lecciones: list[Leccion] = Leccion.cargar_lecciones(verbs_data)
        self.leccion_actual: Leccion | None = None

        self._imagen_actual = None
        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)

        self.show_login()

    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def lbl(self, text, size=15, bold=False, color=TEXT, parent=None):
        p = parent or self.container
        fw = "bold" if bold else "normal"
        return tk.Label(p, text=text, font=("Arial", size, fw), fg=color, bg=BG)

    def btn(self, text, command, color=PRIMARY, width=22, parent=None):
        p = parent or self.container
        return tk.Button(
            p, text=text, command=command,
            font=("Arial", 14, "bold"), bg=color, fg="white",
            activebackground=color, activeforeground="white",
            width=width, height=2, relief="flat", cursor="hand2"
        )

    def entry(self, parent=None, show=None, width=30):
        p = parent or self.container
        kw = {"font": ("Arial", 14), "width": width}
        if show:
            kw["show"] = show
        return tk.Entry(p, **kw)

    def show_login(self):
        self.clear()

        self.lbl("InglesGo", 32, bold=True, color=PRIMARY).pack(pady=(50, 5))
        self.lbl("Your English Learning Adventure", 14).pack(pady=5)

        frame = tk.Frame(self.container, bg="white", padx=40, pady=30)
        frame.pack(pady=20)

        tk.Label(frame, text="Email", font=("Arial", 12), bg="white", fg=TEXT).pack(anchor="w")
        email_entry = tk.Entry(frame, font=("Arial", 14), width=30)
        email_entry.pack(pady=(2, 12))

        tk.Label(frame, text="Password", font=("Arial", 12), bg="white", fg=TEXT).pack(anchor="w")
        pass_entry = tk.Entry(frame, font=("Arial", 14), width=30, show="•")
        pass_entry.pack(pady=(2, 20))

        feedback = tk.Label(frame, text="", font=("Arial", 12), bg="white", fg=DANGER)
        feedback.pack()

        def intentar_login():
            u = Usuario.iniciar_sesion(email_entry.get(), pass_entry.get())
            if u:
                self.usuario_actual = u
                self.progreso       = Progreso(u.id)
                self.show_home()
            else:
                feedback.config(text="Incorrect email or password.")

        tk.Button(
            frame, text="Sign In →", command=intentar_login,
            font=("Arial", 14, "bold"), bg=PRIMARY, fg="white",
            width=24, height=2, relief="flat", cursor="hand2"
        ).pack(pady=8)

        tk.Button(
            frame, text="Don't have an account? Sign Up",
            command=self.show_registro,
            font=("Arial", 11), bg="white", fg=PRIMARY,
            relief="flat", cursor="hand2"
        ).pack()

        # Bind Enter
        self.bind("<Return>", lambda e: intentar_login())

    # =========================================================
    # PANTALLA: Registro
    # =========================================================

    def show_registro(self):
        self.clear()

        self.lbl("Create Account", 28, bold=True, color=PRIMARY).pack(pady=(40, 5))

        frame = tk.Frame(self.container, bg="white", padx=40, pady=30)
        frame.pack(pady=20)

        campos = {}
        for label, key, hide in [
            ("Name", "nombre", False),
            ("Email",  "email",  False),
            ("Password", "password", True),
        ]:
            tk.Label(frame, text=label, font=("Arial", 12), bg="white", fg=TEXT).pack(anchor="w")
            e = tk.Entry(frame, font=("Arial", 14), width=30, show="•" if hide else "")
            e.pack(pady=(2, 12))
            campos[key] = e

        feedback = tk.Label(frame, text="", font=("Arial", 12), bg="white")
        feedback.pack()

        def intentar_registro():
            ok, msg = Usuario.crear_cuenta(
                campos["nombre"].get(),
                campos["email"].get(),
                campos["password"].get(),
            )
            if ok:
                feedback.config(text=msg, fg=SUCCESS)
                self.after(1500, self.show_login)
            else:
                feedback.config(text=msg, fg=DANGER)

        tk.Button(
            frame, text="Create Account", command=intentar_registro,
            font=("Arial", 14, "bold"), bg=SUCCESS, fg="white",
            width=24, height=2, relief="flat", cursor="hand2"
        ).pack(pady=8)

        tk.Button(
            frame, text="← Back to Login", command=self.show_login,
            font=("Arial", 11), bg="white", fg=GRAY,
            relief="flat", cursor="hand2"
        ).pack()

    # =========================================================
    # PANTALLA: Home / Dashboard
    # =========================================================

    def show_home(self):
        self.clear()
        u = self.usuario_actual
        p = self.progreso

        self.lbl(f"Welcome, {u.nombre}!", 26, bold=True, color=PRIMARY).pack(pady=(30, 5))

        total = sum(len(l.obtener_palabras()) for l in self.lecciones)
        pct   = p.calcular_porcentaje(total)

        stats = tk.Frame(self.container, bg=BG)
        stats.pack(pady=10)

        for icon, val in [("⚡ XP", u.xp), ("🔥 Streak", u.racha), ("📊 Level", u.nivel)]:
            col = tk.Frame(stats, bg="white", padx=20, pady=12)
            col.pack(side="left", padx=10)
            tk.Label(col, text=icon, font=("Arial", 12), bg="white", fg=GRAY).pack()
            tk.Label(col, text=str(val), font=("Arial", 20, "bold"), bg="white", fg=TEXT).pack()

        self.lbl(f"Overall Progress: {pct}%", 14, color=GRAY).pack(pady=(15, 5))

        canvas = tk.Canvas(self.container, height=20, bg="#DDE7FF", highlightthickness=0)
        canvas.pack(fill="x", padx=60)
        self._draw_progress_bar(canvas, pct, height=20, color=SUCCESS)

        self.lbl("Available Lessons", 16, bold=True).pack(pady=(20, 5))

        btn_frame = tk.Frame(self.container, bg=BG)
        btn_frame.pack()
        for leccion in self.lecciones:
            tk.Button(
                btn_frame,
                text=f"Unit {leccion.unidad}: {leccion.titulo}",
                command=lambda l=leccion: self.show_selector_modo(l),
                font=("Arial", 13, "bold"), bg=PRIMARY, fg="white",
                width=30, height=2, relief="flat", cursor="hand2", pady=4
            ).pack(pady=4)

        sep = tk.Frame(self.container, bg=BG)
        sep.pack(pady=5)

        row = tk.Frame(self.container, bg=BG)
        row.pack()
        self.btn("My Progress", self.show_progreso, color=SECONDARY, width=18, parent=row).pack(side="left", padx=8)
        self.btn("Sign Out", self._cerrar_sesion, color=GRAY, width=18, parent=row).pack(side="left", padx=8)

    def _cerrar_sesion(self):
        self.usuario_actual = None
        self.progreso       = None
        self.show_login()

    # =========================================================
    # SCREEN: Mode Selector
    # =========================================================

    def show_selector_modo(self, leccion: Leccion):
        self.leccion_actual = leccion
        self.clear()

        self.lbl(f"Unit {leccion.unidad}: {leccion.titulo}", 24, bold=True, color=PRIMARY).pack(pady=(30, 5))
        self.lbl(leccion.descripcion, 13, color=GRAY).pack(pady=5)
        self.lbl("Choose How to Learn", 18, bold=True).pack(pady=(20, 10))

        modos = [
            ("🃏  Flashcards",         "Review words with interactive cards",           self.show_flashcards, PRIMARY),
            ("✅  Multiple Choice",    "Pick the correct translation from 4 options",    self.show_seleccion,  SUCCESS),
            ("✍️  Build Sentences",    "Order the words to build sentences",             self.show_oraciones,  SECONDARY),
        ]

        for titulo, desc, cmd, color in modos:
            f = tk.Frame(self.container, bg="white", padx=20, pady=14)
            f.pack(pady=6, fill="x", padx=80)
            tk.Label(f, text=titulo, font=("Arial", 15, "bold"), bg="white", fg=color).pack(anchor="w")
            tk.Label(f, text=desc,   font=("Arial", 12),         bg="white", fg=GRAY).pack(anchor="w")
            tk.Button(
                f, text="Start! ⚡", command=cmd,
                font=("Arial", 12, "bold"), bg=color, fg="white",
                relief="flat", cursor="hand2", padx=16, pady=6
            ).pack(anchor="e", pady=(6, 0))

        self.btn("← Back", self.show_home, color=GRAY, width=14).pack(pady=16)

    # =========================================================
    # SCREEN: FlashCards
    # =========================================================

    def show_flashcards(self):
        palabras = self.leccion_actual.obtener_palabras()
        if not palabras:
            messagebox.showerror("Error", "No words in this lesson.")
            return

        self._fc = FlashCard(palabras)
        self._render_flashcard()

    def _render_flashcard(self):
        self.clear()
        fc      = self._fc
        palabra = fc.palabra_actual
        actual, total = fc.get_progreso()
        es_reverso    = fc.es_reverso()

        self.lbl(f"Unit {self.leccion_actual.unidad}: {self.leccion_actual.titulo}", 18, bold=True, color=PRIMARY).pack(pady=(20, 2))
        self.lbl(f"{actual} / {total} words", 12, color=GRAY).pack()

        # Progress bar
        canvas_bar = tk.Canvas(self.container, height=8, bg="#DDE7FF", highlightthickness=0)
        canvas_bar.pack(fill="x", padx=60, pady=6)
        self._draw_progress_bar(canvas_bar, int(100 * actual / total), height=8, color=PRIMARY)

        # Card
        card = tk.Frame(self.container, bg="white", padx=30, pady=20)
        card.pack(pady=10, padx=60, fill="x")

        if not es_reverso:
            # FRONT
            row = tk.Frame(card, bg="white")
            row.pack(pady=10, fill="x")
            self._cargar_imagen(row, palabra, size=(220, 170), centered=True)
            tk.Label(card, text="Tap to flip", font=("Arial", 12), bg="white", fg=GRAY).pack(pady=(8, 0))
        else:
            # REVERSE
            info = tk.Frame(card, bg="white")
            info.pack(pady=10)
            tk.Label(info, text=palabra.infinitivo,
                     font=("Arial", 36, "bold"), fg=PRIMARY, bg="white").pack(pady=(0, 10))
            tk.Label(info, text=palabra.traduccion,
                     font=("Arial", 24, "bold"), fg=TEXT, bg="white").pack(pady=(0, 10))
            tk.Label(info, text=f"Present: {palabra.presente}  |  Past: {palabra.pasado}  |  Future: {palabra.futuro}",
                     font=("Arial", 13), fg=GRAY, bg="white").pack(pady=(0, 12))
            tk.Button(info, text="🔊 Listen",
                      command=lambda: self._reproducir_audio(palabra),
                      font=("Arial", 12, "bold"), bg=SECONDARY, fg="white",
                      relief="flat", cursor="hand2", padx=10, pady=4).pack()

        tk.Button(card, text="🔄 Flip Card",
                  command=lambda: [fc.voltear(), self._render_flashcard()],
                  font=("Arial", 12), bg="#EEF2FF", fg=PRIMARY,
                  relief="flat", cursor="hand2", padx=12, pady=4).pack(pady=(10, 0))

        # Navigation
        nav = tk.Frame(self.container, bg=BG)
        nav.pack(pady=12)

        tk.Button(nav, text="← Previous",
                  command=lambda: [fc.anterior(), self._render_flashcard()],
                  font=("Arial", 13, "bold"), bg="#E0E0E0", fg=TEXT,
                  width=12, height=2, relief="flat", cursor="hand2").grid(row=0, column=0, padx=10)

        tk.Button(nav, text="Next →",
                  command=lambda: [fc.siguiente(), self._render_flashcard()],
                  font=("Arial", 13, "bold"), bg=PRIMARY, fg="white",
                  width=12, height=2, relief="flat", cursor="hand2").grid(row=0, column=1, padx=10)

        self.btn("← Back to Selector", lambda: self.show_selector_modo(self.leccion_actual),
                 color=GRAY, width=22).pack(pady=4)

    def _cargar_imagen(self, parent, palabra: Palabra, size: tuple = (160, 120), centered: bool = False):
        path = BASE_DIR / palabra.imagen_url
        try:
            img = Image.open(path).resize(size)
            self._imagen_actual = ImageTk.PhotoImage(img)
            if centered:
                tk.Label(parent, image=self._imagen_actual, bg="white").pack(pady=0)
            else:
                tk.Label(parent, image=self._imagen_actual, bg="white").pack(side="left")
        except Exception:
            if centered:
                tk.Label(parent, text="[imagen]", font=("Arial", 12), fg=GRAY, bg="white").pack(pady=0)
            else:
                tk.Label(parent, text="[imagen]", font=("Arial", 12), fg=GRAY, bg="white").pack(side="left")

    def _reproducir_audio(self, palabra: Palabra):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(palabra.infinitivo)
            engine.runAndWait()
        except Exception as e:
            messagebox.showinfo("Audio", f"Could not play audio:\n{e}")

    def _draw_progress_bar(self, canvas: tk.Canvas, percent: int, height: int = 20, color: str = PRIMARY, show_text: bool = False):
        canvas.update_idletasks()
        width = canvas.winfo_width() or canvas.winfo_reqwidth()
        if width <= 0:
            width = 600
        fill_width = int(width * max(0, min(percent, 100)) / 100)
        canvas.create_rectangle(0, 0, width, height, fill="#DDE7FF", outline="")
        canvas.create_rectangle(0, 0, fill_width, height, fill=color, outline="")
        if show_text:
            canvas.create_text(width // 2, height // 2, text=f"{percent}%", fill=TEXT, font=("Arial", 11, "bold"))

    # =========================================================
    # SCREEN: Multiple Choice Exercise
    # =========================================================

    def show_seleccion(self):
        palabras = self.leccion_actual.obtener_palabras()
        if not palabras:
            messagebox.showerror("Error", "No words in this lesson.")
            return
        self._quiz = EjercicioSeleccion(palabras)
        self._render_seleccion()

    def _render_seleccion(self):
        self.clear()
        quiz    = self._quiz
        palabra = quiz.palabra

        self.lbl(f"Select the Correct Translation", 20, bold=True, color=PRIMARY).pack(pady=(25, 5))
        self.lbl(f"Unit {self.leccion_actual.unidad}: {self.leccion_actual.titulo}", 12, color=GRAY).pack()

        # Question card
        card = tk.Frame(self.container, bg="white", padx=30, pady=20)
        card.pack(pady=15, padx=80, fill="x")

        row = tk.Frame(card, bg="white")
        row.pack(pady=10, fill="x")
        self._cargar_imagen(row, palabra, size=(220, 170), centered=True)
        tk.Button(row, text="🔊", command=lambda: self._reproducir_audio(palabra),
                  font=("Arial", 14), bg=SECONDARY, fg="white",
                  relief="flat", cursor="hand2", padx=16, pady=8).pack(pady=(10, 0))

        # Options
        feedback_lbl = tk.Label(self.container, text="", font=("Arial", 14, "bold"), bg=BG)
        feedback_lbl.pack(pady=5)

        opts_frame = tk.Frame(self.container, bg=BG)
        opts_frame.pack()

        def seleccionar(opcion, btns):
            correcto = quiz.verificar_respuesta(opcion)
            self.progreso.actualizar_progreso(palabra, correcto)
            if correcto:
                self.usuario_actual.agregar_xp(10)
                feedback_lbl.config(text="✅ Correct! +10 XP", fg=SUCCESS)
            else:
                feedback_lbl.config(text=f"❌ Wrong. It was: {quiz.respuesta_correcta}", fg=DANGER)
            for b in btns:
                b.config(state="disabled")
            self.after(1800, lambda: [quiz.nueva_pregunta(), self._render_seleccion()])

        btns = []
        for i, opcion in enumerate(quiz.opciones):
            b = tk.Button(
                opts_frame, text=opcion,
                font=("Arial", 14, "bold"), bg="white", fg=TEXT,
                width=18, height=2, relief="solid", cursor="hand2",
                bd=1
            )
            b.grid(row=i // 2, column=i % 2, padx=10, pady=6)
            btns.append(b)

        for b in btns:
            b.config(command=lambda op=b["text"], bs=btns: seleccionar(op, bs))

        self.btn("← Back to Selector",
                 lambda: self.show_selector_modo(self.leccion_actual),
                 color=GRAY, width=22).pack(pady=14)

    # =========================================================
    # SCREEN: Build Sentences Exercise
    # =========================================================

    def show_oraciones(self):
        palabras = self.leccion_actual.obtener_palabras()
        if not palabras:
            messagebox.showerror("Error", "No words in this lesson.")
            return
        self._oracion = EjercicioOracion(palabras, tiempo="present")
        self._palabras_seleccionadas = []
        self._render_oracion()

    def _render_oracion(self):
        self.clear()
        ej      = self._oracion
        palabra = ej.palabra

        self.lbl("Build the Sentence in English", 20, bold=True, color=PRIMARY).pack(pady=(20, 2))
        self.lbl(f"Unit {self.leccion_actual.unidad}: {self.leccion_actual.titulo}", 12, color=GRAY).pack()

        # ---------------------------------------------------
        # Tabs: Present | Past | Future
        # ---------------------------------------------------
        TIEMPOS = [("present", "Present"), ("past", "Past"), ("future", "Future")]

        tabs_frame = tk.Frame(self.container, bg=BG)
        tabs_frame.pack(pady=(14, 4))

        def cambiar_tiempo(tiempo):
            if tiempo == ej.tiempo:
                return
            ej.set_tiempo(tiempo)
            self._palabras_seleccionadas = []
            self._render_oracion()

        for clave, etiqueta in TIEMPOS:
            activo = (clave == ej.tiempo)
            tab_btn = tk.Button(
                tabs_frame, text=etiqueta,
                font=("Arial", 13, "bold"),
                bg=PRIMARY if activo else "white",
                fg="white" if activo else PRIMARY,
                relief="flat", bd=1, cursor="hand2",
                padx=22, pady=8,
                command=lambda t=clave: cambiar_tiempo(t)
            )
            tab_btn.pack(side="left", padx=4)

        # Image only, centered
        top = tk.Frame(self.container, bg=BG)
        top.pack(pady=10, fill="x")
        self._cargar_imagen(top, palabra, size=(220, 170), centered=True)

        # Answer zone
        respuesta_lbl = tk.Label(self.container,
                                 text=" ".join(self._palabras_seleccionadas) or "Click the words...",
                                 font=("Arial", 16), fg=TEXT if self._palabras_seleccionadas else GRAY,
                                 bg="white", padx=20, pady=12, relief="solid", bd=1, width=50)
        respuesta_lbl.pack(pady=8, padx=60)

        feedback_lbl = tk.Label(self.container, text="", font=("Arial", 14, "bold"), bg=BG)
        feedback_lbl.pack(pady=4)

        # Available words
        self.lbl("AVAILABLE WORDS", 11, color=GRAY).pack()
        palabras_frame = tk.Frame(self.container, bg=BG)
        palabras_frame.pack(pady=6)

        pal_btns = []
        for i, pal in enumerate(ej.palabras_disponibles):
            b = tk.Button(
                palabras_frame, text=pal,
                font=("Arial", 13), bg="white", fg=TEXT,
                relief="solid", bd=1, padx=10, pady=4, cursor="hand2"
            )
            b.grid(row=i // 5, column=i % 5, padx=4, pady=4)
            pal_btns.append(b)

        def agregar_palabra(pal, btn):
            self._palabras_seleccionadas.append(pal)
            btn.config(state="disabled", bg="#EEF2FF")
            respuesta_lbl.config(
                text=" ".join(self._palabras_seleccionadas),
                fg=TEXT
            )

        for b in pal_btns:
            b.config(command=lambda p=b["text"], bt=b: agregar_palabra(p, bt))

        # Action buttons
        acciones = tk.Frame(self.container, bg=BG)
        acciones.pack(pady=10)

        def verificar():
            respuesta = " ".join(self._palabras_seleccionadas)
            correcto  = ej.verificar_oracion(respuesta)
            self.progreso.actualizar_progreso(palabra, correcto)
            if correcto:
                self.usuario_actual.agregar_xp(15)
                feedback_lbl.config(text="✅ Correct! +15 XP", fg=SUCCESS)
            else:
                feedback_lbl.config(
                    text=f"❌ Wrong. Correct: {ej.oracion_correcta}", fg=DANGER
                )
            for b in pal_btns:
                b.config(state="disabled")
            self.after(2000, lambda: [ej.nueva_oracion(),
                                      self._palabras_seleccionadas.clear(),
                                      self._render_oracion()])

        def borrar():
            self._palabras_seleccionadas.clear()
            self._render_oracion()

        def pista():
            hint = ej.usar_pista()
            if hint:
                feedback_lbl.config(
                    text=f"💡 Hint ({ej.get_pistas_restantes()} left): {hint}",
                    fg=SECONDARY
                )
            else:
                feedback_lbl.config(text="No more hints available.", fg=GRAY)

        tk.Button(acciones, text="✅ Check", command=verificar,
                  font=("Arial", 13, "bold"), bg=SUCCESS, fg="white",
                  relief="flat", cursor="hand2", padx=14, pady=6).grid(row=0, column=0, padx=6)

        tk.Button(acciones, text="🗑 Clear", command=borrar,
                  font=("Arial", 13, "bold"), bg=DANGER, fg="white",
                  relief="flat", cursor="hand2", padx=14, pady=6).grid(row=0, column=1, padx=6)

        tk.Button(acciones, text=f"💡 Hint ({ej.get_pistas_restantes()})", command=pista,
                  font=("Arial", 13, "bold"), bg=SECONDARY, fg="white",
                  relief="flat", cursor="hand2", padx=14, pady=6).grid(row=0, column=2, padx=6)

        self.btn("← Back to Selector",
                 lambda: self.show_selector_modo(self.leccion_actual),
                 color=GRAY, width=22).pack(pady=8)

    # =========================================================
    # SCREEN: Progress
    # =========================================================

    def show_progreso(self):
        self.clear()
        p     = self.progreso
        u     = self.usuario_actual
        total = sum(len(l.obtener_palabras()) for l in self.lecciones)
        pct   = p.calcular_porcentaje(total)

        self.lbl("My Progress", 28, bold=True, color=PRIMARY).pack(pady=(30, 10))

        stats = tk.Frame(self.container, bg=BG)
        stats.pack(pady=10)
        for label, val in [
            ("⚡ Total XP",         u.xp),
            ("🏅 Score",           p.get_puntaje()),
            ("✅ Exercises",        p.get_ejercicios_completados()),
            ("🔥 Streak",          u.racha),
        ]:
            col = tk.Frame(stats, bg="white", padx=18, pady=12)
            col.pack(side="left", padx=8)
            tk.Label(col, text=label, font=("Arial", 11), bg="white", fg=GRAY).pack()
            tk.Label(col, text=str(val), font=("Arial", 20, "bold"), bg="white", fg=TEXT).pack()

        self.lbl(f"Overall Progress: {pct}%", 15).pack(pady=(18, 4))
        c = tk.Canvas(self.container, height=22, bg="#DDE7FF", highlightthickness=0)
        c.pack(fill="x", padx=60)
        self._draw_progress_bar(c, pct, height=22, color=SUCCESS, show_text=True)

        # By lesson
        self.lbl("Progress by Unit", 15, bold=True).pack(pady=(16, 4))
        for lec in self.lecciones:
            pal   = lec.obtener_palabras()
            pct_l = p.calcular_porcentaje(len(pal)) if pal else 0
            tk.Label(self.container,
                     text=f"Unit {lec.unidad} — {lec.titulo}: {pct_l}%",
                     font=("Arial", 13), bg=BG, fg=TEXT).pack()

        # Words to review
        debiles = p.get_verbos_debiles()
        if debiles:
            self.lbl("Words to review:", 13, color=DANGER).pack(pady=(12, 2))
            tk.Label(self.container,
                     text=", ".join(debiles[:12]),
                     font=("Arial", 12), bg=BG, fg=TEXT, wraplength=600).pack()

        row = tk.Frame(self.container, bg=BG)
        row.pack(pady=16)
        tk.Button(row, text="Reset Progress", command=self._confirmar_reset,
                  font=("Arial", 12, "bold"), bg=DANGER, fg="white",
                  width=18, relief="flat", cursor="hand2").pack(side="left", padx=8)
        self.btn("← Back", self.show_home, color=GRAY, width=14, parent=row).pack(side="left", padx=8)

    def _confirmar_reset(self):
        if messagebox.askyesno("Confirm", "Reset all progress?"):
            self.progreso.reiniciar()
            self.show_progreso()