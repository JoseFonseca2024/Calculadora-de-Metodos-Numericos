import re

def normalizar_funcion(funcion_str):
    # Quitar espacios
    funcion_str = funcion_str.replace(" ", "")

    # Potencias unicode
    funcion_str = funcion_str.replace("²", "**2")
    funcion_str = funcion_str.replace("³", "**3")

    # π → pi
    funcion_str = funcion_str.replace("π", "pi")

    # Potencias ^
    funcion_str = funcion_str.replace("^", "**")

    # Multiplicaciones implícitas
    # Número (entero o decimal) + variable → 2.5x → 2.5*x
    funcion_str = re.sub(r'(\d+(\.\d+)?)([a-zA-Z])', r'\1*\3', funcion_str)
    # Variable + número → x2 → x*2
    funcion_str = re.sub(r'([a-zA-Z])(\d+(\.\d+)?)', r'\1*\2', funcion_str)
    # x(x+1) → x*(x+1)
    funcion_str = re.sub(r'([a-zA-Z])\(', r'\1*(', funcion_str)
    # (x+1)(x-2) → (x+1)*(x-2)
    funcion_str = re.sub(r'\)(\()', r')*(', funcion_str)

    # CONSTANTES e y pi
    # Número (entero o decimal) + e → 2.5e → 2.5*E
    funcion_str = re.sub(r'(\d+(\.\d+)?)e\b', r'\1*E', funcion_str)
    # Variable + e → xe → x*E
    funcion_str = re.sub(r'([a-zA-Z])e\b', r'\1*E', funcion_str)
    # e sola → E
    funcion_str = re.sub(r'\be\b', 'E', funcion_str)
    # Número + pi → 2.5pi → 2.5*pi
    funcion_str = re.sub(r'(\d+(\.\d+)?)pi\b', r'\1*pi', funcion_str)
    # Variable + pi → xpi → x*pi
    funcion_str = re.sub(r'([a-zA-Z])pi\b', r'\1*pi', funcion_str)

    # EXPONENCIALES e^x → exp(x)
    funcion_str = re.sub(r'E\*\*\((.*?)\)', r'exp(\1)', funcion_str)
    funcion_str = re.sub(r'E\*\*(\w+)', r'exp(\1)', funcion_str)

    return funcion_str