# app/exporter.py
from openpyxl import Workbook

def export_to_excel(data: dict, filename: str = "factura.xlsx"):
    wb = Workbook()

    # Hoja 1: Datos generales
    ws_info = wb.active
    ws_info.title = "Factura"

    ws_info.append(["Campo", "Valor"])
    ws_info.append(["Razón social", data.get("razon_social")])
    ws_info.append(["CUIT", data.get("cuit")])
    ws_info.append(["Fecha", data.get("fecha")])
    ws_info.append(["Tipo", data.get("tipo_factura")])
    ws_info.append(["Total", data.get("total_factura")])

    # Hoja 2: Ítems
    ws_items = wb.create_sheet(title="Items")
    ws_items.append(["Descripción", "Cantidad", "Precio unitario", "Total"])

    for item in data.get("items", []):
        ws_items.append([
            item.get("descripcion"),
            item.get("cantidad"),
            item.get("precio_unitario"),
            item.get("total"),
        ])

    wb.save(filename)
    return filename
