from flask import Flask, request, redirect, url_for

app = Flask(__name__)

MI_CONTRASEÑA = "admin123"

# Listas de datos en memoria
noticias = [
    {
        "titulo": "Última Hora: Novedades del mercado de fichajes de fútbol",
        "texto": "Entérate de las últimas transferencias, rumores y datos relevantes del fútbol internacional.",
        "fecha": "2026-08-29"
    }
]

usuarios_registrados = []

# Plantilla base del HTML para mantener un diseño uniforme
def render_pagina(titulo_pagina, contenido_principal):
    return f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titulo_pagina} | Últimominuto</title>
        <style>
            * {{ box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            body {{ background-color: #f4f6f9; margin: 0; padding: 0; }}
            
            /* Encabezado y Menú */
            header {{ background-color: #1b1b1b; color: white; padding: 20px; text-align: center; }}
            header h1 {{ margin: 0; color: #e50914; font-size: 32px; letter-spacing: 1px; }}
            header p {{ margin: 5px 0 0; color: #ccc; font-size: 14px; }}
            
            nav {{ background-color: #111; display: flex; justify-content: center; border-bottom: 3px solid #e50914; }}
            nav a {{ color: white; text-decoration: none; padding: 14px 20px; font-weight: bold; font-size: 15px; display: inline-block; transition: background 0.3s; }}
            nav a:hover {{ background-color: #e50914; }}
            
            /* Contenido */
            .container {{ max-width: 800px; margin: 25px auto; padding: 20px; }}
            .card {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; }}
            
            /* Formularios */
            label {{ font-weight: bold; display: block; margin-top: 10px; margin-bottom: 5px; color: #333; }}
            input, textarea {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; margin-bottom: 15px; }}
            button {{ background-color: #e50914; color: white; border: none; padding: 12px; border-radius: 4px; font-weight: bold; width: 100%; cursor: pointer; font-size: 16px; }}
            button:hover {{ background-color: #b80710; }}
        </style>
    </head>
    <body>
        <header>
            <h1>ÚLTIMOMINUTO</h1>
            <p>El portal líder en noticias de fútbol al instante</p>
        </header>
        
        <nav>
            <a href="/">Noticias</a>
            <a href="/nosotros">Sobre Nosotros</a>
            <a href="/registro">Registro</a>
        </nav>
        
        <div class="container">
            {contenido_principal}
        </div>
    </body>
    </html>
    '''

# 1. PORTADA: SECCIÓN DE NOTICIAS
@app.route('/')
def home():
    html_noticias = ""
    for n in noticias:
        html_noticias += f'''
        <article style="margin-bottom:20px; border-bottom:1px solid #eee; padding-bottom:15px;">
            <h3 style="color:#1b1b1b; margin-bottom:5px; font-size:20px;">{n["titulo"]}</h3>
            <span style="color:#888; font-size:12px;">Publicado: {n["fecha"]}</span>
            <p style="color:#444; line-height:1.6; margin-top:10px;">{n["texto"]}</p>
        </article>
        '''
    contenido = f'''
    <div class="card">
        <h2 style="color:#111; margin-top:0;">Noticias Destacadas</h2>
        {html_noticias}
    </div>
    '''
    return render_pagina("Noticias de Fútbol", contenido)

# 2. SECCIÓN SOBRE NOSOTROS
@app.route('/nosotros')
def nosotros():
    contenido = '''
    <div class="card">
        <h2 style="color:#111; margin-top:0;">Sobre Nosotros</h2>
        <p style="line-height:1.6; color:#444;">
            <strong>ÚLTIMOMINUTO</strong> es tu plataforma digital de referencia para seguir toda la actualidad del fútbol nacional e internacional en tiempo real.
        </p>
        <p style="line-height:1.6; color:#444;">
            Nos apasiona el deporte rey y nos dedicamos a llevar la información más veraz sobre fichajes, resultados de partidos, análisis y coberturas exclusivas directamente a tu pantalla.
        </p>
    </div>
    '''
    return render_pagina("Sobre Nosotros", contenido)

# 3. SECCIÓN DE REGISTRO DE USUARIOS
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    mensaje = ""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        if nombre and email:
            usuarios_registrados.append({"nombre": nombre, "email": email})
            mensaje = "<p style='color:green; font-weight:bold; text-align:center;'>¡Registro completado con éxito! Bienvenido a la comunidad.</p>"
            
    contenido = f'''
    <div class="card">
        <h2 style="color:#111; margin-top:0;">Registro de Usuarios</h2>
        <p style="color:#666;">Únete a nuestra comunidad para recibir alertas y contenido exclusivo.</p>
        {mensaje}
        <form method="POST">
            <label>Nombre Completo:</label>
            <input type="text" name="nombre" placeholder="Tu nombre..." required>
            
            <label>Correo Electrónico:</label>
            <input type="email" name="email" placeholder="tu@email.com" required>
            
            <button type="submit">Registrarme</button>
        </form>
    </div>
    '''
    return render_pagina("Registro de Usuarios", contenido)

# 4. PANEL DE ADMINISTRACIÓN SECRETO (Solo para ti)
@app.route('/admin-secreto', methods=['GET', 'POST'])
def admin():
    mensaje = ""
    if request.method == 'POST':
        clave = request.form.get('clave')
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')

        if clave == MI_CONTRASEÑA:
            if titulo and texto:
                noticias.insert(0, {"titulo": titulo, "texto": texto, "fecha": "2026-08-29"})
                return redirect(url_for('home'))
        else:
            mensaje = "<p style='color:red; text-align:center;'>Contraseña incorrecta</p>"

    contenido = f'''
    <div class="card">
        <h2 style="color:#111; margin-top:0;">Panel Privado de Publicación</h2>
        {mensaje}
        <form method="POST">
            <label>Contraseña Administrador:</label>
            <input type="password" name="clave" placeholder="Clave secreta" required>
            
            <label>Título de la Noticia:</label>
            <input type="text" name="titulo" placeholder="Ej: Gran fichaje confirmado" required>
            
            <label>Contenido:</label>
            <textarea name="texto" rows="5" placeholder="Redacta la noticia..." required></textarea>
            
            <button type="submit">Publicar Noticia</button>
        </form>
    </div>
    '''
    return render_pagina("Panel Secreto", contenido)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
