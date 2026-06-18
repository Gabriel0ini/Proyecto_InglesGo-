from utils import load_json, VERBS_FILE
from palabra import Palabra

class Leccion:
    def __init__(self, id: int, titulo: str, unidad: int, descripcion: str, palabras: list[Palabra]):
        self.id          = id
        self.titulo      = titulo
        self.unidad      = unidad
        self.descripcion = descripcion
        self._palabras   = palabras

    # ----------------------------------------------------------
    def obtener_palabras(self) -> list[Palabra]:
        return self._palabras

    # ----------------------------------------------------------
    @staticmethod
    def cargar_lecciones(verbs_data: list[dict]) -> list["Leccion"]:
        """
        Construye lecciones agrupando los verbos por campo 'unidad'.
        Si los verbos no tienen campo 'unidad', todos van a la Unidad 1.
        """
        grupos: dict[int, list[Palabra]] = {}
        for v in verbs_data:
            p = Palabra(v)
            u = p.unidad
            grupos.setdefault(u, []).append(p)

        meta = {
            1: ("Los verbos",  "Aprende verbos en presente, pasado y futuro"),
            2: ("Saludos",     "Aprende a decir Hello, Goodbye y más"),
            3: ("Colores",     "Identifica los colores en inglés"),
            4: ("Acciones",    "Verbos de acción cotidiana"),
        }

        lecciones = []
        for unidad_num, palabras in sorted(grupos.items()):
            titulo, desc = meta.get(unidad_num, (f"Unidad {unidad_num}", ""))
            lecciones.append(Leccion(
                id=unidad_num,
                titulo=titulo,
                unidad=unidad_num,
                descripcion=desc,
                palabras=palabras
            ))
        return lecciones
