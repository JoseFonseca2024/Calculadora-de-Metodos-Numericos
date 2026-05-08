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

            # Coeficientes de la parábola
            a = (d2 - d1) / (h2 + h1)
            b = a * h2 + d2
            c = f2

            # Discriminante
            discriminante = np.sqrt(b**2 - 4*a*c + 0j)

            # Posibles denominadores
            den1 = b + discriminante
            den2 = b - discriminante

            abs_den1 = abs(den1)
            abs_den2 = abs(den2)

            # Selección del denominador de mayor magnitud
            if abs_den1 > abs_den2:
                denominador = den1
                denominador_usado = "b + √(b² - 4ac)"
            else:
                denominador = den2
                denominador_usado = "b - √(b² - 4ac)"

            # Nueva aproximación
            dx = -2 * c / denominador
            x3 = x2 + dx

            # Error relativo porcentual
            if abs(x3) < 1e-12:
                error = 0
            else:
                error = abs(dx / x3) * 100

            iteraciones.append({
                "i": i,

                "x0": x0,
                "x1": x1,
                "x2": x2,

                "f(x0)": f0,
                "f(x1)": f1,
                "f(x2)": f2,

                "h1": h1,
                "h2": h2,

                "d1": d1,
                "d2": d2,

                "a": a,
                "b": b,
                "c": c,

                "discriminante": discriminante,

                "den1": den1,
                "den2": den2,

                "denominador_usado": denominador_usado,

                "x3": x3.real if abs(x3.imag) < 1e-10 else x3,

                "Error%": float(abs(error))
            })

            # Criterio de paro
            if abs(error) < tol:
                break

            # Actualización de puntos
            x0 = x1
            x1 = x2
            x2 = x3.real if abs(x3.imag) < 1e-10 else x3

            i += 1

        except ZeroDivisionError:
            return False, "División por cero detectada.", None

        except Exception as e:
            return False, f"Error en el cálculo: {str(e)}", None

    if i >= max_iter:
        return False, "El método no converge en 100 iteraciones.", None

    return True, "", iteraciones