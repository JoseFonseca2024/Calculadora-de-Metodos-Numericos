import numpy as np

def ejecutar_muller(f, x0, x1, x2, tol):
    iteraciones = []
    i = 0
    max_iter = 100

    while i < max_iter:
        try:
            f0, f1, f2 = f(x0), f(x1), f(x2)
            
            h1 = x1 - x0
            h2 = x2 - x1
            d1 = (f1 - f0) / h1
            d2 = (f2 - f1) / h2
            
            # Coeficientes de la parábola: a(x-x2)^2 + b(x-x2) + c
            a = (d2 - d1) / (h2 + h1)
            b = a * h2 + d2
            c = f2
            
            # El discriminante (usamos 0j para permitir complejos si es necesario)
            discriminante = np.sqrt(b**2 - 4*a*c + 0j)
            
            # Elegimos el denominador más grande para mayor estabilidad numérica
            den1 = b + discriminante
            den2 = b - discriminante
            denominador = den1 if abs(den1) > abs(den2) else den2
            
            dx = -2 * c / denominador
            x3 = x2 + dx
            
            # Error relativo porcentual
            if abs(x3) < 1e-12:
                error = 0
            else:
                error = abs(dx / x3) * 100
            
            iteraciones.append({
                "i": i,
                "x0": x0, "x1": x1, "x2": x2,
                "f(x0)": f0, "f(x1)": f1, "f(x2)": f2,
                "a": a, "b": b, "c": c,
                "x3": x3.real if abs(x3.imag) < 1e-10 else x3,
                "Error%": float(abs(error))
            })

            if abs(error) < tol:
                break
                
            # Actualización para la siguiente iteración
            x0, x1, x2 = x1, x2, (x3.real if abs(x3.imag) < 1e-10 else x3)
            i += 1
            
            if i >= max_iter:
                return False, "El método no converge en 100 iteraciones.", None

        except ZeroDivisionError:
            return False, "División por cero detectada en los coeficientes.", None
        except Exception as e:
            return False, f"Error en el cálculo: {str(e)}", None
        
    return True, "", iteraciones