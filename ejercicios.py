import random
from palabra import Palabra

class FlashCard:
    def __init__(self, palabras: list[Palabra]):
        self._palabras     = palabras
        self._indice       = 0
        self.palabra_actual: Palabra = palabras[0] if palabras else None
        self._mostrando_reverso = False

    # ----------------------------------------------------------
    def voltear(self) -> bool:
        """Alterna entre frente y reverso. Retorna True si ahora muestra reverso."""
        self._mostrando_reverso = not self._mostrando_reverso
        return self._mostrando_reverso

    def siguiente(self) -> Palabra:
        self._indice = (self._indice + 1) % len(self._palabras)
        self.palabra_actual = self._palabras[self._indice]
        self._mostrando_reverso = False
        return self.palabra_actual

    def anterior(self) -> Palabra:
        self._indice = (self._indice - 1) % len(self._palabras)
        self.palabra_actual = self._palabras[self._indice]
        self._mostrando_reverso = False
        return self.palabra_actual

    def es_reverso(self) -> bool:
        return self._mostrando_reverso

    def get_progreso(self) -> tuple[int, int]:
        return self._indice + 1, len(self._palabras)


# =============================================================
# CLASE: EjercicioSeleccion
# Quiz de selección múltiple (4 opciones)
# =============================================================

class EjercicioSeleccion:
    def __init__(self, palabras: list[Palabra]):
        self._palabras = palabras
        self.palabra: Palabra = None
        self.opciones: list[str] = []
        self.respuesta_correcta: str = ""
        self.nueva_pregunta()

    # ----------------------------------------------------------
    def nueva_pregunta(self):
        self.palabra = random.choice(self._palabras)
        self.respuesta_correcta = self.palabra.infinitivo
        incorrectas = [
            p.infinitivo for p in self._palabras
            if p.infinitivo != self.respuesta_correcta
        ]
        seleccion = random.sample(incorrectas, min(3, len(incorrectas)))
        self.opciones = seleccion + [self.respuesta_correcta]
        random.shuffle(self.opciones)

    def verificar_respuesta(self, opcion: str) -> bool:
        return opcion.strip().lower() == self.respuesta_correcta.strip().lower()


# =============================================================
# CLASE: EjercicioOracion
# Constructor de oraciones con palabras disponibles
# Soporta los 3 tiempos verbales: present, past, future
# =============================================================

class EjercicioOracion:
    HINTS_MAX = 3

    def __init__(self, palabras: list[Palabra], tiempo: str = "present"):
        self._palabras           = palabras
        self.tiempo               = tiempo  # "present" | "past" | "future"
        self.palabra: Palabra     = None
        self.sujeto: str          = ""
        self.palabras_disponibles: list[str] = []
        self.oracion_correcta: str = ""
        self._pistas_restantes    = self.HINTS_MAX
        self.nueva_oracion()

    # ----------------------------------------------------------
    def set_tiempo(self, tiempo: str):
        """Cambia el tiempo verbal activo (present/past/future) y genera una nueva oración."""
        self.tiempo = tiempo
        self.nueva_oracion()

    def nueva_oracion(self):
        self.palabra = random.choice(self._palabras)
        fila = random.choice(self.palabra.oraciones) if self.palabra.oraciones else None

        if fila:
            self.sujeto = fila.get("subject", "I")
            frase = fila.get(self.tiempo, "")
            self.oracion_correcta = f"{self.sujeto} {frase}".strip()
        else:
            # Compatibilidad si una palabra no trae 'sentences'
            self.sujeto = "I"
            self.oracion_correcta = f"I {self.palabra.infinitivo} {self.palabra.objeto}"

        palabras_correctas = self.oracion_correcta.split()
        distractores = [
            p.infinitivo for p in self._palabras
            if p.infinitivo != self.palabra.infinitivo
        ]
        extra = random.sample(distractores, min(5, len(distractores)))
        self.palabras_disponibles = palabras_correctas + extra
        random.shuffle(self.palabras_disponibles)

    def verificar_oracion(self, respuesta: str) -> bool:
        return " ".join(respuesta.strip().lower().split()) == self.oracion_correcta.lower()

    def usar_pista(self) -> str | None:
        if self._pistas_restantes <= 0:
            return None
        self._pistas_restantes -= 1
        return self.oracion_correcta

    def get_pistas_restantes(self) -> int:
        return self._pistas_restantes


# =============================================================