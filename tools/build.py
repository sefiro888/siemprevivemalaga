# -*- coding: utf-8 -*-
"""Aplica la cabecera, el menú, el pie y los adornos comunes a todas las páginas.
Es idempotente: se puede ejecutar tantas veces como haga falta.
Uso:  python tools/build.py
"""
import re, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

WA = 'https://wa.me/34622749770'
ORN = 'assets/images/adornos/'
import time
VERSION = time.strftime('%m%d%H%M')
WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a9.9 9.9 0 0 0-8.53 15L2 22l5.15-1.4A10 10 0 1 0 12 2Zm4.5 12.2'
          'c-.25-.12-1.48-.73-1.71-.81-.23-.08-.4-.12-.57.12-.17.25-.65.81-.8.98-.15.17-.3.19-.55.06-.25-.12-1.06-.39-2.02-1.25'
          '-.75-.67-1.25-1.5-1.4-1.75-.15-.25-.02-.39.11-.52.11-.11.25-.3.37-.44.12-.14.17-.25.25-.42.08-.17.04-.32-.02-.45'
          '-.06-.12-.57-1.37-.78-1.87-.21-.49-.42-.42-.57-.43h-.49c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1s.9 2.44 1.03 2.6'
          'c.12.17 1.77 2.7 4.28 3.78 2.1.9 2.55.72 3.03.68.49-.07 1.48-.61 1.69-1.2.21-.59.21-1.09.15-1.2-.07-.1-.23-.16-.48-.29Z"/></svg>')

COLLECTIONS = [
    ('ramos.html', 'Ramos', 'El detalle que habla', 'ramos'),
    ('orquideas.html', 'Orquídeas', 'Elegancia natural', 'orquideas'),
    ('rosas.html', 'Rosas', 'Un gesto clásico', 'rosas'),
    ('variedad-de-flores.html', 'Variedad de flores', 'Color en cada pétalo', 'variedad'),
    ('fechas-especiales.html', 'Fechas especiales', 'Momentos que importan', 'fechas'),
    ('macetas.html', 'Macetas', 'Un rincón con vida', 'macetas'),
    ('cactus-y-plantas.html', 'Cactus y plantas', 'Verdes singulares', 'cactus'),
    ('rosas-eternas.html', 'Rosas eternas', 'Un recuerdo que permanece', 'rosas-eternas'),
    ('packs-de-regalo.html', 'Packs de regalo', 'Detalles con intención', 'packs'),
]
SPECIAL = [
    ('bodas.html', 'Ramos de novia y bodas', 'Arreglos que capturan la esencia de vuestro amor', 'bodas'),
    ('eventos.html', 'Eventos corporativos y sociales', 'Elegancia y sofisticación para cada evento', 'eventos'),
]

# página -> (tema WhatsApp, adorno del encabezado, adorno de la llamada final)
PAGES = {
    'ramos.html': ('Ramos', 'ramos', 'variedad'),
    'orquideas.html': ('Orquídeas', 'orquideas', 'portada-esquina'),
    'macetas.html': ('Macetas', 'macetas', 'cactus-plantas'),
    'cactus-y-plantas.html': ('Cactus y plantas', 'cactus', 'cactus-plantas'),
    'variedad-de-flores.html': ('Variedad de flores', 'variedad', 'ramos'),
    'fechas-especiales.html': ('Fechas especiales', 'fechas', 'portada-esquina'),
    'rosas.html': ('Rosas', 'rosas', 'ramos'),
    'rosas-eternas.html': ('Rosas eternas', 'regalos', 'rosas'),
    'packs-de-regalo.html': ('Packs de regalo', 'fechas', 'regalos'),
    'sobre-nosotros.html': ('', 'portada-esquina', 'variedad'),
}

def is_active(page, href):
    return ' is-active' if page == href else ''

