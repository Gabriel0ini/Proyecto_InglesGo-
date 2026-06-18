import json
import hashlib
from pathlib import Path

# =============================================================
# RUTAS DEL PROYECTO
# =============================================================

BASE_DIR      = Path(__file__).parent
DATA_DIR      = BASE_DIR / "data"
USUARIOS_FILE = DATA_DIR / "usuarios.json"
VERBS_FILE    = DATA_DIR / "verbs.json"
PROGRESS_FILE = DATA_DIR / "progress.json"

# =============================================================
# PALETA DE COLORES
# =============================================================

BG        = "#F2F7FF"
PRIMARY   = "#3366FF"
SECONDARY = "#FFB703"
SUCCESS   = "#2A9D8F"
DANGER    = "#E63946"
TEXT      = "#1D3557"
GRAY      = "#6c757d"

# =============================================================
# FUNCIONES UTILITARIAS
# =============================================================

def load_json(path, default):
    """Carga un archivo JSON. Si no existe o falla, retorna el valor por defecto."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    """Guarda datos en un archivo JSON con formato legible."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def hash_password(password: str) -> str:
    """Hashea una contraseña con SHA-256. Las contraseñas nunca se guardan en texto plano."""
    return hashlib.sha256(password.encode()).hexdigest()