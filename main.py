from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.ocr import extract_text
from app.ai_parser import parse_invoice
from app.database import engine, SessionLocal
from app.models import Base, Invoice

import pandas as pd
import shutil
import os
import json

# ------------------ DB INIT ------------------

Base.metadata.create_all(bind=engine)

# ------------------ APP ------------------

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------------ HOME ------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ------------------ LISTAR FACTURAS ------------------

@app.get("/invoices/")
def get_invoices():
    db = SessionLocal()
    try:
        return db.query(Invoice).all()
    finally:
        db.close()

# ------------------ EXPORTAR TODO ------------------

@app.get("/export/")
def export_all():
    db = SessionLocal()
    try:
        invoices = db.query(Invoice).all()

        rows = []
        for inv in invoices:
            rows.append({
                "Proveedor": inv.supplier,
                "Fecha": inv.date,
                "Total": inv.total,
                "Items": inv.items
            })

        df = pd.DataFrame(rows)
        filename = "todas_las_facturas.xlsx"
        df.to_excel(filename, index=False)

        return FileResponse(
            filename,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    finally:
        db.close()

# ------------------ SUBIR FACTURA ------------------

@app.post("/upload/")
async def upload_invoice(file: UploadFile = File(...)):
    # Guardar archivo
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR
    text = extract_text(file_path)

    # IA
    data = parse_invoice(text)
    print("DATA IA >>>", data)

    # Normalizar total con coma
    raw_total = data.get("total_factura", "0") \
        .replace(".", "") \
        .replace(",", ".")

    db = SessionLocal()

    try:
        invoice = Invoice(
            supplier=data.get("razon_social"),
            date=data.get("fecha"),
            total=float(raw_total),
            items=json.dumps(data.get("items", []))
        )

        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        print("ID GUARDADO >>>", invoice.id)

        return {"message": "Factura guardada", "id": invoice.id}

    finally:
        db.close()

# ------------------ ELIMINAR FACTURA ------------------

@app.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: int):
    db = SessionLocal()
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

        if not invoice:
            return {"error": "Factura no encontrada"}

        db.delete(invoice)
        db.commit()

        return {"message": "Factura eliminada"}
    finally:
        db.close()
