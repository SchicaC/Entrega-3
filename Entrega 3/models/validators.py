import re

def validate_numeric_input(char):
    """Valida que solo se ingresen números"""
    return char.isdigit() or char == ""

def validate_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_text_length(text, min_len=1, max_len=100):
    """Valida longitud del texto"""
    return min_len <= len(text) <= max_len

def validate_special_chars(text):
    """Valida que no contenga caracteres especiales peligrosos"""
    dangerous_chars = [';', '--', '/*', '*/', '@@', 'char', 'nchar', 'varchar']
    return not any(char in text.lower() for char in dangerous_chars)