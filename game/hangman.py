"""
Módulo que contiene la lógica principal del juego del Ahorcado.
"""

class Hangman:
    """Clase que maneja la lógica del juego del ahorcado."""
    
    def __init__(self, word):
        """
        Inicializa un nuevo juego del ahorcado.
        
        Args:
            word (str): La palabra a adivinar
        """
        self.word = word.upper()
        self.guessed_letters = set()
        self.incorrect_letters = set()
        self.max_attempts = 6
        self.attempts_left = self.max_attempts
        self.game_over = False
        self.won = False
    
    def guess(self, letter):
        """
        Procesa un intento de adivinar una letra.
        
        Args:
            letter (str): La letra que se intenta adivinar
            
        Returns:
            bool: True si la letra está en la palabra, False si no
        """
        if self.game_over:
            return False
            
        letter = letter.upper()
        
        # Si la letra ya fue intentada, no hacer nada
        if letter in self.guessed_letters or letter in self.incorrect_letters:
            return letter in self.guessed_letters
            
        # Comprobar si la letra está en la palabra
        if letter in self.word:
            self.guessed_letters.add(letter)
            
            # Verificar si ha ganado
            if all(letter in self.guessed_letters for letter in self.word if letter.isalpha()):
                self.game_over = True
                self.won = True
                
            return True
        else:
            self.incorrect_letters.add(letter)
            self.attempts_left -= 1
            
            # Verificar si ha perdido
            if self.attempts_left <= 0:
                self.game_over = True
                
            return False
    
    def get_word_display(self):
        """
        Obtiene la representación actual de la palabra con guiones bajos para letras no adivinadas.
        
        Returns:
            str: La palabra con guiones para letras no adivinadas
        """
        display = []
        for letter in self.word:
            if letter.isalpha():
                if letter in self.guessed_letters:
                    display.append(letter)
                else:
                    display.append("_")
            else:
                display.append(letter)  # Mantener espacios u otros caracteres
                
        return " ".join(display)
    
    def get_hangman_stage(self):
        """
        Obtiene el índice de la etapa actual del ahorcado.
        
        Returns:
            int: Índice de la etapa (0-6)
        """
        return self.max_attempts - self.attempts_left