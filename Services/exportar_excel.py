import io
import numpy as np
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.styles import Font

def _configurar_grafica_base(ws, f, iteraciones, xmin_offset=1.5):
    xs = [it["Ci"] for it in iteraciones] + [it["Ci+1"] for it in iteraciones]

    xmin, xmax = min(xs), max(xs)

    x_vals = np.linspace(xmin - xmin_offset, xmax + xmin_offset, 100)

    ws["H1"], ws["I1"] = "x_curva", "f(x)"

    for i, x in enumerate(x_vals, start=2):
        ws.cell(row=i, column=8, value=float(x))

        try:
            y = f(x)
            ws.cell(row=i, column=9, value=float(y) if np.isfinite(y) else None)
        except (ValueError, TypeError, ZeroDivisionError):
            ws.cell(row=i, column=9, value=None)

    return len(x_vals) + 1, xmin, xmax

def _crear_chart_base(xmin, xmax):
    chart = ScatterChart()
    chart.x_axis.title = "x"
    chart.y_axis.title = "f(x)"
    chart.legend.position = "b"

    # Estilo ejes
    def style_axis(axis):
        line = LineProperties()
        line.solidFill = "000000"
        line.w = 20000
        gp = GraphicalProperties()
        gp.line = line
        axis.graphicalProperties = gp

    style_axis(chart.x_axis)
    style_axis(chart.y_axis)

    chart.x_axis.scaling.min = xmin - 0.5
    chart.x_axis.scaling.max = xmax + 0.5

    return chart

def exportar_excel_newton(df, f, iteraciones):
    output = io.BytesIO()

    wb = Workbook()
    ws = wb.active
    ws.title = "Newton"

    #Tabla
    headers = ['i', 'Ci', 'f(Ci)', "f'(Ci)", 'Ci+1', 'Error%']
    ws.append(headers)

    for row in df.itertuples(index=False):
        ws.append(list(row))

    #Curva de la función
    last_row, xmin, xmax = _configurar_grafica_base(ws, f, iteraciones)

    #Tangentes
    ws["K1"], ws["L1"] = "x_tang", "y_tang"

    row = 2
    for it in iteraciones:
        ws.cell(row=row, column=11, value=it["Ci"])
        ws.cell(row=row, column=12, value=it["f(Ci)"])

        ws.cell(row=row + 1, column=11, value=it["Ci+1"])
        ws.cell(row=row + 1, column=12, value=0)

        row += 3

    #Grafico
    chart = _crear_chart_base(xmin, xmax)
    chart.title = "Método Newton-Raphson"

    # f(x)
    x_ref = Reference(ws, min_col=8, min_row=2, max_row=last_row)
    y_ref = Reference(ws, min_col=9, min_row=2, max_row=last_row)
    serie = Series(y_ref, x_ref, title="f(x)")
    chart.series.append(serie)

    # tangentes
    x_t = Reference(ws, min_col=11, min_row=2, max_row=row - 1)
    y_t = Reference(ws, min_col=12, min_row=2, max_row=row - 1)
    serie_t = Series(y_t, x_t, title="Tangentes")
    chart.series.append(serie_t)

    ws.add_chart(chart, "H15")

    for cell in ws[1]:
        cell.font = Font(bold=True)

    wb.save(output)
    output.seek(0)
    return output.getvalue()

def exportar_excel_secante(df, f, iteraciones):
    output = io.BytesIO()

    wb = Workbook()
    ws = wb.active
    ws.title = "Secante"

    #Tabla
    headers = ['i', 'Ci-1', 'Ci', 'f(Ci-1)', 'f(Ci)', 'Ci+1', 'Error%']
    ws.append(headers)

    for row in df.itertuples(index=False):
        ws.append(list(row))

    #Curva
    last_row, xmin, xmax = _configurar_grafica_base(ws, f, iteraciones)

    #Secantes
    ws["K1"], ws["L1"] = "x_sec", "y_sec"

    row = 2
    for it in iteraciones:
        ws.cell(row=row, column=11, value=it["Ci-1"])
        ws.cell(row=row, column=12, value=it["f(Ci-1)"])

        ws.cell(row=row + 1, column=11, value=it["Ci"])
        ws.cell(row=row + 1, column=12, value=it["f(Ci)"])

        ws.cell(row=row + 2, column=11, value=it["Ci+1"])
        ws.cell(row=row + 2, column=12, value=0)

        row += 4

    #Grafico
    chart = _crear_chart_base(xmin, xmax)
    chart.title = "Método de la Secante"

    # f(x)
    x_ref = Reference(ws, min_col=8, min_row=2, max_row=last_row)
    y_ref = Reference(ws, min_col=9, min_row=2, max_row=last_row)
    serie = Series(y_ref, x_ref, title="f(x)")
    chart.series.append(serie)

    # secantes
    x_s = Reference(ws, min_col=11, min_row=2, max_row=row - 1)
    y_s = Reference(ws, min_col=12, min_row=2, max_row=row - 1)
    serie_s = Series(y_s, x_s, title="Secantes")
    chart.series.append(serie_s)

    ws.add_chart(chart, "H15")

    for cell in ws[1]:
        cell.font = Font(bold=True)

    wb.save(output)
    output.seek(0)
    return output.getvalue()

