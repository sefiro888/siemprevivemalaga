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


def orn_quote(name, eyebrow, text):
    return (f'<div class="orn-quote" data-reveal><img class="orn" src="{ORN}{name}.webp" alt="" aria-hidden="true" loading="lazy">'
            f'<div><span class="orn-quote-eyebrow">{eyebrow}</span><p class="orn-quote-text">{text}</p></div></div>')

# Contenido ampliado de cada colección
LEADS = {
    'ramos.html': dict(orn='ramos', qe='El detalle que habla', q='Un ramo dice lo que a veces no sabemos decir.',
        items=[('Ramo clásico', 'Rosas y flor de temporada con verdes, compacto y elegante. Nunca falla.'),
               ('Ramo silvestre', 'Aire de campo recién cortado: movimiento, texturas y flores pequeñas en libertad.'),
               ('Ramo en un solo tono', 'Varias flores de un mismo color para un efecto delicado y muy actual.'),
               ('Ramo a tu medida', 'Tú eliges colores, tamaño y presupuesto; nosotros le damos forma.')],
        ideal=['Cumpleaños', 'Aniversarios', 'Dar las gracias', 'Porque sí']),
    'orquideas.html': dict(orn='orquideas', qe='Belleza serena', q='Una presencia delicada para disfrutar despacio.',
        items=[('Orquídea en maceta', 'Phalaenopsis de una o dos varas, lista para regalar y fácil de cuidar.'),
               ('Composición de orquídeas', 'Varias plantas reunidas en un mismo recipiente para lucir en grande.'),
               ('Con maceta decorativa', 'Acompañada de cerámica o cestería para integrarla en tu casa.'),
               ('Vara de orquídea', 'Como protagonista de un ramo o de un centro para ocasiones especiales.')],
        ideal=['Casa nueva', 'Nacimientos', 'Regalo de empresa', 'Decoración']),
    'rosas.html': dict(orn='rosas', qe='Un clásico vivo', q='Cada rosa tiene su propia manera de emocionar.',
        items=[('Una sola rosa', 'El gesto más sencillo y quizá el más elegante, con lazo y tarjeta.'),
               ('Docena de rosas', 'El ramo clásico por excelencia, en rojo o en el tono que prefieras.'),
               ('Rosas de colores', 'Rojo pasión, rosa ternura, blanco serenidad o amarillo alegría.'),
               ('Rosas con acompañamiento', 'Combinadas con paniculata, eucalipto u otras flores de temporada.')],
        ideal=['San Valentín', 'Aniversarios', 'Declaraciones', 'Día de la Madre']),
    'variedad-de-flores.html': dict(orn='variedad', qe='Color en cada pétalo', q='Cuando las flores se mezclan, nace algo único.',
        items=[('Flor de temporada', 'Lo mejor de cada momento del año: tulipanes, girasoles, margaritas, lirios…'),
               ('Mezcla de colores', 'Composiciones alegres que combinan tonos y texturas con equilibrio.'),
               ('En jarrón o cesta', 'Arreglos listos para colocar en una mesa, un recibidor o una celebración.'),
               ('Flor suelta', 'Tallos sueltos para que crees tu propio jarrón en casa.')],
        ideal=['Casa', 'Cumpleaños', 'Mesa de celebración', 'Alegrar el día']),
    'fechas-especiales.html': dict(orn='fechas', qe='Momentos que importan', q='Hay fechas que merecen florecer.',
        items=[('San Valentín', 'Rosas, ramos y detalles para decir «te quiero» a lo grande.'),
               ('Día de la Madre', 'Flores y plantas para agradecer todo lo que hace por ti.'),
               ('Celebraciones familiares', 'Comuniones, graduaciones, aniversarios y reuniones especiales.'),
               ('Recuerdos y homenajes', 'Composiciones sobrias y respetuosas para acompañar a quien lo necesita.')],
        ideal=['Encargar con antelación', 'Tarjeta personalizada', 'Recogida en tienda', 'Consulta de entrega']),
    'macetas.html': dict(orn='macetas', qe='Un rincón con vida', q='Una planta es un regalo que sigue creciendo.',
        items=[('Plantas de interior', 'Verdes fáciles de cuidar que llenan de vida salones, dormitorios y oficinas.'),
               ('Plantas con flor', 'Color que dura semanas: ideales para regalar o alegrar una terraza.'),
               ('Macetas decorativas', 'Cerámica, barro o cestería para que la planta luzca como merece.'),
               ('Composiciones de plantas', 'Varias especies combinadas en un mismo recipiente.')],
        ideal=['Casa nueva', 'Oficina', 'Regalo duradero', 'Amantes del verde']),
    'cactus-y-plantas.html': dict(orn='cactus', qe='Verdes singulares', q='Pequeños, resistentes y llenos de carácter.',
        items=[('Cactus individuales', 'Formas curiosas y muy poco riego: perfectos para empezar.'),
               ('Suculentas', 'Rosetas de colores suaves que casi se cuidan solas.'),
               ('Maceta artesanal', 'Cactus y suculentas en recipientes decorados a mano.'),
               ('Composiciones', 'Pequeños jardines de varias plantas para una mesa o una estantería.')],
        ideal=['Escritorio', 'Regalo original', 'Poco riego', 'Principiantes']),
    'rosas-eternas.html': dict(orn='regalos', qe='Un recuerdo que permanece', q='Una rosa que guarda el momento para siempre.',
        items=[('Rosa bajo cúpula', 'Una pieza de cristal que protege la rosa y la convierte en recuerdo.'),
               ('Elige el color', 'Tonos clásicos o más atrevidos según la persona y la ocasión.'),
               ('Presentación', 'Base, lazo y tarjeta para que el regalo llegue listo para emocionar.'),
               ('Pack con detalle', 'Combinada con otros detalles para un regalo más completo.')],
        ideal=['Aniversarios', 'San Valentín', 'Recuerdo especial', 'Sin riego']),
    'packs-de-regalo.html': dict(orn='fechas', qe='Detalles con intención', q='Un regalo pensado de principio a fin.',
        items=[('Flores y peluche', 'La combinación más tierna para cumpleaños, nacimientos o San Valentín.'),
               ('Flores y detalle', 'Un ramo acompañado de un pequeño complemento elegido para esa persona.'),
               ('Planta y tarjeta', 'Un regalo duradero con un mensaje escrito a mano.'),
               ('Pack a tu medida', 'Cuéntanos a quién quieres sorprender y lo preparamos juntos.')],
        ideal=['Cumpleaños', 'San Valentín', 'Nacimientos', 'Sorpresas']),
}

