# crea_sesame_lib/gui/editor.py
import threading
import webview
import os
from .. import connection, movimiento, emotes


class API:
    """
    Métodos expuestos al JavaScript de Blockly.
    Cada método puede ser llamado desde el navegador con:
        window.pywebview.api.<nombre_metodo>(args)
    """

    # ── Conexión ────────────────────────────────────────────────

    def conectar(self, mock=False):
        """Conecta al robot. Si mock=True, corre sin hardware."""
        try:
            connection.conectar_robot(mock=mock)
            return {"ok": True, "mensaje": "¡Conectado al robot!"}
        except Exception as e:
            return {"ok": False, "mensaje": str(e)}

    # ── Ejecución ───────────────────────────────────────────────

    def ejecutar_codigo(self, codigo: str):
        """
        Recibe el código Python generado por Blockly y lo ejecuta
        en un hilo secundario para no bloquear la UI.
        """
        connection._reset_stop()

        # Namespace restringido: solo pueden llamar funciones de la lib
        namespace = {
            "__builtins__": {"range": range, "print": print, "int": int, "float": float, "str": str},         # sin acceso a builtins de Python
            "mover_adelante":  movimiento.mover_adelante,
            "mover_atras":     movimiento.mover_atras,
            "girar_derecha":   movimiento.girar_derecha,
            "girar_izquierda": movimiento.girar_izquierda,
            "mover":           movimiento.mover,
            "girar_derecha_angulo":  movimiento.girar_derecha_angulo,
            "girar_izquierda_angulo": movimiento.girar_izquierda_angulo,
            "hacer_emote":     emotes.hacer_emote,
            "detener":         movimiento.detener,
            "range":           range,    # necesario para loops for
            "print":           print,    # útil para debugging estudiantil
        }

        def run():
            try:
                exec(codigo, namespace)
            except Exception as e:
                print(f"[ERROR] Error ejecutando el código: {e}")

        threading.Thread(target=run, daemon=True).start()
        return {"ok": True}

    def detener(self):
        """Detiene el robot inmediatamente desde el botón de la UI."""
        try:
            movimiento.detener()
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "mensaje": str(e)}

    def obtener_emotes(self):
        """Devuelve la lista de emotes disponibles para poblar el bloque."""
        return emotes.AVAILABLE_EMOTES


def launch():
    """Punto de entrada — abre la ventana del editor."""
    api = API()
    html_path = os.path.join(os.path.dirname(__file__), "editor.html")

    window = webview.create_window(
        title="CREA Sesame — Editor de Bloques",
        url=html_path,
        js_api=api,
        width=1280,
        height=780,
        resizable=True,
        min_size=(900, 600),
    )
    webview.start(debug=False)