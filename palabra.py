from utils import load_json, save_json

class Palabra:
    def __init__(self, data: dict):
        self.id          = data.get("id", 0)
        self.infinitivo  = data.get("base", "")
        self.presente    = data.get("present", data.get("base", ""))
        self.pasado      = data.get("past", "")
        self.futuro      = data.get("future", "")
        self.traduccion  = data.get("spanish", "")
        self.imagen_url  = data.get("image", "")
        self.audio_url   = data.get("audio", "")
        self.objeto      = data.get("object", "something")
        self.unidad      = data.get("unidad", 1)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "base": self.infinitivo,
            "present": self.presente,
            "past": self.pasado,
            "future": self.futuro,
            "spanish": self.traduccion,
            "image": self.imagen_url,
            "audio": self.audio_url,
            "object": self.objeto,
            "unidad": self.unidad,
        }