def build_lead(s, page):
    L = LEADS[page]
    m = re.search(r'<div class="category-lead lead-v2"[^>]*>.*?<!--/lead--></div>', s, flags=re.S) \
        or re.search(r'<div class="category-lead"[^>]*>.*?</p></div>', s, flags=re.S)
    if not m:
        return s
    block = m.group(0)
    eyebrow = re.search(r'<span class="eyebrow">(.*?)</span>', block).group(1)
    h2 = re.search(r'<h2[^>]*>.*?</h2>', block, flags=re.S).group(0)
    p = (re.search(r'<p class="lead-p">(.*?)</p>', block, flags=re.S) or re.search(r'<p>(.*?)</p>', block, flags=re.S)).group(1)
    items = ''.join(f'<li><span>{i+1:02d}</span><div><strong>{t}</strong><small>{d}</small></div></li>' for i, (t, d) in enumerate(L['items']))
    ideal = ''.join(f'<li>{x}</li>' for x in L['ideal'])
    new = (f'<div class="category-lead lead-v2">'
           f'<div class="lead-intro" data-reveal><span class="eyebrow">{eyebrow}</span>{h2}<p class="lead-p">{p}</p>{orn_quote(L["orn"], L["qe"], L["q"])}</div>'
           f'<aside class="offer-card" data-reveal="right"><span class="eyebrow">Qué puedes encargar</span><ul class="offer-list">{items}</ul>'
           f'<p class="offer-label">Ideal para</p><ul class="chips">{ideal}</ul>'
           f'<a class="button" href="{WA}" target="_blank" rel="noopener noreferrer">Pedir por WhatsApp</a>'
           f'<p class="offer-note">Disponibilidad y precios según temporada: te lo confirmamos por WhatsApp.</p></aside>'
           f'<!--/lead--></div>')
    return s.replace(block, new, 1)


# Foto de fondo de cada cabecera (alta resolución, banco de imágenes)
HERO_IMG = {
    'index.html': ('inicio', 'Rosas de jardín en tonos rosa y melocotón'),
    'ramos.html': ('ramos', 'Florista atando un ramo de flores rosadas'),
    'orquideas.html': ('orquideas', 'Orquídeas fucsia en flor'),
    'rosas.html': ('rosas', 'Rosas rojas con hojas de eucalipto'),
    'variedad-de-flores.html': ('variedad', 'Composición de flores variadas en tonos cálidos'),
    'fechas-especiales.html': ('fechas', 'Centro floral en una mesa de celebración'),
    'macetas.html': ('macetas', 'Plantas de interior en macetas junto a una ventana'),
    'cactus-y-plantas.html': ('cactus', 'Cactus y suculentas en macetas'),
    'rosas-eternas.html': ('rosas-eternas', 'Rosas en tonos melocotón'),
    'packs-de-regalo.html': ('packs', 'Rosas rojas junto a una caja de regalo'),
    'bodas.html': ('bodas', 'Novia con ramo de rosas rosadas y paniculata'),
    'eventos.html': ('eventos', 'Mesa de evento con camino de flores blancas'),
    'galeria.html': ('galeria', 'Floristería con composiciones de flores de colores'),
}

