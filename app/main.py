from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.ocr import extract_text
from app.ai_parser import parse_invoice
from app.exporter import export_to_excel
from fastapi.responses import FileResponse
import uuid
import shutil
import os


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload/")
async def upload_invoice(file: UploadFile = File(...)):
    # 1. Guardar archivo
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Extraer texto
    text = extract_text(file_path)

    # 3. Llamar a la IA
    data = parse_invoice(text)

    # 4. Exportar a Excel
    filename = f"factura_{uuid.uuid4().hex}.xlsx"
    export_to_excel(data, filename)

    # 5. Devolver archivo
    return FileResponse(
        path=filename,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

