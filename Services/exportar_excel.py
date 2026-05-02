import io
import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

def procesar_fila_compleja(fila):
    """Procesa la fila para separar resultados y errores en columnas distintas."""
    nueva_fila = []
    for celda in fila:
        # Limpieza de Tuplas (Intervalos)
        if isinstance(celda, tuple):
            nueva_fila.append(f"[{celda[0]:.4f}, {celda[1]:.4f}]")
        
        # Limpieza de Listas (Iteraciones) -> Separar en 2 valores
        elif isinstance(celda, list) and len(celda) > 0 and isinstance(celda[-1], dict):
            ult = celda[-1]
            res = ult.get('raiz') or ult.get('Ci+1') or ult.get('x_nuevo') or 0
            err = ult.get('Error%') or ult.get('error') or 0
            nueva_fila.append(round(float(res), 6))
            nueva_fila.append(f"{err:.4e}")
            
        # Limpieza de Números
        elif isinstance(celda, (float, np.float64, np.float32)):
            nueva_fila.append(round(float(celda), 8))
        else:
            nueva_fila.append(celda)
    return nueva_fila

def exportar_excel_generico(df, f_num=None, metodo_nombre="Reporte", extra_data=None):
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = str(metodo_nombre)[:30]
    
    if isinstance(df, list):
        df = pd.DataFrame(df)

    # Estilos profesionales
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                         top=Side(style='thin'), bottom=Side(style='thin'))

    # Ajustar encabezados si hay iteraciones
    columnas_originales = df.columns.tolist()
    nuevos_encabezados = []
    for col in columnas_originales:
        if col.lower() == 'iteraciones':
            nuevos_encabezados.extend(['Resultado Final', 'Error Relativo'])
        else:
            nuevos_encabezados.append(col)
    ws.append(nuevos_encabezados)
    
    # Agregar datos procesados
    for _, fila in df.iterrows():
        ws.append(procesar_fila_compleja(fila))

    # Aplicar formato a toda la tabla
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if cell.row == 1:
                cell.fill = header_fill
                cell.font = header_font

    # Auto-ajuste de ancho
    for column in ws.columns:
        max_length = max(len(str(cell.value)) for cell in column)
        ws.column_dimensions[column[0].column_letter].width = max_length + 4

    wb.save(output)
    output.seek(0)
    return output.getvalue()

# --- MÉTODOS CERRADOS (Bisección y Regla Falsa) ---
# Se agregan valores por defecto (=None) para que no falten argumentos
def exportar_excel_biseccion(df, f_num=None, iteraciones=None):
    return exportar_excel_generico(df, f_num, "Biseccion")

def exportar_excel_regla_falsa(df, f_num=None, iteraciones=None):
    return exportar_excel_generico(df, f_num, "ReglaFalsa")

# --- MÉTODOS ABIERTOS ---
# Usamos *args o valores por defecto para atrapar lo que mande la vista
def exportar_excel_newton(df, f_num=None, f_der_num=None, x0=None):
    return exportar_excel_generico(df, f_num, "NewtonRaphson")

def exportar_excel_secante(df, f_num=None, x0=None, x1=None):
    return exportar_excel_generico(df, f_num, "Secante")

def exportar_excel_punto_fijo(df, f_num=None, g_num=None, x0=None):
    return exportar_excel_generico(df, f_num, "PuntoFijo")

# --- SERIE DE TAYLOR ---
def exportar_excel_taylor(df, f_num=None, poly_func=None, x_eval=None, a=None):
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "SerieDeTaylor"
    
    # Encabezados específicos
    ws.append(["REPORTE DE SERIE DE TAYLOR"])
    if a is not None: ws.append(["Punto de expansión (a):", a])
    if x_eval is not None: ws.append(["Valor a evaluar (x):", x_eval])
    ws.append([]) 
    
    if isinstance(df, list):
        df = pd.DataFrame(df)
        
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)
        
    wb.save(output)
    output.seek(0)
    return output.getvalue()    