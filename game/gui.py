"""
Módulo que contiene la interfaz gráfica del juego del Ahorcado.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from game.hangman import Hangman
from game.word_manager import WordManager

class AhorcadoGUI:
    """Clase para la interfaz gráfica del juego del Ahorcado."""
    
    def __init__(self):
        """Inicializa la interfaz gráfica."""
        self.root = tk.Tk()
        self.root.title("Juego del Ahorcado")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        self.hangman = None
        self.current_category = None
        
        # Definir los dibujos del ahorcado para cada etapa
        self.hangman_images = [
            # 0: Sin errores
            """
            
            
            
            
            
            ____________
            """,
            
            # 1: Primer error
            """
            
            |
            |
            |
            |
            |____________
            """,
            
            # 2: Segundo error
            """
            _________
            |
            |
            |
            |
            |____________
            """,
            
            # 3: Tercer error
            """
            _________
            |        |
            |
            |
            |
            |____________
            """,
            
            # 4: Cuarto error
            """
            _________
            |        |
            |        O
            |
            |
            |____________
            """,
            
            # 5: Quinto error
            """
            _________
            |        |
            |        O
            |       /|\\
            |
            |____________
            """,
            
            # 6: Sexto error (perdió)
            """
            _________
            |        |
            |        O
            |       /|\\
            |       / \\
            |____________
            """
        ]
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura los elementos de la interfaz de usuario."""
        # Crear frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header con título y categoría
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="JUEGO DEL AHORCADO", font=("Arial", 18, "bold"))
        title_label.pack()
        
        self.category_label = tk.Label(header_frame, text="", font=("Arial", 14))
        self.category_label.pack()
        
        # Frame central con dibujo y palabra
        center_frame = tk.Frame(main_frame)
        center_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Dibujo del ahorcado (izquierda)
        hangman_frame = tk.Frame(center_frame, width=400, height=300, bd=2, relief=tk.RIDGE)
        hangman_frame.pack(side=tk.LEFT, padx=(0, 10))
        hangman_frame.pack_propagate(False)
        
        self.hangman_display = tk.Label(
            hangman_frame, 
            text=self.hangman_images[0], 
            font=("Courier", 14),
            justify=tk.LEFT
        )
        self.hangman_display.pack(expand=True)
        
        # Palabra y letras incorrectas (derecha)
        word_frame = tk.Frame(center_frame)
        word_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Mostrar la palabra con guiones
        word_label = tk.Label(word_frame, text="Palabra:", font=("Arial", 12))
        word_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.word_display = tk.Label(word_frame, text="", font=("Arial", 18, "bold"))
        self.word_display.pack(pady=(0, 20))
        
        # Mostrar letras incorrectas
        incorrect_label = tk.Label(word_frame, text="Letras incorrectas:", font=("Arial", 12))
        incorrect_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.incorrect_display = tk.Label(word_frame, text="", font=("Arial", 14))
        self.incorrect_display.pack(anchor=tk.W)
        
        # Teclado virtual
        keyboard_frame = tk.Frame(main_frame)
        keyboard_frame.pack(fill=tk.X, pady=(20, 10))
        
        # Primera fila: Q-P
        row1_frame = tk.Frame(keyboard_frame)
        row1_frame.pack(fill=tk.X)
        for letter in "QWERTYUIOP":
            btn = tk.Button(
                row1_frame, 
                text=letter, 
                width=4, 
                height=2, 
                font=("Arial", 10, "bold"),
                command=lambda l=letter: self._guess_letter(l)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            
        # Segunda fila: A-L
        row2_frame = tk.Frame(keyboard_frame)
        row2_frame.pack(fill=tk.X)
        for letter in "ASDFGHJKLÑ":
            btn = tk.Button(
                row2_frame, 
                text=letter, 
                width=4, 
                height=2, 
                font=("Arial", 10, "bold"),
                command=lambda l=letter: self._guess_letter(l)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            
        # Tercera fila: Z-M
        row3_frame = tk.Frame(keyboard_frame)
        row3_frame.pack(fill=tk.X)
        for letter in "ZXCVBNM":
            btn = tk.Button(
                row3_frame, 
                text=letter, 
                width=4, 
                height=2, 
                font=("Arial", 10, "bold"),
                command=lambda l=letter: self._guess_letter(l)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Guarda las referencias a los botones para poder deshabilitarlos
        self.letter_buttons = row1_frame.winfo_children() + row2_frame.winfo_children() + row3_frame.winfo_children()
        
        # Botones de acción
        action_frame = tk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Selector de categoría
        category_frame = tk.Frame(action_frame)
        category_frame.pack(side=tk.LEFT)
        
        category_label = tk.Label(category_frame, text="Categoría:", font=("Arial", 12))
        category_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.category_var = tk.StringVar()
        categories = ["Aleatorio"] + WordManager.get_categories()
        self.category_selector = ttk.Combobox(category_frame, textvariable=self.category_var, values=categories, state="readonly", width=15)
        self.category_selector.current(0)
        self.category_selector.pack(side=tk.LEFT)
        
        # Botones de Nuevo Juego y Salir
        btn_frame = tk.Frame(action_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        new_game_btn = tk.Button(btn_frame, text="Nuevo Juego", font=("Arial", 12), command=self._start_new_game)
        new_game_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(btn_frame, text="Salir", font=("Arial", 12), command=self.root.quit)
        exit_btn.pack(side=tk.LEFT, padx=5)
        
    def _start_new_game(self):
        """Inicia un nuevo juego."""
        # Obtener la categoría seleccionada (o None para aleatorio)
        selected_category = self.category_var.get()
        if selected_category == "Aleatorio":
            selected_category = None
            
        # Obtener una palabra aleatoria y su categoría
        word, category = WordManager.get_random_word(selected_category)
        
        # Actualizar la categoría mostrada
        self.current_category = category
        self.category_label.config(text=f"Categoría: {category.capitalize()}")
        
        # Crear nuevo juego
        self.hangman = Hangman(word)
        
        # Actualizar la interfaz
        self.word_display.config(text=self.hangman.get_word_display())
        self.incorrect_display.config(text="")
        self.hangman_display.config(text=self.hangman_images[0])
        
        # Habilitar todos los botones de letras
        for button in self.letter_buttons:
            button.config(state=tk.NORMAL)
    
    def _guess_letter(self, letter):
        """
        Procesa el intento de adivinar una letra.
        
        Args:
            letter (str): La letra que se intenta adivinar
        """
        if not self.hangman:
            messagebox.showinfo("Nuevo Juego", "Por favor, inicia un nuevo juego primero.")
            return
            
        # Deshabilitar el botón de la letra
        for button in self.letter_buttons:
            if button.cget("text") == letter:
                button.config(state=tk.DISABLED)
                break
                
        # Procesar la letra
        is_correct = self.hangman.guess(letter)
        
        # Actualizar la interfaz
        self.word_display.config(text=self.hangman.get_word_display())
        self.incorrect_display.config(text=" ".join(sorted(self.hangman.incorrect_letters)))
        
        # Actualizar el dibujo del ahorcado si la letra es incorrecta
        if not is_correct:
            stage = self.hangman.get_hangman_stage()
            self.hangman_display.config(text=self.hangman_images[stage])
        
        # Verificar si el juego ha terminado
        if self.hangman.game_over:
            if self.hangman.won:
                messagebox.showinfo("¡Felicidades!", f"¡Has ganado! La palabra era: {self.hangman.word}")
            else:
                messagebox.showinfo("Game Over", f"¡Has perdido! La palabra era: {self.hangman.word}")
    
    def run(self):
        """Inicia la aplicación."""
        # Iniciar el primer juego
        self._start_new_game()
        
        # Iniciar el bucle principal de la interfaz
        self.root.mainloop()