def header(page):
    coll_active = page in [c[0] for c in COLLECTIONS]
    spec_active = page in [s[0] for s in SPECIAL]
    mega = ''.join(
        f'<a class="mega-item{is_active(page,h)}" href="{h}"><img src="assets/images/thumbs/{t}.webp" alt="" width="56" height="56" loading="lazy"><span><strong>{n}</strong><small>{tag}</small></span></a>'
        for h, n, tag, t in COLLECTIONS)
    spec = ''.join(
        f'<a class="spec-item{is_active(page,h)}" href="{h}"><span class="spec-img"><img src="assets/images/thumbs/{t}-card.webp" alt="" loading="lazy"></span><strong>{n}</strong><small>{tag}</small></a>'
        for h, n, tag, t in SPECIAL)
    m_coll = ''.join(
        f'<a class="mchip{is_active(page,h)}" href="{h}"><img src="assets/images/thumbs/{t}.webp" alt="" width="64" height="64" loading="lazy"><span>{n}</span></a>'
        for h, n, tag, t in COLLECTIONS)
    m_spec = ''.join(
        f'<a class="mspec{is_active(page,h)}" href="{h}"><img src="assets/images/thumbs/{t}-card.webp" alt="" loading="lazy"><span>{n}</span></a>'
        for h, n, tag, t in SPECIAL)
    def nl(href, label):
        cur = ' aria-current="page"' if page == href else ''
        return f'<a class="nav-link{is_active(page, href)}" href="{href}"{cur}>{label}</a>'
    home = '' if page == 'index.html' else 'index.html'
    return f'''<header class="site-header">
  <div class="topbar"><div class="container topbar-inner"><span class="topbar-msg"><span aria-hidden="true">✿</span> Floristería y artesanía en Vélez-Málaga</span><span class="topbar-links"><a href="tel:+34622749770">622 74 97 70</a><span aria-hidden="true">·</span><a href="https://www.instagram.com/floristeria_siempre_vive/" target="_blank" rel="noopener noreferrer">Instagram</a><span aria-hidden="true">·</span><a href="{home}#contacto">Av. Vivar Téllez, 53</a></span></div></div>
  <div class="header-main"><div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Siempre Vive, ir al inicio"><img src="logo.jpeg" width="64" height="64" alt=""><span class="brand-copy"><span class="brand-name">Siempre Vive</span><span class="brand-sub">Floristería · Artesanía</span></span></a>
    <nav class="desktop-nav" aria-label="Navegación principal">
      <div class="nav-dropdown nav-mega"><button class="nav-trigger{' is-active' if coll_active else ''}" type="button" aria-expanded="false" aria-controls="mega-colecciones">Colecciones <svg viewBox="0 0 12 8" aria-hidden="true"><path d="m1 1 5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button>
        <div class="dropdown-panel mega-panel" id="mega-colecciones"><div class="mega-inner">
          <div class="mega-intro"><span class="script">Nuestras</span><strong>colecciones</strong><p>Flores, plantas y detalles para cada forma de sentir. Elige una colección y pídela directamente por WhatsApp.</p><a class="text-link" href="index.html#flores">Verlas todas <span aria-hidden="true">↗</span></a><img class="mega-orn" src="{ORN}esquina-sup.webp" alt="" aria-hidden="true"></div>
          <div class="mega-grid">{mega}</div>
          <a class="mega-feature" href="galeria.html"><img src="assets/images/thumbs/galeria.webp" alt="" loading="lazy"><span><small>Inspírate</small><strong>Galería de trabajos</strong><em>Ver galería ↗</em></span></a>
        </div></div>
      </div>
      <div class="nav-dropdown nav-spec"><button class="nav-trigger{' is-active' if spec_active else ''}" type="button" aria-expanded="false" aria-controls="menu-bodas">Bodas y eventos <svg viewBox="0 0 12 8" aria-hidden="true"><path d="m1 1 5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button>
        <div class="dropdown-panel spec-panel" id="menu-bodas">{spec}</div>
      </div>
      {nl('galeria.html', 'Galería')}
      <a class="nav-link" href="index.html#ideas">Ideas para elegir</a>
      {nl('sobre-nosotros.html', 'Siempre Vive')}
      <a class="nav-link" href="{home}#contacto">Contacto</a>
    </nav>
    <a class="header-cta" href="{WA}" data-wa="" target="_blank" rel="noopener noreferrer"><span class="cta-dot" aria-hidden="true"></span>Pedir por WhatsApp</a>
    <button class="menu-toggle" type="button" aria-label="Abrir menú" aria-controls="mobile-menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div></div>
  <nav class="mobile-nav" id="mobile-menu" aria-label="Navegación móvil" inert>
    
    <div class="mnav-head"><a class="brand" href="index.html"><img src="logo.jpeg" width="48" height="48" alt=""><span class="brand-name">Siempre Vive</span></a><button class="mnav-close" type="button" aria-label="Cerrar menú"><span></span><span></span></button></div>
    <div class="mnav-body">
      <div class="mnav-links">
        <a href="index.html"{' aria-current="page"' if page=='index.html' else ''}><small>01</small>Inicio</a>
        <a href="galeria.html"{' aria-current="page"' if page=='galeria.html' else ''}><small>02</small>Galería</a>
        <a href="index.html#ideas"><small>03</small>Ideas para elegir</a>
        <a href="sobre-nosotros.html"{' aria-current="page"' if page=='sobre-nosotros.html' else ''}><small>04</small>Siempre Vive</a>
        <a href="{home}#contacto"><small>05</small>Contacto</a>
      </div>
      <p class="mnav-label">Bodas y eventos</p>
      <div class="mnav-spec">{m_spec}</div>
      <p class="mnav-label">Colecciones <span aria-hidden="true">→ desliza</span></p>
      <div class="mnav-chips">{m_coll}</div>
      <div class="mnav-foot"><a class="button btn-light-wa" href="{WA}" data-wa="" target="_blank" rel="noopener noreferrer">Pedir por WhatsApp</a><div class="mnav-contact"><a href="tel:+34622749770">622 74 97 70</a><a href="https://www.instagram.com/floristeria_siempre_vive/" target="_blank" rel="noopener noreferrer">Instagram ↗</a></div><span class="script">con amor, Siempre Vive</span></div>
      <img class="mnav-orn-b" src="{ORN}guirnalda-fina.webp" alt="" aria-hidden="true">
    </div>
  </nav>
</header>'''

