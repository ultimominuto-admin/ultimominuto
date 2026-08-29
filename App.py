from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ultimominuto_secret_key_2026'

MI_CONTRASEÑA = "Manresa2017"

# Base de datos de noticias
noticias = [
    {
        "id": 1,
        "titulo": "Resumen Verificado: Novedades del Mercado de Fichajes",
        "categoria": "Fichajes",
        "imagen": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=800&q=80",
        "texto": "Sintetizamos los reportes confirmados de las principales ligas. Sin rumores infundados ni fake news: solo traspasos oficiales y acuerdos de fuentes confiables.",
        "fecha": "2026-08-29"
    }
]

usuarios_registrados = []

def render_pagina(titulo_pagina, contenido_principal):
    login_btn = '<a href="/admin" class="nav-btn admin-btn">⚙️ Admin</a>'
    if session.get('logged_in'):
        login_btn = '<a href="/admin" class="nav-btn admin-btn">✍️ Redactar</a> <a href="/logout" class="nav-btn logout-btn">Salir</a>'

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>{titulo_pagina} | ÚLTIMOMINUTO - Noticias de Fútbol Verificadas</title>
    <meta name="description" content="Portal de noticias deportivas y fútbol en tiempo real. Resúmenes verificados, filtrado de fake news, fichajes y actualidad deportiva al instante.">
    <meta name="keywords" content="fútbol, noticias deportivas, fichajes, resúmenes de fútbol, noticias verificadas, deportes hoy, periodismo deportivo, sin fake news">
    <meta name="author" content="ÚLTIMOMINUTO">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{titulo_pagina} | ÚLTIMOMINUTO">
    <meta property="og:description" content="Información deportiva fiable y resúmenes sin noticias falsas.">
    <meta property="og:type" content="website">

    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --primary: #e50914;
            --dark: #0f0f11;
            --card-bg: #ffffff;
            --text: #1a1a1a;
            --text-muted: #666666;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Open Sans', sans-serif; }}
        body {{ background-color: #f4f6f9; color: var(--text); display: flex; flex-direction: column; min-height: 100vh; }}

        header {{ background: var(--dark); color: white; padding: 20px; text-align: center; border-bottom: 3px solid var(--primary); }}
        .logo-container {{ display: inline-flex; align-items: center; gap: 10px; text-decoration: none; }}
        .logo-icon {{ background: var(--primary); color: white; font-family: 'Montserrat', sans-serif; font-weight: 900; font-size: 22px; padding: 5px 12px; border-radius: 6px; transform: skewX(-10deg); display: inline-block; }}
        .logo-text {{ font-family: 'Montserrat', sans-serif; font-size: 32px; font-weight: 900; letter-spacing: -1px; color: #ffffff; text-transform: uppercase; }}
        .slogan {{ font-size: 12px; color: #aaa; text-transform: uppercase; letter-spacing: 2px; margin-top: 5px; font-weight: 600; }}

        nav {{ background: #18181c; display: flex; justify-content: center; align-items: center; flex-wrap: wrap; border-bottom: 1px solid #2a2a2e; }}
        nav a {{ color: #d1d1d1; text-decoration: none; padding: 14px 18px; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 13px; text-transform: uppercase; transition: all 0.3s; }}
        nav a:hover {{ background: var(--primary); color: white; }}
        .nav-btn {{ border-radius: 4px; margin: 4px; padding: 6px 12px !important; font-size: 11px !important; }}
        .admin-btn {{ background: var(--primary); color: white !important; }}
        .logout-btn {{ background: #333; color: white !important; }}

        .container {{ max-width: 950px; margin: 30px auto; padding: 0 15px; flex: 1; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        
        .news-card {{ background: var(--card-bg); border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); display: flex; flex-direction: column; }}
        .news-img {{ width: 100%; height: 180px; object-fit: cover; }}
        .news-body {{ padding: 18px; flex-grow: 1; display: flex; flex-direction: column; }}
        .news-tag {{ align-self: flex-start; background: rgba(229, 9, 20, 0.1); color: var(--primary); padding: 3px 8px; border-radius: 12px; font-size: 10px; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; }}
        .news-title {{ font-family: 'Montserrat', sans-serif; font-size: 17px; font-weight: 700; color: var(--dark); margin-bottom: 8px; line-height: 1.3; }}
        .news-date {{ font-size: 11px; color: var(--text-muted); margin-bottom: 10px; }}
        .news-text {{ font-size: 13px; color: #444; line-height: 1.6; flex-grow: 1; }}

        .info-card {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); max-width: 600px; margin: auto; }}
        .info-card h2 {{ font-family: 'Montserrat', sans-serif; font-size: 22px; font-weight: 900; margin-bottom: 15px; color: var(--dark); border-bottom: 3px solid var(--primary); display: inline-block; padding-bottom: 4px; }}
        
        label {{ font-weight: 700; display: block; margin-top: 12px; margin-bottom: 4px; font-size: 12px; text-transform: uppercase; color: #444; }}
        input, textarea, select {{ width: 100%; padding: 10px 12px; border: 1px solid #ccc; border-radius: 6px; font-size: 14px; margin-bottom: 10px; }}
        
        .btn-primary {{ background: var(--primary); color: white; border: none; padding: 12px; border-radius: 6px; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 14px; text-transform: uppercase; width: 100%; margin-top: 15px; cursor: pointer; transition: background 0.3s; display: inline-block; text-align: center; text-decoration: none; }}
        .btn-primary:hover {{ background: #b80710; }}

        footer {{ background: var(--dark); color: #888; padding: 30px 20px 15px; margin-top: 40px; font-size: 12px; line-height: 1.6; border-top: 1px solid #222; }}
        .footer-content {{ max-width: 950px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; text-align: left; }}
        .footer-col h4 {{ color: #fff; font-family: 'Montserrat', sans-serif; margin-bottom: 10px; font-size: 14px; }}
        .seo-box {{ background: #151518; padding: 15px; border-radius: 6px; margin-top: 20px; font-size: 11px; color: #777; border-left: 2px solid var(--primary); }}
        .footer-copy {{ text-align: center; margin-top: 20px; padding-top: 15px; border-top: 1px solid #222; font-weight: 600; color: #666; }}
    </style>
</head>
<body>
    <header>
        <a href="/" class="logo-container">
            <span class="logo-icon">UM</span>
            <span class="logo-text">ÚLTIMOMINUTO</span>
        </a>
        <div class="slogan">Noticias Deportivas Verificadas al Instante</div>
    </header>

    <nav>
        <a href="/">Noticias</a>
        <a href="/nosotros">Sobre Nosotros</a>
        <a href="/registro">Notificarme</a>
        <a href="/donaciones">Donaciones</a>
        {login_btn}
    </nav>
    
    <div class="container">
        {contenido_principal}
    </div>

    <footer>
        <div class="footer-content">
            <div class="footer-col">
                <h4>ÚLTIMOMINUTO</h4>
                <p>El portal digital independiente comprometido con la veracidad en el fútbol y deporte internacional. Síntesis clara sin clickbait.</p>
            </div>
            <div class="footer-col">
                <h4>Categorías Principales</h4>
                <p>Fichajes Oficiales • Champions League • Resultados en Vivo • Rumores Verificados • Análisis Táctico</p>
            </div>
        </div>
        
        <div class="seo-box">
            <strong>Portal de Periodismo Deportivo Verificado:</strong> Encuentra resúmenes de fútbol diario, información de transferencias filtrada sin fake news, alineaciones y noticias de última hora en tiempo real. 
        </div>

        <div class="footer-copy">
            © 2026 ÚLTIMOMINUTO. Todos los derechos reservados.
        </div>
    </footer>
</body>
</html>'''

@app.route('/')
def home():
    html_noticias = ""
    for n in noticias:
        img_src = n.get("imagen") or "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=800&q=80"
        html_noticias += f'''
        <div class="news-card">
            <img src="{img_src}" class="news-img" alt="Noticia">
            <div class="news-body">
                <span class="news-tag">{n.get("categoria", "Fútbol")}</span>
                <h3 class="news-title">{n["titulo"]}</h3>
                <div class="news-date">🗓️ {n["fecha"]} • Verificado</div>
                <p class="news-text">{n["texto"]}</p>
            </div>
        </div>
        '''
    contenido = f'<div class="grid">{html_noticias}</div>'
    return render_pagina("Noticias Verificadas", contenido)

@app.route('/nosotros')
def nosotros():
    contenido = '''
    <div class="info-card">
        <h2>Sobre Nosotros</h2>
        <p style="line-height:1.7; color:#444; margin-top: 10px;">
            En <strong>ÚLTIMOMINUTO</strong> combatimos la desinformación en el deporte. Nos dedicamos a rastrear y recopilar las noticias publicadas en los principales medios globales para ofrecerte únicamente <strong>resúmenes claros, directos y libres de fake news</strong>.
        </p>
        <p style="line-height:1.7; color:#444; margin-top: 15px;">
            Eliminamos el amarillismo, las especulaciones falsas y el clickbait. Nuestro compromiso es ahorrarte tiempo entregándote solo la información veraz y comprobada.
        </p>
    </div>
    '''
    return render_pagina("Sobre Nosotros", contenido)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    mensaje = ""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        if nombre and email:
            usuarios_registrados.append({"nombre": nombre, "email": email})
            mensaje = "<div style='background:#d4edda; color:#155724; padding:10px; border-radius:6px; margin-bottom:15px; font-weight:bold; text-align:center;'>¡Te has suscrito con éxito! Recibirás alertas con las noticias verificadas.</div>"
            
    contenido = f'''
    <div class="info-card">
        <h2>Registro de Alertas</h2>
        <p style="color:#666; margin-bottom: 15px;">Regístrate para recibir en tu correo las noticias verídicas del día sin spam.</p>
        {mensaje}
        <form method="POST">
            <label>Nombre Completo</label>
            <input type="text" name="nombre" placeholder="Tu nombre..." required>
            
            <label>Correo Electrónico</label>
            <input type="email" name="email" placeholder="tu@correo.com" required>
            
            <button type="submit" class="btn-primary">Activar Notificaciones</button>
        </form>
    </div>
    '''
    return render_pagina("Registro de Alertas", contenido)

# Donaciones configuradas con donacionesultimominuto@gmail.com
@app.route('/donaciones')
def donaciones():
    contenido = '''
    <div class="info-card" style="text-align:center;">
        <h2>Apoya Nuestro Proyecto</h2>
        <p style="line-height:1.7; color:#444; margin-top: 10px;">
            Mantener un periodismo libre de falsedades e independiente requiere tiempo y recursos. Tu apoyo nos ayuda a seguir redactando y verificando información 100% fiable.
        </p>
        <div style="background:#f8f9fa; padding:20px; border-radius:8px; margin:20px 0; border:1px dashed #ccc;">
            <p style="font-weight:bold; color:#111; margin-bottom:10px;">Correo oficial de donaciones:</p>
            <p style="color:var(--primary); font-weight:bold; font-size:16px;">donacionesultimominuto@gmail.com</p>
        </div>
        <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=donacionesultimominuto@gmail.com&item_name=Donacion+Ultimo+Minuto&currency_code=EUR" target="_blank" class="btn-primary">
            💙 Hacer una Donación con PayPal
        </a>
    </div>
    '''
    return render_pagina("Donaciones", contenido)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    mensaje = ""
    if request.method == 'POST' and 'clave_login' in request.form:
        if request.form.get('clave_login') == MI_CONTRASEÑA:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            mensaje = "<div style='background:#f8d7da; color:#721c24; padding:10px; border-radius:6px; margin-bottom:15px; text-align:center; font-weight:bold;'>Contraseña incorrecta</div>"

    if request.method == 'POST' and 'titulo' in request.form:
        if session.get('logged_in'):
            titulo = request.form.get('titulo')
            categoria = request.form.get('categoria')
            imagen = request.form.get('imagen')
            texto = request.form.get('texto')
            
            if titulo and texto:
                nueva = {
                    "id": len(noticias) + 1,
                    "titulo": titulo,
                    "categoria": categoria,
                    "imagen": imagen if imagen else "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=800&q=80",
                    "texto": texto,
                    "fecha": "2026-08-29"
                }
                noticias.insert(0, nueva)
                return redirect(url_for('home'))

    if not session.get('logged_in'):
        contenido = f'''
        <div class="info-card">
            <h2>Acceso Administrador</h2>
            {mensaje}
            <form method="POST">
                <label>Contraseña Administrador</label>
                <input type="password" name="clave_login" placeholder="Ingresa la clave" required>
                <button type="submit" class="btn-primary">Entrar al Panel</button>
            </form>
        </div>
        '''
        return render_pagina("Acceso Admin", contenido)

    contenido = f'''
    <div class="info-card">
        <h2>Redactar Noticia Verificada</h2>
        <form method="POST">
            <label>Título de la Noticia</label>
            <input type="text" name="titulo" placeholder="Ej: Resumen oficial de fichajes" required>
            
            <label>Categoría</label>
            <select name="categoria">
                <option value="Fichajes">Fichajes</option>
                <option value="Champions League">Champions League</option>
                <option value="La Liga">La Liga</option>
                <option value="Internacional">Internacional</option>
            </select>
            
            <label>URL de Imagen (Opcional)</label>
            <input type="url" name="imagen" placeholder="https://ejemplo.com/imagen.jpg">
            
            <label>Resumen Verificado (Sin Fake News)</label>
            <textarea name="texto" rows="5" placeholder="Escribe el resumen comprobado de la noticia..." required></textarea>
            
            <button type="submit" class="btn-primary">🚀 Publicar Noticia</button>
        </form>
    </div>
    '''
    return render_pagina("Redactar", contenido)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
