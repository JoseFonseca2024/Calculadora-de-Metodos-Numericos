import numpy as np

def ejecutar_muller(f, x0, x1, x2, tol):

    iteraciones = []

    i = 0
    max_iter = 100

    while i < max_iter:

        try:

            # =====================================================
            # EVALUACIONES
            # =====================================================

            f0 = float(f(x0))
            f1 = float(f(x1))
            f2 = float(f(x2))

            # =====================================================
            # DIFERENCIAS
            # =====================================================

            h1 = x1 - x0
            h2 = x2 - x1

            if abs(h1) < 1e-14 or abs(h2) < 1e-14:
                return (
                    False,
                    "División por cero en h1 o h2.",
                    None
                )

            d1 = (f1 - f0) / h1
            d2 = (f2 - f1) / h2

            # =====================================================
            # COEFICIENTES
            # =====================================================

            denominador_a = h1 + h2

            if abs(denominador_a) < 1e-14:
                return (
                    False,
                    "División por cero calculando 'a'.",
                    None
                )

            a = (d2 - d1) / denominador_a
            b = a * h2 + d2
            c = f2

            # =====================================================
            # DISCRIMINANTE
            # =====================================================

            discriminante = b**2 - 4*a*c

            # Corrección de ruido numérico
            if discriminante < 0 and abs(discriminante) < 1e-12:
                discriminante = 0.0

            # Si sigue siendo negativo -> detener
            if discriminante < 0:

                return (
                    False,
                    (
                        "El método generó un "
                        "discriminante negativo.\n\n"
                        "La iteración salió del dominio real."
                    ),
                    iteraciones
                )

            sqrt_disc = np.sqrt(discriminante)

            # =====================================================
            # DENOMINADORES
            # =====================================================

            den1 = b + sqrt_disc
            den2 = b - sqrt_disc

            # Evitar cancelación
            if abs(den1) > abs(den2):
                denominador = den1
                denominador_usado = "b + √Δ"
            else:
                denominador = den2
                denominador_usado = "b - √Δ"

            if abs(denominador) < 1e-14:
                return (
                    False,
                    "El denominador se volvió cero.",
                    iteraciones
                )

            # =====================================================
            # NUEVA APROXIMACIÓN
            # =====================================================

            dx = -2 * c / denominador

            x3 = x2 + dx

            # =====================================================
            # VALIDAR REAL
            # =====================================================

            if not np.isfinite(x3):

                return (
                    False,
                    "La iteración produjo un valor inválido.",
                    iteraciones
                )

            x3 = float(x3)

            # =====================================================
            # ERROR
            # =====================================================

            if abs(x3) < 1e-14:
                error = abs(dx) * 100
            else:
                error = abs(dx / x3) * 100

            # =====================================================
            # GUARDAR ITERACIÓN
            # =====================================================

            iteraciones.append({

                "i": i,

                "x0": float(x0),
                "x1": float(x1),
                "x2": float(x2),

                "f(x0)": float(f0),
                "f(x1)": float(f1),
                "f(x2)": float(f2),

                "h1": float(h1),
                "h2": float(h2),

                "d1": float(d1),
                "d2": float(d2),

                "a": float(a),
                "b": float(b),
                "c": float(c),

                "discriminante": float(discriminante),

                "den1": float(den1),
                "den2": float(den2),

                "denominador_usado": denominador_usado,

                "x3": float(x3),

                "Error%": float(error)
            })

            # =====================================================
            # CRITERIO DE PARO
            # =====================================================

            if error < tol:
                break

            # =====================================================
            # ACTUALIZAR
            # =====================================================

            x0 = x1
            x1 = x2
            x2 = x3

            i += 1

        except ZeroDivisionError:

            return (
                False,
                "División por cero detectada.",
                iteraciones
            )

        except Exception as e:

            return (
                False,
                f"Error en el cálculo: {str(e)}",
                iteraciones
            )

    if i >= max_iter:

        return (
            False,
            "El método no converge en 100 iteraciones.",
            iteraciones
        )

    return True, "", iteraciones