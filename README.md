# Invoice AI Processor

Aplicación web que permite subir facturas en PDF o imagen, extraer el texto con OCR y usar IA para convertirlas en datos estructurados, exportándolos automáticamente a Excel.

Proyecto desarrollado con **Python, FastAPI, OCR e integración con modelos de IA vía API**.

---

## 🚀 Funcionalidades

- Subida de facturas en PDF o JPG
- Extracción de texto con OCR
- Procesamiento con IA para detectar:
  - Razón social
  - CUIT
  - Fecha
  - Tipo de factura
  - Precios unitarios
  - Precio total
- Exportación automática a Excel (.xlsx)
- Interfaz web simple con HTML + Bootstrap

---

## 🛠️ Tecnologías

- Python 3
- FastAPI
- Jinja2
- Tesseract OCR
- Groq API (LLaMA)
- OpenPyXL
- HTML + Bootstrap

---

## 📂 Estructura del proyecto

```text
invoice_ai_processor/
│
├── app/
│   ├── main.py        # Servidor FastAPI
│   ├── ocr.py         # OCR (PDF/JPG → texto)
│   ├── ai_parser.py  # Llamada a IA
│   └── exporter.py   # Exportación a Excel
│
├── templates/
│   └── index.html
│
├── static/
│   └── styles.css
│
├── uploads/           # Archivos temporales (ignorado en git)
├── venv/              # Entorno virtual (ignorado en git)
├── .gitignore
└── README.md
