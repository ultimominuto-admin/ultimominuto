from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configurar Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

noticias = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        texto_original = data.get('contenido', '')
        
        if texto_original:
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(f"Reescribe esta noticia para un portal deportivo, hazla atractiva y concisa: {texto_original}")
                noticias.insert(0, response.text)
            except Exception as e:
                noticias.insert(0, texto_original)
                
        return jsonify({"status": "ok"}), 200
        
    return render_template('index.html', noticias=noticias)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
