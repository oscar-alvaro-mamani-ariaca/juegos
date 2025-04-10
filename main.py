"""
Punto de entrada principal para el juego del Ahorcado.
Este archivo inicia la aplicación.
"""
from game.gui import AhorcadoGUI

if __name__ == "__main__":
    app = AhorcadoGUI()
    app.run()