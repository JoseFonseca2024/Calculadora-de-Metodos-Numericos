import io
import numpy as np
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.styles import Font

def exportar_excel_bytes(df, f, iteraciones):
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Newton_Raphson"

    # 1. TABLA DE DATOS PRINCIPAL
    headers = ['i', 'Ci', 'f(Ci)', "f'(Ci)", 'Ci+1', 'Error%']
    ws.append(headers)
    for row in df.itertuples(index=False):
        ws.append(list(row))

    # 2. DATOS PARA LA CURVA f(x)
    ws['H1'], ws['I1'] = "x_curva", "f(x)"
    xs_puntos = [it["Ci"] for it in iteraciones] + [it["Ci+1"] for it in iteraciones]
    xmin_map, xmax_map = min(xs_puntos), max(xs_puntos)

    x_vals = np.linspace(xmin_map - 1.5, xmax_map + 1.5, 100)
    for idx, x in enumerate(x_vals, 2):
        ws.cell(row=idx, column=8, value=float(x))
        try:
            y_val = f(x)
            ws.cell(row=idx, column=9, value=float(y_val) if np.isfinite(y_val) else None)
        except:
            ws.cell(row=idx, column=9, value=None)
    last_row_f = len(x_vals) + 1

    # 3. DATOS DE TANGENTES
    ws['K1'], ws['L1'] = "x_tang", "y_tang"
    row_t = 2
    for it in iteraciones:
        ws.cell(row=row_t, column=11, value=it["Ci"])
        ws.cell(row=row_t, column=12, value=it["f(Ci)"])
        ws.cell(row=row_t+1, column=11, value=it["Ci+1"])
        ws.cell(row=row_t+1, column=12, value=0)
        row_t += 3

    # 4. CONFIGURACIÓN DEL GRÁFICO
    chart = ScatterChart()
    chart.title = "Análisis Geométrico: Newton-Raphson"
    chart.x_axis.title = "x"
    chart.y_axis.title = "f(x)"
    chart.legend.position = 'b'

    # --- REMARCAR EJES X e Y (Asignación manual segura) ---
    def aplicar_formato_eje(eje):
        linea = LineProperties()
        linea.solidFill = "000000"
        linea.w = 20000
        props = GraphicalProperties()
        props.line = linea
        eje.graphicalProperties = props

    aplicar_formato_eje(chart.x_axis)
    aplicar_formato_eje(chart.y_axis)

    # SERIE 1: Curva f(x) - AZUL
    x_f_ref = Reference(ws, min_col=8, min_row=2, max_row=last_row_f)
    y_f_ref = Reference(ws, min_col=9, min_row=2, max_row=last_row_f)
    s_curva = Series(y_f_ref, x_f_ref, title="f(x)")
    
    linea_azul = LineProperties()
    linea_azul.solidFill = "0000FF"
    linea_azul.w = 25000
    props_azul = GraphicalProperties()
    props_azul.line = linea_azul
    s_curva.graphicalProperties = props_azul
    chart.series.append(s_curva)

    # SERIE 2: Tangentes - NARANJA PUNTEADO
    x_t_ref = Reference(ws, min_col=11, min_row=2, max_row=row_t-1)
    y_t_ref = Reference(ws, min_col=12, min_row=2, max_row=row_t-1)
    s_tang = Series(y_t_ref, x_t_ref, title="Tangentes (Pasos)")
    
    linea_naranja = LineProperties()
    linea_naranja.solidFill = "FF8C00"
    linea_naranja.dashStyle = "sysDash" # Aquí estaba el error anterior
    props_naranja = GraphicalProperties()
    props_naranja.line = linea_naranja
    s_tang.graphicalProperties = props_naranja
    chart.series.append(s_tang)

    # SERIE 3: Puntos de Iteración - ROJOS
    x_p_ref = Reference(ws, min_col=2, min_row=2, max_row=len(iteraciones)+1)
    y_p_ref = Reference(ws, min_col=3, min_row=2, max_row=len(iteraciones)+1)
    s_puntos = Series(y_p_ref, x_p_ref, title="Puntos (Ci)")
    
    s_puntos.marker.symbol = "circle"
    s_puntos.marker.size = 7
    props_rojo = GraphicalProperties()
    props_rojo.solidFill = "FF0000" 
    s_puntos.marker.graphicalProperties = props_rojo
    chart.series.append(s_puntos)

    # 5. ESCALA Y ZOOM
    chart.x_axis.scaling.min = xmin_map - 0.5
    chart.x_axis.scaling.max = xmax_map + 0.5
    f_vals = [abs(it["f(Ci)"]) for it in iteraciones]
    f_max = max(f_vals) if f_vals else 10
    chart.y_axis.scaling.min = -1
    chart.y_axis.scaling.max = f_max + 1

    ws.add_chart(chart, "H15")

    for cell in ws[1]:
        cell.font = Font(bold=True)

    wb.save(output)
    output.seek(0)
    return output.getvalue()