from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Base de datos persistente en memoria mientras el servidor corre
noticias = []

@app.route('/')
def home():
    return render_template('index.html', noticias=reversed(noticias))

@app.route('/api/noticias', methods=['POST'])
def recibir_noticia():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "No se recibieron datos"}), 400

    nueva_noticia = {
        "titulo": data.get("titulo", "Sin título"),
        "meta_descripcion": data.get("meta_descripcion", ""),
        "cuerpo": data.get("cuerpo", ""),
        "imagen_url": data.get("imagen_url", ""),
        "categoria": data.get("categoria", "ÚLTIMA HORA"),
        "fecha": data.get("fecha", "Hace un momento"),
        "tags": data.get("tags", "Noticias, Actualidad")
    }

    noticias.append(nueva_noticia)
    return jsonify({"status": "success", "message": "Noticia publicada correctamente"}), 200

if __name__ == '__main__':
    app.run(debug=True)
