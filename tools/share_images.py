# -*- coding: utf-8 -*-
"""Genera las imágenes de vista previa (1200x630) que muestran WhatsApp, Facebook, etc.
al compartir un enlace, y los iconos del sitio.
Uso:  python tools/share_images.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
F = 'tools/fonts/'
OUT = 'assets/images/compartir'
os.makedirs(OUT, exist_ok=True)

CREAM = (248, 243, 234)
FOREST = (29, 58, 47)
ROSE = (163, 90, 105)
GOLD = (180, 140, 85)
SOFT = (86, 103, 93)

def font(name, size):
    return ImageFont.truetype(F + name, size)

# página -> (imagen de fondo, antetítulo, título, subtítulo)
SHARE = {
    'index': ('cabeceras/inicio', 'Vélez-Málaga', 'Flores con alma', 'Ramos, novias, eventos y plantas para decir lo que sientes.'),
    'ramos': ('cabeceras/ramos', 'Colección', 'Ramos', 'Un gesto muy tuyo, flor a flor.'),
    'orquideas': ('cabeceras/orquideas', 'Colección', 'Orquídeas', 'Una presencia delicada para disfrutar despacio.'),
    'rosas': ('cabeceras/rosas', 'Colección', 'Rosas', 'Cada rosa tiene su propia manera de emocionar.'),
    'variedad-de-flores': ('cabeceras/variedad', 'Colección', 'Variedad de flores', 'Cuando las flores se mezclan, nace algo único.'),
    'fechas-especiales': ('cabeceras/fechas', 'Colección', 'Fechas especiales', 'Hay fechas que merecen florecer.'),
    'macetas': ('cabeceras/macetas', 'Colección', 'Macetas', 'Una planta es un regalo que sigue creciendo.'),
    'cactus-y-plantas': ('cabeceras/cactus', 'Colección', 'Cactus y plantas', 'Pequeños, resistentes y llenos de carácter.'),
    'rosas-eternas': ('cabeceras/rosas-eternas', 'Colección', 'Rosas eternas', 'Una rosa que guarda el momento para siempre.'),
    'packs-de-regalo': ('cabeceras/packs', 'Colección', 'Packs de regalo', 'Un regalo pensado de principio a fin.'),
    'bodas': ('cabeceras/bodas', 'Especialidad', 'Ramos de novia y bodas', 'Arreglos que capturan la esencia de vuestro amor.'),
    'eventos': ('cabeceras/eventos', 'Especialidad', 'Eventos corporativos y sociales', 'Elegancia y sofisticación para cualquier evento.'),
    'galeria': ('cabeceras/galeria', 'Inspiración', 'Galería de trabajos', 'Ramos, bodas, eventos, plantas y regalos.'),
    'sobre-nosotros': ('../../471170567_605242295371037_7502117801894070333_n', 'Conócenos', 'Un paraíso de colores', 'Floristería y artesanía en Vélez-Málaga.'),
}

def load(path):
    for ext in ('.webp', '.jpg', '.png', '.jpeg'):
        p = 'assets/images/' + path + ext
        if os.path.exists(p):
            return Image.open(p).convert('RGB')
    raise FileNotFoundError(path)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines

def arch_mask(w, h, r_bottom=26):
    m = Image.new('L', (w * 2, h * 2), 0)
    d = ImageDraw.Draw(m)
    W, H, R = w * 2, h * 2, w  # semicírculo superior
    d.ellipse([0, 0, W, 2 * R], fill=255)
    d.rounded_rectangle([0, R, W, H], radius=r_bottom * 2, fill=255)
    d.rectangle([0, R, W, H - r_bottom * 2], fill=255)
    return m.resize((w, h), Image.LANCZOS)

logo = Image.open('logo.jpeg').convert('RGB')
lw = 118
logo_c = ImageOps.fit(logo, (lw * 2, lw * 2), Image.LANCZOS)
lm = Image.new('L', (lw * 2, lw * 2), 0); ImageDraw.Draw(lm).ellipse([0, 0, lw * 2 - 1, lw * 2 - 1], fill=255)
logo_c.putalpha(lm); logo_c = logo_c.resize((lw, lw), Image.LANCZOS)
orn = Image.open('assets/images/adornos/esquina-inf.webp').convert('RGBA')

for key, (bg, eyebrow, title, sub) in SHARE.items():
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), CREAM)
    # halo rosado suave
    halo = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([700, -250, 1500, 550], fill=(244, 214, 218, 150))
    halo = halo.filter(ImageFilter.GaussianBlur(90))
    img.paste(halo, (0, 0), halo)
    d = ImageDraw.Draw(img)

    # foto en arco a la derecha
    aw, ah = 420, 560
    ax, ay = W - aw - 70, H - ah - 35
    photo = ImageOps.fit(load(bg), (aw, ah), Image.LANCZOS, centering=(0.5, 0.45))
    img.paste(photo, (ax, ay), arch_mask(aw, ah))
    # marco dorado fino
    fr = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); fd = ImageDraw.Draw(fr)
    pad = 13 * 2; x0, y0, x1, y1 = (ax * 2 - pad, ay * 2 - pad, (ax + aw) * 2 + pad, (ay + ah) * 2 + pad)
    r = (x1 - x0) // 2
    fd.arc([x0, y0, x1, y0 + 2 * r], 180, 360, fill=GOLD + (170,), width=3)
    fd.line([x0, y0 + r, x0, y1], fill=GOLD + (170,), width=3)
    fd.line([x1, y0 + r, x1, y1], fill=GOLD + (170,), width=3)
    fr = fr.resize((W, H), Image.LANCZOS)
    img.paste(fr, (0, 0), fr)
    # adorno floral junto a la base del arco (sobre el fondo crema, no sobre la foto)
    o = orn.copy(); o.thumbnail((150, 150), Image.LANCZOS)
    img.paste(o, (ax - o.width - 22, H - o.height - 10), o)

    # texto a la izquierda
    x = 70
    img.paste(logo_c, (x, 52), logo_c)
    d.text((x + lw + 22, 78), 'Siempre Vive', font=font('cormorant-garamond_latin-500-normal.ttf', 46), fill=FOREST)
    d.text((x + lw + 24, 132), 'FLORISTERÍA · ARTESANÍA', font=font('dm-sans_latin-600-normal.ttf', 17), fill=ROSE, spacing=4)

    y = 222
    d.line([x, y + 12, x + 38, y + 12], fill=ROSE, width=2)
    d.text((x + 54, y), eyebrow.upper(), font=font('dm-sans_latin-600-normal.ttf', 19), fill=ROSE)
    tsize = 82 if len(title) < 16 else 64 if len(title) < 26 else 56
    tf = font('cormorant-garamond_latin-500-normal.ttf', tsize)
    lines = wrap(d, title, tf, 560)
    y += 42
    for ln in lines:
        d.text((x, y), ln, font=tf, fill=FOREST)
        y += int(tsize * 1.02)
    sf = font('cormorant-garamond_latin-500-italic.ttf', 32)
    y += 10
    for ln in wrap(d, sub, sf, 560)[:2]:
        d.text((x, y), ln, font=sf, fill=SOFT)
        y += 40
    # pie: WhatsApp
    bf = font('dm-sans_latin-600-normal.ttf', 20)
    label = 'Pide por WhatsApp · 622 74 97 70'
    tw = d.textlength(label, font=bf)
    by = H - 92
    d.rounded_rectangle([x, by, x + tw + 56, by + 52], radius=26, fill=FOREST)
    d.ellipse([x + 20, by + 21, x + 30, by + 31], fill=(127, 211, 160))
    d.text((x + 40, by + 13), label, font=bf, fill=(255, 255, 255))

    out = f'{OUT}/{key}.jpg'
    img.save(out, 'JPEG', quality=86, optimize=True, progressive=True)
    print(out, os.path.getsize(out) // 1024, 'KB')

# iconos del sitio (pestaña del navegador y pantalla de inicio del móvil)
for size, name in [(32, 'favicon-32.png'), (180, 'apple-touch-icon.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
    ic = ImageOps.fit(logo, (size, size), Image.LANCZOS)
    ic.save(f'{OUT}/{name}')
print('iconos listos')
