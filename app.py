import os
import time
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Configuración de la IA Gemini con tu API Key de Render
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

noticias = []

@app.route('/', methods=['POST'])
def recibir_noticia():
    data = request.get_json(silent=True) or {}
    contenido = data.get('contenido')

    if not contenido:
        return jsonify({"error": "No se recibió contenido"}), 400

    try:
        # La IA reescribe la noticia
        prompt = f'Reescribe el siguiente titular de noticia para que sea llamativo y original, manteniendo el significado y en español: "{contenido}"'
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        titulo_reescrito = response.text.strip()

        nueva_noticia = {
            "id": int(time.time()),
            "original": contenido,
            "ia": titulo_reescrito,
            "fecha": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        noticias.insert(0, nueva_noticia)
        print("Noticia procesada:", nueva_noticia)

        return jsonify({"status": "éxito", "noticia": nueva_noticia}), 200

    except Exception as e:
        print("Error con Gemini:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def ver_noticias():
    html = "<h1>Último Minuto - Noticias con IA</h1><ul>"
    for n in noticias:
        html += f"<li><strong>[{n['fecha']}]</strong> {n['ia']}<br><small>Original: {n['original']}</small></li><br>"
    html += "</ul>"
    return html

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
