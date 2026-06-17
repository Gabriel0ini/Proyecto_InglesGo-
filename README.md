<<<<<<< HEAD
# Proyecto_InglesGo-
=======
# Aprendiendo Inglés con Flash Cards

Aplicación de escritorio para Taller de Programación.

## Tecnologías usadas
- Python
- Tkinter
- JSON como base de datos local
- Pillow para imágenes
- pyttsx3 para pronunciación por voz
- PyInstaller para generar EXE

## Cómo ejecutar

1. Instalar Python.
2. Abrir la carpeta del proyecto en VS Code.
3. Crear entorno virtual:

```bash
python -m venv venv
```

4. Activar entorno virtual en Windows:

```bash
venv\Scripts\activate
```

5. Instalar librerías:

```bash
pip install -r requirements.txt
```

6. Ejecutar:

```bash
python main.py
```

## Cómo cambiar los verbos

Editar el archivo:

```bash
data/verbs.json
```

Ejemplo:

```json
{
  "base": "eat",
  "past": "ate",
  "future": "will eat",
  "spanish": "comer",
  "object": "pizza",
  "image": "assets/images/eat.png",
  "audio": "assets/audio/eat.mp3"
}
```

## Cómo cambiar imágenes

Reemplazar las imágenes de:

```bash
assets/images/
```

Usar el mismo nombre del verbo, por ejemplo:

```bash
eat.png
run.png
sleep.png
```

## Cómo crear EXE

```bash
pyinstaller --onefile --windowed main.py
```

El ejecutable aparecerá en:

```bash
dist/main.exe
```

## Importante para la entrega

Las imágenes actuales son de ejemplo. Para la entrega final se recomienda reemplazarlas por imágenes reales de acciones.
>>>>>>> cbbb7ed (Subiendo app inicial)
