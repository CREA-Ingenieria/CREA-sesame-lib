# crea_sesame_lib/gui/editor.py
import threading
import webview
import os
from .. import connection, movimiento, emotes


class API:
    """Methods exposed to Blockly's JavaScript via the pywebview bridge."""

    def conectar(self, mock=False):
        try:
            connection.conectar_robot(mock=mock)
            return {"ok": True, "mensaje": "¡Conectado al robot!"}
        except Exception as e:
            return {"ok": False, "mensaje": str(e)}

    def ejecutar_codigo(self, codigo: str):
        connection._reset_stop()

        # Allowed names in exec() scope.
        # __builtins__ must allow basic types so variable assignments work:
        #   x = 3          needs int
        #   x = 1.5        needs float
        #   x = "hola"    needs str
        #   for i in range(n)  needs range
        # Imports, file access, and eval are intentionally excluded.
        namespace = {
            "__builtins__": {
                "range":    range,
                "int":      int,
                "float":    float,
                "str":      str,
                "bool":     bool,
                "abs":      abs,
                "round":    round,
                "min":      min,
                "max":      max,
                "print":    print,
            },
            # Robot lib functions
            "mover_adelante":           movimiento.mover_adelante,
            "mover_atras":              movimiento.mover_atras,
            "girar_derecha":            movimiento.girar_derecha,
            "girar_izquierda":          movimiento.girar_izquierda,
            "mover":                    movimiento.mover,
            "girar_derecha_angulo":     movimiento.girar_derecha_angulo,
            "girar_izquierda_angulo":   movimiento.girar_izquierda_angulo,
            "hacer_emote":              emotes.hacer_emote,
            "detener":                  movimiento.detener,
        }

        def run():
            try:
                exec(codigo, namespace)
            except Exception as e:
                print(f"[ERROR] Error ejecutando código: {e}")

        threading.Thread(target=run, daemon=True).start()
        return {"ok": True}

    def detener(self):
        try:
            movimiento.detener()
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "mensaje": str(e)}

    def obtener_emotes(self):
        return emotes.AVAILABLE_EMOTES


def launch():
    api = API()
    html_path = os.path.join(os.path.dirname(__file__), "editor.html")

    window = webview.create_window(
        title="Editor de Sesame Bot",
        url=html_path,
        js_api=api,
        width=1280,
        height=780,
        resizable=True,
        min_size=(900, 600),
    )
    webview.start(debug=False)