def set_hero_img(s, page):
    if page not in HERO_IMG:
        return s
    name, alt = HERO_IMG[page]
    src = f'assets/images/cabeceras/{name}.webp'
    s = re.sub(r'(<div class="page-hero-image"[^>]*><img )src="[^"]*" alt="[^"]*"', lambda m: f'{m.group(1)}src="{src}" alt="{alt}, imagen de banco"', s, count=1)
    s = re.sub(r'<link rel="preload" as="image" href="[^"]*">', f'<link rel="preload" as="image" href="{src}">', s, count=1)
    s = re.sub(r'(<div class="page-hero-image"[^>]*>.*?<span class="photo-tag">)[^<]*(</span>)', lambda m: m.group(1) + 'Imagen de banco' + m.group(2), s, count=1, flags=re.S)
    return s


# Dirección pública de la web: cámbiala aquí cuando tenga dominio propio
SITE = 'https://sefiro888.github.io/siemprevivemalaga/'

# Título que se ve al compartir el enlace (WhatsApp, Facebook…)
OG_TITLE = {
    'index.html': 'Floristería Siempre Vive · Flores con alma en Vélez-Málaga',
    'ramos.html': 'Ramos de flores · Siempre Vive Vélez-Málaga',
    'orquideas.html': 'Orquídeas · Siempre Vive Vélez-Málaga',
    'rosas.html': 'Rosas · Siempre Vive Vélez-Málaga',
    'variedad-de-flores.html': 'Variedad de flores · Siempre Vive Vélez-Málaga',
    'fechas-especiales.html': 'Flores para fechas especiales · Siempre Vive',
    'macetas.html': 'Plantas y macetas · Siempre Vive Vélez-Málaga',
    'cactus-y-plantas.html': 'Cactus y plantas · Siempre Vive Vélez-Málaga',
    'rosas-eternas.html': 'Rosas eternas · Siempre Vive Vélez-Málaga',
    'packs-de-regalo.html': 'Packs de regalo con flores · Siempre Vive',
    'bodas.html': 'Ramos de novia y arreglos de boda · Siempre Vive',
    'eventos.html': 'Flores para eventos corporativos y sociales · Siempre Vive',
    'galeria.html': 'Galería de trabajos · Floristería Siempre Vive',
    'sobre-nosotros.html': 'Conoce Siempre Vive · Floristería en Vélez-Málaga',
}

def head_meta(s, page):
    if page not in OG_TITLE:
        return s
    for pat in [r'\s*<meta property="og:[^>]*>', r'\s*<meta name="twitter:[^>]*>', r'\s*<link rel="canonical"[^>]*>',
                r'\s*<link rel="icon"[^>]*>', r'\s*<link rel="apple-touch-icon"[^>]*>', r'\s*<link rel="manifest"[^>]*>',
                r'\s*<meta name="theme-color"[^>]*>', r'\s*<!--og-->']:
        s = re.sub(pat, '', s)
    key = page[:-5]
    url = SITE + ('' if page == 'index.html' else page)
    img = f'{SITE}assets/images/compartir/{key}.jpg'
    title = OG_TITLE[page]
    desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    block = ('\n  <!--og--><meta name="theme-color" content="#1d3a2f">'
             f'<link rel="canonical" href="{url}">'
             '<link rel="icon" type="image/png" sizes="32x32" href="assets/images/compartir/favicon-32.png">'
             '<link rel="apple-touch-icon" href="assets/images/compartir/apple-touch-icon.png">'
             '<link rel="manifest" href="site.webmanifest">'
             '\n  <meta property="og:type" content="website"><meta property="og:site_name" content="Floristería Siempre Vive"><meta property="og:locale" content="es_ES">'
             f'<meta property="og:url" content="{url}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">'
             f'\n  <meta property="og:image" content="{img}"><meta property="og:image:secure_url" content="{img}"><meta property="og:image:type" content="image/jpeg">'
             f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{title}">'
             f'\n  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{img}">')
    s = re.sub(r'(<meta name="description" content="[^"]*">)', lambda m: m.group(1) + block, s, count=1)
    return s

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
    s = head_meta(s, page)
    s = set_hero_img(s, page)
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
        # presentación de la colección: texto, adorno con frase y tarjeta «Qué puedes encargar»
        if page in LEADS:
            s = build_lead(s, page)
        # en «Siempre Vive» el adorno va acompañado de una frase
        if page == 'sobre-nosotros.html':
            s = re.sub(r'<img class="orn orn-lead"[^>]*>', '', s)
            if 'orn-quote' not in s:
                s = re.sub(r'(<div class="about-split"><div>.*?)(</div><figure)', lambda m: m.group(1) + orn_quote('portada-esquina', 'Nuestro lugar', 'Un pequeño paraíso de colores en Vélez-Málaga.') + m.group(2), s, count=1, flags=re.S)
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
            s = re.sub(r'(<aside class="offer-card".*?<a class="button"[^>]*>)[^<]*?(</a>)', lambda m: m.group(1) + label + m.group(2), s, count=1, flags=re.S)
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
