# CREA Sesame Lib

Librería de Python que provee una capa de abstracción sobre [`CREA-sesame-companion`](https://github.com/CREA-robotics/CREA-sesame-companion) para simplificar el control del robot Sesame. Permite a los estudiantes mover, girar y animar el robot con llamadas a funciones simples, sin necesidad de manejar la conexión ni las peticiones HTTP directamente.

Además incluye un **editor visual de bloques** (estilo Scratch) para estudiantes que prefieren programar sin escribir código.

---

## Estructura del proyecto

```
CREA-sesame-lib/
├── crea_sesame_lib/          # Paquete principal de la librería
│   ├── __init__.py
│   ├── connection.py         # Descubrimiento de IP y conexión al robot
│   ├── movimiento.py         # Funciones de movimiento (adelante, atrás, giros)
│   ├── emotes.py             # Funciones de animaciones del robot
│   └── gui/                  # Editor visual de bloques
│       ├── __init__.py
│       ├── editor.py         # Ventana pywebview y bridge Python ↔ JavaScript
│       ├── editor.html       # Canvas de Blockly con los bloques personalizados
│       └── blockly/          # Archivos de Blockly descargados localmente
│           ├── blockly_compressed.js
│           ├── blocks_compressed.js
│           └── python_compressed.js
├── examples/
│   └── basic_usage.py        # Ejemplo de uso de la librería por código
├── main.py                   # Punto de entrada del editor visual
├── download_blockly.py       # Script para descargar Blockly (ejecutar una sola vez)
├── pyproject.toml
└── README.md
```

---

## Requisitos previos

- Python 3.9 o superior
- Estar conectado a la red WiFi del robot Sesame antes de ejecutar cualquier programa
- Haber ejecutado `download_blockly.py` al menos una vez (solo necesario para el editor visual)

---

## Uso

### Opción A — Editor visual de bloques

Ideal para estudiantes que no tienen experiencia previa con Python.

**Paso 1 — Activar el entorno virtual**

```bash
# Windows
.venv\Scripts\activate
```

**Paso 2 — Ejecutar el editor**

```bash
python main.py
```

Se abrirá una ventana con el editor de bloques. Desde ahí puedes conectarte al robot (o activar el modo simulación), armar tu programa arrastrando bloques y presionar **Ejecutar**.

---

### Opción B — Uso por código Python

Ideal para estudiantes que quieren escribir sus propios programas.

**Paso 1 — Activar el entorno virtual**

```bash
# Windows
.venv\Scripts\activate
```

**Paso 2 — Escribir y ejecutar tu programa**

Crea un archivo `.py` e importa los módulos que necesites:

```python
from crea_sesame_lib import connection, movimiento, emotes

# Conectar al robot (detecta la IP automáticamente)
connection.conectar_robot()

# Mover el robot
movimiento.mover_adelante(2)       # Avanza 2 segundos
movimiento.girar_derecha(1)        # Gira a la derecha 1 segundo
movimiento.girar_derecha_angulo(90) # Gira 90 grados a la derecha

# Hacer un emote
emotes.hacer_emote("wave")

# Detener el robot en cualquier momento (o presiona ESPACIO)
movimiento.detener()
```

> **Tip:** presiona la tecla **ESPACIO** durante la ejecución para detener el robot inmediatamente.

---

## Instalación para desarrolladores

```bash
# Clonar ambos repositorios al mismo nivel
git clone https://github.com/CREA-robotics/CREA-sesame-companion
git clone https://github.com/CREA-robotics/CREA-sesame-lib

# Crear y activar el entorno virtual dentro de sesame-lib
cd CREA-sesame-lib
python -m venv .venv
.venv\Scripts\activate

# Instalar dependencias
pip install -e ../CREA-sesame-companion
pip install -e .

# Descargar Blockly (solo una vez, necesario para el editor visual)
python download_blockly.py
```
