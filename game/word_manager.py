"""
Módulo para gestionar las palabras y categorías del juego.
"""
import random
from resources.categories import CATEGORIES

class WordManager:
    """Clase para gestionar la selección de palabras."""
    
    @staticmethod
    def get_categories():
        """
        Obtiene las categorías disponibles.
        
        Returns:
            list: Lista de nombres de categorías
        """
        return list(CATEGORIES.keys())
    
    @staticmethod
    def get_random_word(category=None):
        """
        Obtiene una palabra aleatoria de la categoría especificada.
        Si no se especifica categoría, selecciona una aleatoria.
        
        Args:
            category (str, optional): Categoría de la que seleccionar la palabra
            
        Returns:
            tuple: (palabra_seleccionada, categoría_seleccionada)
        """
        if category is None or category not in CATEGORIES:
            category = random.choice(list(CATEGORIES.keys()))
            
        word = random.choice(CATEGORIES[category])
        return word, category