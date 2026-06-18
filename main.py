
from utils import DATA_DIR, USUARIOS_FILE, PROGRESS_FILE, save_json
from app import InglesGoApp

if __name__ == "__main__":
    # Crear archivos de datos si no existen
    DATA_DIR.mkdir(exist_ok=True)
    if not USUARIOS_FILE.exists():
        save_json(USUARIOS_FILE, [])
    if not PROGRESS_FILE.exists():
        save_json(PROGRESS_FILE, {})

    app = InglesGoApp()
    app.mainloop()