def exportar_excel_biseccion(df, f, iteraciones):
    output = io.BytesIO()

    wb = Workbook()
    ws = wb.active
    ws.title = "Bisección"

    # 🔹 Tabla correcta
    headers = ['i', 'a', 'b', 'Ci', 'f(Ci)', 'Error%']
    ws.append(headers)

    for row in df.itertuples(index=False):
        ws.append(list(row))

    # 🔹 Curva
    last_row, xmin, xmax = _configurar_grafica_base(ws, f, iteraciones)

    # 🔹 Puntos medios (Ci)
    ws["K1"], ws["L1"] = "x_mid", "y_mid"

    row = 2
    for it in iteraciones:
        ws.cell(row=row, column=11, value=it["Ci"])
        ws.cell(row=row, column=12, value=it["f(Ci)"])
        row += 1

    # 🔹 Gráfico
    chart = _crear_chart_base(xmin, xmax)
    chart.title = "Método de Bisección"

    # f(x)
    x_ref = Reference(ws, min_col=8, min_row=2, max_row=last_row)
    y_ref = Reference(ws, min_col=9, min_row=2, max_row=last_row)
    serie = Series(y_ref, x_ref, title="f(x)")
    chart.series.append(serie)

    # puntos Ci
    x_c = Reference(ws, min_col=11, min_row=2, max_row=row - 1)
    y_c = Reference(ws, min_col=12, min_row=2, max_row=row - 1)
    serie_c = Series(y_c, x_c, title="Aproximaciones")
    chart.series.append(serie_c)

    ws.add_chart(chart, "H15")

    # 🔹 Encabezados en negrita
    for cell in ws[1]:
        cell.font = Font(bold=True)

    wb.save(output)
    output.seek(0)
    return output.getvalue()

def exportar_excel_regla_falsa(df, f, iteraciones):
    output = io.BytesIO()

    wb = Workbook()
    ws = wb.active
    ws.title = "Regla Falsa"

    # Tabla
    headers = ['i', 'a', 'b', 'Ci', 'f(Ci)', 'Error%']
    ws.append(headers)

    for row in df.itertuples(index=False):
        ws.append(list(row))

    # Curva (USANDO TU BASE)
    last_row, xmin, xmax = _configurar_grafica_base(ws, f, iteraciones)

    # Puntos Ci
    ws["K1"], ws["L1"] = "x_ci", "y_ci"

    row = 2
    for it in iteraciones:
        ws.cell(row=row, column=11, value=it["Ci"])
        ws.cell(row=row, column=12, value=it["f(Ci)"])
        row += 1

    # Gráfico 
    chart = _crear_chart_base(xmin, xmax)
    chart.title = "Método de la Regla Falsa"

    # f(x)
    x_ref = Reference(ws, min_col=8, min_row=2, max_row=last_row)
    y_ref = Reference(ws, min_col=9, min_row=2, max_row=last_row)
    chart.series.append(Series(y_ref, x_ref, title="f(x)"))

    # puntos
    x_ci = Reference(ws, min_col=11, min_row=2, max_row=row - 1)
    y_ci = Reference(ws, min_col=12, min_row=2, max_row=row - 1)
    chart.series.append(Series(y_ci, x_ci, title="Aproximaciones"))

    ws.add_chart(chart, "H15")

    for cell in ws[1]:
        cell.font = Font(bold=True)

    wb.save(output)
    output.seek(0)
    return output.getvalue()