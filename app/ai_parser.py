# app/ai_parser.py

from groq import Groq
import os
import json
import re

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse_invoice(text: str) -> dict:
    prompt = f"""
Extraé datos de la siguiente factura y devolvé SOLO un objeto JSON.
No expliques nada.
No uses comillas triples.
No pongas texto fuera del JSON.

Formato:

{{
  "razon_social": "",
  "cuit": "",
  "fecha": "",
  "tipo_factura": "",
  "items": [
    {{"descripcion": "", "cantidad": "", "precio_unitario": "", "total": ""}}
  ],
  "total_factura": ""
}}

Factura:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Respondé SOLO JSON válido. Nada más."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()

    # 🔍 Extraer el primer bloque JSON
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"La IA no devolvió JSON válido:\n{raw}")

    return json.loads(match.group())
