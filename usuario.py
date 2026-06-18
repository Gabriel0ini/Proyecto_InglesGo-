from utils import load_json, save_json, hash_password, USUARIOS_FILE

class Usuario:
    def __init__(self, data: dict):
        self.id       = data.get("id", 0)
        self.nombre   = data.get("nombre", "")
        self.email    = data.get("email", "")
        self._password= data.get("password", "")
        self.xp       = data.get("xp", 0)
        self.racha    = data.get("racha", 0)
        self.nivel    = data.get("nivel", 1)

    # ----------------------------------------------------------
    @staticmethod
    def iniciar_sesion(email: str, password: str) -> "Usuario | None":
        """Busca al usuario por email y verifica contraseña."""
        usuarios = load_json(USUARIOS_FILE, [])
        hashed = hash_password(password)
        for u in usuarios:
            if u["email"].lower() == email.lower() and u["password"] == hashed:
                return Usuario(u)
        return None

    # ----------------------------------------------------------
    @staticmethod
    def crear_cuenta(nombre: str, email: str, password: str) -> "tuple[bool, str]":
        """
        Registra un nuevo usuario.
        Retorna (True, mensaje) si OK, (False, error) si falla.
        """
        if not nombre or not email or not password:
            return False, "Todos los campos son obligatorios."
        if "@" not in email:
            return False, "El email no es válido."
        if len(password) < 4:
            return False, "La contraseña debe tener al menos 4 caracteres."

        usuarios = load_json(USUARIOS_FILE, [])

        for u in usuarios:
            if u["email"].lower() == email.lower():
                return False, "Ya existe una cuenta con ese email."

        nuevo_id = max((u["id"] for u in usuarios), default=0) + 1
        nuevo = {
            "id": nuevo_id,
            "nombre": nombre,
            "email": email,
            "password": hash_password(password),
            "xp": 0,
            "racha": 0,
            "nivel": 1,
        }
        usuarios.append(nuevo)
        save_json(USUARIOS_FILE, usuarios)
        return True, "Cuenta creada correctamente."

    # ----------------------------------------------------------
    def agregar_xp(self, cantidad: int):
        self.xp += cantidad
        self._guardar()

    def _guardar(self):
        usuarios = load_json(USUARIOS_FILE, [])
        for i, u in enumerate(usuarios):
            if u["id"] == self.id:
                usuarios[i]["xp"]    = self.xp
                usuarios[i]["racha"] = self.racha
                usuarios[i]["nivel"] = self.nivel
                break
        save_json(USUARIOS_FILE, usuarios)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "password": self._password,
            "xp": self.xp,
            "racha": self.racha,
            "nivel": self.nivel,
        }