def footer(page):
    home = '' if page == 'index.html' else 'index.html'
    colls = ''.join(f'<li><a href="{h}">{n}</a></li>' for h, n, _, _ in COLLECTIONS)
    return f'''<div class="footer-garland" aria-hidden="true"><img class="orn-garland" src="{ORN}guirnalda.webp" alt="" loading="lazy"><p class="script">Gracias por dejarnos formar parte de tus momentos</p></div>
<footer class="footer"><div class="container"><div class="footer-top">
  <div class="footer-about"><a class="footer-brand" href="index.html"><img src="logo.jpeg" width="56" height="56" alt="" loading="lazy">Siempre Vive</a><p>Floristería y artesanía en Vélez-Málaga. Un paraíso de colores para compartir.</p><a class="button btn-light-wa" href="{WA}" data-wa="" target="_blank" rel="noopener noreferrer">Escríbenos por WhatsApp</a></div>
  <div><small>Colecciones</small><ul>{colls}</ul></div>
  <div><small>Especialidades</small><ul><li><a href="bodas.html">Ramos de novia y bodas</a></li><li><a href="eventos.html">Eventos corporativos y sociales</a></li><li><a href="index.html#ideas">Ideas para elegir</a></li><li><a href="galeria.html">Galería</a></li><li><a href="sobre-nosotros.html">Siempre Vive</a></li></ul></div>
  <div><small>Visítanos</small><ul><li><a href="https://www.google.com/maps/search/?api=1&amp;query=Av.%20Vivar%20T%C3%A9llez%2053%2C%2029700%20V%C3%A9lez-M%C3%A1laga" target="_blank" rel="noopener noreferrer">Av. Vivar Téllez, 53<br>29700 Vélez-Málaga</a></li><li><a href="tel:+34622749770">622 74 97 70</a></li><li><a href="https://www.instagram.com/floristeria_siempre_vive/" target="_blank" rel="noopener noreferrer">@floristeria_siempre_vive ↗</a></li><li class="footer-hours">L–V 10:00–14:00 · 17:00–20:00<br>Sáb 10:00–14:00 · 17:00–19:00</li></ul></div>
</div><div class="footer-bottom"><span>© 2026 Siempre Vive · Vélez-Málaga</span><span>Demostración web · Imágenes de banco pendientes de sustituir por fotos originales</span></div></div></footer>'''

HEAD_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&amp;family=DM+Sans:wght@400;500;600;700&amp;family=Pinyon+Script&amp;display=swap">')

def orn(name, cls, extra=''):
    return f'<img class="orn {cls}" src="{ORN}{name}.webp" alt="" aria-hidden="true" loading="lazy"{extra}>'

def divider(name='divisor'):
    return f'<div class="orn-divider" aria-hidden="true"><img src="{ORN}{name}.webp" alt="" loading="lazy"></div>'

