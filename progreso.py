from utils import load_json, save_json, PROGRESS_FILE
from palabra import Palabra

class Progreso:
    def __init__(self, usuario_id: int):
        self.usuario_id = usuario_id
        datos = load_json(PROGRESS_FILE, {})
        uid   = str(usuario_id)
        self._data = datos.get(uid, {
            "puntaje": 0,
            "ejercicios_completados": 0,
            "verbos": {}
        })

    # ----------------------------------------------------------
    def actualizar_progreso(self, palabra: Palabra, correcto: bool):
        base = palabra.infinitivo
        if base not in self._data["verbos"]:
            self._data["verbos"][base] = {"correcto": 0, "incorrecto": 0, "dominado": False}

        if correcto:
            self._data["puntaje"]                       += 10
            self._data["ejercicios_completados"]        += 1
            self._data["verbos"][base]["correcto"]      += 1
        else:
            self._data["verbos"][base]["incorrecto"]    += 1

        if self._data["verbos"][base]["correcto"] >= 3:
            self._data["verbos"][base]["dominado"] = True

        self._guardar()

    # ----------------------------------------------------------
    def calcular_porcentaje(self, total_palabras: int) -> float:
        if total_palabras == 0:
            return 0.0
        dominados = sum(
            1 for v in self._data["verbos"].values() if v.get("dominado")
        )
        return round((dominados / total_palabras) * 100, 1)

    # ----------------------------------------------------------
    def esta_dominado(self, infinitivo: str) -> bool:
        return self._data["verbos"].get(infinitivo, {}).get("dominado", False)

    def get_puntaje(self) -> int:
        return self._data.get("puntaje", 0)

    def get_ejercicios_completados(self) -> int:
        return self._data.get("ejercicios_completados", 0)

    def get_verbos_debiles(self) -> list[str]:
        return [
            base for base, info in self._data["verbos"].items()
            if not info.get("dominado")
        ]

    def _guardar(self):
        datos = load_json(PROGRESS_FILE, {})
        datos[str(self.usuario_id)] = self._data
        save_json(PROGRESS_FILE, datos)

    def reiniciar(self):
        self._data = {"puntaje": 0, "ejercicios_completados": 0, "verbos": {}}
        self._guardar()

