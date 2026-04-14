import io
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Font


# GENERADOR DE GRÁFICA (BASE PARA TODOS)
def generar_grafico(f, iteraciones, metodo="Método"):
    xs = [it["Ci"] for it in iteraciones if "Ci" in it]
    xs += [it["Ci+1"] for it in iteraciones if "Ci+1" in it]

    xmin, xmax = min(xs), max(xs)
    x = np.linspace(xmin - 2, xmax + 2, 400)

    y = []
    for val in x:
        try:
            y_val = f(val)
            y.append(y_val if np.isfinite(y_val) else None)
        except:
            y.append(None)

    plt.figure()

    # 🔥 ejes tipo plano cartesiano
    plt.axhline(0)
    plt.axvline(0)

    # 🔥 función
    plt.plot(x, y, label="f(x)")

    # 🔥 puntos Ci + etiquetas
    for i, it in enumerate(iteraciones):
        if "Ci" in it and "f(Ci)" in it:
            xi = it["Ci"]
            yi = it["f(Ci)"]

            plt.scatter(xi, yi)
            plt.text(xi, yi, f"C{i}", fontsize=8)

    # 🔥 raíz final
    ultima = iteraciones[-1]

    if "Ci+1" in ultima:
        raiz = ultima["Ci+1"]
    else:
        raiz = ultima["Ci"]

    try:
        y_raiz = f(raiz)
    except:
        y_raiz = 0

    # punto raíz destacado
    plt.scatter(raiz, y_raiz, marker='x', s=100)
    plt.text(raiz, y_raiz, f"Raíz ≈ {raiz:.4f}", fontsize=9)

    plt.title(metodo)
    plt.legend()
    plt.grid()

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)

    return img_bytes

#  NEWTON
def exportar_excel_newton(df, f, iteraciones):
    output = io.BytesIO()

    wb = Workbook()
    ws = wb.active
    ws.title = "Newton"

    headers = ['i', 'Ci', 'f(Ci)', "f'(Ci)", 'Ci+1', 'Error%']
    ws.append(headers)

    for row in df.itertuples(index=False):
        ws.append(list(row))

    img_bytes = generar_grafico(f, iteraciones, "Método Newton-Raphson")

    img = Image(img_bytes)
    ws.add_image(img, "H2")

    for cell in ws[1]:
        cell.font = Font(bold=True)

    wb.save(output)
    output.seek(0)
    return output.getvalue()


# SECANTE
def exportar_excel_secante(df, f, iteraciones):
    output = io.BytesIO()

    wb = Workbook()
    ws = wb.active
    ws.title = "Secante"

    headers = ['i', 'Ci-1', 'Ci', 'f(Ci-1)', 'f(Ci)', 'Ci+1', 'Error%']
    ws.append(headers)

    for row in df.itertuples(index=False):
        ws.append(list(row))

    img_bytes = generar_grafico(f, iteraciones, "Método de la Secante")

    img = Image(img_bytes)
    ws.add_image(img, "H2")

    for cell in ws[1]:
        cell.font = Font(bold=True)

    wb.save(output)
    output.seek(0)
    return output.getvalue()


# BISECCIÓN
def exportar_excel_biseccion(df, f, iteraciones):
    output = io.BytesIO()

    wb = Workbook()
    ws = wb.active
    ws.title = "Bisección"

    headers = ['i', 'a', 'b', 'Ci', 'f(Ci)', 'Error%']
    ws.append(headers)

    for row in df.itertuples(index=False):
        ws.append(list(row))

    img_bytes = generar_grafico(f, iteraciones, "Método de Bisección")

    img = Image(img_bytes)
    ws.add_image(img, "H2")

    for cell in ws[1]:
        cell.font = Font(bold=True)

    wb.save(output)
    output.seek(0)
    return output.getvalue()


# REGLA FALSA
def exportar_excel_regla_falsa(df, f, iteraciones):
    output = io.BytesIO()

    wb = Workbook()
    ws = wb.active
    ws.title = "Regla Falsa"

    headers = ['i', 'a', 'b', 'Ci', 'f(Ci)', 'Error%']
    ws.append(headers)

    for row in df.itertuples(index=False):
        ws.append(list(row))

    img_bytes = generar_grafico(f, iteraciones, "Método de la Regla Falsa")

    img = Image(img_bytes)
    ws.add_image(img, "H2")

    for cell in ws[1]:
        cell.font = Font(bold=True)

    wb.save(output)
    output.seek(0)
    return output.getvalue()

def exportar_excel_punto_fijo(resultados):

    output = io.BytesIO()

    wb = Workbook()

    wb.remove(wb.active)

    for i, item in enumerate(resultados):

        intervalo = item["intervalo"]
        g_name = item["g"]
        iteraciones = item["iteraciones"]

        ws = wb.create_sheet(title=f"{g_name}_R{i+1}")

        ws.append(["i", "Ci", "Ci+1", "Error%"])

        for it in iteraciones:
            ws.append([
                it["i"],
                it["Ci"],
                it["Ci+1"],
                it["Error%"]
            ])

        for cell in ws[1]:
            cell.font = Font(bold=True)

    wb.save(output)
    output.seek(0)

    return output.getvalue()