def process(path):
    page = os.path.basename(path)
    s = open(path, encoding='utf-8').read()
    o = s
    # cabecera y pie
    s = re.sub(r'<header class="site-header">.*?</header>', lambda m: header(page), s, flags=re.S)
    s = re.sub(r'(<div class="footer-garland".*?</div>\s*)?<footer class="footer">.*?</footer>', lambda m: footer(page), s, flags=re.S)
    # hojas de estilo y fuentes
    if 'premium.css' not in s:
        s = re.sub(r'<link rel="stylesheet" href="assets/css/styles.css(\?v=[\w.]+)?">', lambda m:
                   HEAD_FONTS + '<link rel="stylesheet" href="assets/css/styles.css"><link rel="stylesheet" href="assets/css/premium.css">', s, count=1)
    s = s.replace('WAICON', WA_SVG)
    # versión en los recursos para evitar cachés antiguas
    s = re.sub(r'assets/css/premium\.css(\?v=[\w.]+)?', f'assets/css/premium.css?v={VERSION}', s)
    s = re.sub(r'assets/css/styles\.css(\?v=[\w.]+)?', f'assets/css/styles.css?v={VERSION}', s)
    s = re.sub(r'assets/js/site\.js(\?v=[\w.]+)?', f'assets/js/site.js?v={VERSION}', s)

    if page in PAGES:
        topic, hero_orn, cta_orn = PAGES[page]
        # la cinta de texto va justo después del encabezado de página
        mq = re.search(r'\s*<div class="marquee".*?</div></div></div>', s, flags=re.S)
        if mq and s.index(mq.group(0)) < s.index('<section class="page-hero"'):
            block = mq.group(0).strip()
            s = s.replace(mq.group(0), '', 1)
            end = s.index('</section>', s.index('<section class="page-hero"')) + len('</section>')
            s = s[:end] + '\n' + block + s[end:]
        # imagen del encabezado en arco con adorno
        if 'hero-visual' not in s:
            s = re.sub(r'(<div class="page-hero-image"[^>]*>.*?</div>)(</section>)',
                       lambda m: f'<div class="hero-visual">{m.group(1)}</div>{m.group(2)}', s, count=1, flags=re.S)
        # los adornos nunca van sobre la foto del encabezado
        s = re.sub(r'<img class="orn orn-hero"[^>]*>', '', s)
        # adorno de la colección junto al titular de la introducción, en una zona libre
        if 'orn-lead' not in s:
            s, n = re.subn(r'(<div class="category-lead"[^>]*><div>.*?</h2>)', lambda m: m.group(1) + orn(hero_orn, 'orn-lead'), s, count=1, flags=re.S)
            if not n and '<div class="about-split"><div>' in s:
                s = re.sub(r'(<div class="about-split"><div>.*?)(</div><figure)', lambda m: m.group(1) + orn(hero_orn, 'orn-lead') + m.group(2), s, count=1, flags=re.S)
        # separador floral antes de la guía
        if 'orn-divider' not in s:
            for anchor in ['<section class="field-guide"', '<section class="about-offerings"']:
                if anchor in s:
                    s = s.replace(anchor, divider() + '\n' + anchor, 1)
                    break
        # adorno en la llamada final
        if 'orn-cta' not in s:
            s = re.sub(r'(<section class="container category-cta"[^>]*>)', lambda m: m.group(1) + orn(cta_orn, 'orn-cta'), s, count=1)
        # galería de categoría ampliable
        s = re.sub(r'<figure( data-reveal)?>(<img src="[^"]+" alt="[^"]*" loading="lazy">)',
                   lambda m: f'<figure data-reveal data-lightbox>{m.group(2)}', s)
        s = s.replace('<figure data-reveal data-lightbox data-lightbox>', '<figure data-reveal data-lightbox>')
        # botones de WhatsApp con el nombre de la colección
        if topic:
            label = f'Pedir {topic} por WhatsApp'
            s = re.sub(r'(<div class="hero-actions"><a class="button"[^>]*>)[^<]*?(</a>)', lambda m: m.group(1) + label + m.group(2), s, count=1)
            s = re.sub(r'(<section class="container category-cta".*?<a class="button"[^>]*>)[^<]*?(</a>)', lambda m: m.group(1) + label + m.group(2), s, count=1, flags=re.S)
        # enlaces de servicios hacia las nuevas páginas
        if page == 'sobre-nosotros.html':
            s = s.replace('<a href="fechas-especiales.html"><span>02 / La celebración</span>', '<a href="bodas.html"><span>02 / La celebración</span>')
            s = s.replace('<strong>Ver ocasiones ↗</strong>', '<strong>Ver bodas ↗</strong>')
            s = s.replace('<a href="fechas-especiales.html"><span>03 / El espacio</span>', '<a href="eventos.html"><span>03 / El espacio</span>')
        # enlaces relacionados: añadir especialidades
        if 'related-links' in s and 'bodas.html' not in s.split('related-links', 1)[1].split('</div>', 1)[0]:
            s = re.sub(r'(<div class="related-links">)', r'\1<a href="bodas.html">Bodas ↗</a><a href="eventos.html">Eventos ↗</a><a href="galeria.html">Galería ↗</a>', s, count=1)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s)
        print('actualizado', page)

for f in sorted(glob.glob('*.html')):
    process(f)
