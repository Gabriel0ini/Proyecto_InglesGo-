from utils import load_json, save_json

# Sujetos disponibles para armar oraciones, en orden de presentación.
SUJETOS = ["I", "You", "He", "She", "It", "We", "They"]


class Palabra:
    def __init__(self, data: dict):
        self.id          = data.get("id", 0)
        self.infinitivo  = data.get("base", "")
        self.traduccion  = data.get("spanish", "")
        self.imagen_url  = data.get("image", "")
        self.audio_url   = data.get("audio", "")
        self.unidad      = data.get("unidad", 1)

        # Nueva estructura: una fila completa (sujeto + present/past/future)
        # por cada uno de los 7 sujetos. Ejemplo de fila:
        # {"subject": "I", "present": "play soccer in the park",
        #  "past": "played soccer in the park", "future": "will play soccer in the park"}
        self.oraciones: list[dict] = data.get("sentences", [])

        # Campos antiguos mantenidos por compatibilidad con otras pantallas
        # (flashcards, selección múltiple). Se derivan de la fila "I" si existe,
        # o si no, caen en los campos planos viejos (object/past/future).
        fila_i = next((f for f in self.oraciones if f.get("subject") == "I"), None)
        self.presente = data.get("present", self.infinitivo)
        self.pasado   = data.get("past", "")
        self.futuro   = data.get("future", "")
        self.objeto   = data.get("object", "something")
        if fila_i:
            self.pasado = fila_i.get("past", self.pasado)
            self.futuro = fila_i.get("future", self.futuro)

    # ----------------------------------------------------------
    def obtener_oracion(self, sujeto: str, tiempo: str) -> str:
        """
        Devuelve la oración completa (con sujeto) para un sujeto y tiempo dados.
        tiempo: "present" | "past" | "future"
        """
        fila = next((f for f in self.oraciones if f.get("subject") == sujeto), None)
        if not fila:
            return ""
        return f"{sujeto} {fila.get(tiempo, '')}".strip()

    def oraciones_por_tiempo(self, tiempo: str) -> list[str]:
        """Devuelve las 7 oraciones completas (con sujeto) para un tiempo dado."""
        return [
            f"{fila.get('subject')} {fila.get(tiempo, '')}".strip()
            for fila in self.oraciones
            if fila.get("subject")
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "base": self.infinitivo,
            "spanish": self.traduccion,
            "image": self.imagen_url,
            "audio": self.audio_url,
            "unidad": self.unidad,
            "sentences": self.oraciones,
        }