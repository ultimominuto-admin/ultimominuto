from flask import Flask, request, redirect, url_for

app = Flask(__name__)

noticias = [
    {
        "titulo": "Última Hora: Novedades del mercado de fichajes de fútbol",
        "texto": "Entérate de las últimas transferencias, rumores y datos relevantes del fútbol internacional.",
        "fecha": "2026-08-29"
    }
]

@app.route('/')
def home():
    html_noticias = ""
    for n in noticias:
        html_noticias += f'''
        <article style="margin-bottom:20px; border-bottom:1px solid #ddd; padding-bottom:15px;">
            <h3 style="color:#1b1b1b; margin-bottom:5px;">{n["titulo"]}</h3>
            <p style="color:#555; font-size:14px;">Publicado: {n.get("fecha", "2026-08-29")}</p>
            <p style="color:#333; line-height:1.6;">{n["texto"]}</p>
        </article>
        '''

    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <title>Últimominuto | Noticias de Fútbol y Deportes de Última Hora</title>
        <meta name="description" content="Portal de noticias de fútbol en vivo, resultados, fichajes e información deportiva al instante en Últimominuto.">
        <meta name="keywords" content="noticias de fútbol, deportes ultima hora, fichajes, resultados futbol, ultimominuto">
        <meta name="robots" content="index, follow">

        <meta property="og:title" content="Últimominuto - Noticias de Fútbol al Instante">
        <meta property="og:description" content="Toda la actualidad deportiva y el mercado de fichajes en un solo lugar.">
        <meta property="og:type" content="website">

        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px; }}
            header {{ background-color: #1b1b1b; color: white; padding: 20px; text-align: center; border-radius: 8px; }}
            h1 {{ margin: 0; color: #e50914; font-size: 28px; }}
            .content {{ margin-top: 20px; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            a.admin-btn {{ display: inline-block; margin-top: 15px; color: white; background-color: #e50914; padding: 10px 15px; border-radius: 5px; text-decoration: none; font-weight: bold; }}
        </style>
    </head>
    <body>
        <header>
            <h1>ÚLTIMOMINUTO</h1>
            <p>Noticias de fútbol e información deportiva en tiempo real</p>
        </header>
        <main class="content">
            <h2>Noticias Destacadas de Hoy</h2>
            {html_noticias}
            <a class="admin-btn" href="/admin">+ Publicar Nueva Noticia</a>
        </main>
    </body>
    </html>
    '''

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')
        if titulo and texto:
            noticias.insert(0, {"titulo": titulo, "texto": texto, "fecha": "2026-08-29"})
        return redirect(url_for('home'))

    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Panel de Control | Últimominuto</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f4; }
            form { background: white; padding: 20px; border-radius: 8px; max-width: 500px; margin: auto; }
            input, textarea { width: 100%; margin-bottom: 12px; padding: 10px; box-sizing: border-box; }
            button { background: #e50914; color: white; border: none; padding: 12px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; }
        </style>
    </head>
    <body>
        <form method="POST">
            <h2>Publicar Noticia SEO</h2>
            <label>Título Informativo:</label>
            <input type="text" name="titulo" placeholder="Ej: Fichaje confirmado en el Real Madrid" required>
            <label>Contenido de la noticia:</label>
            <textarea name="texto" rows="5" placeholder="Escribe la noticia..." required></textarea>
            <button type="submit">Publicar Noticia</button>
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
