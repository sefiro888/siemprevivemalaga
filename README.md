# Siempre Vive · demostración web

Web escaparate estática para Floristería y Artesanía Siempre Vive, en Vélez-Málaga. Abre `index.html` en un navegador o publica esta carpeta en GitHub Pages. Todas las rutas internas son relativas.

## Páginas (14)

| Página | Contenido |
| --- | --- |
| `index.html` | Portada: especialidades (bodas y eventos), 9 colecciones con botón de WhatsApp propio, **Ideas para elegir** (8 ocasiones + guía de color), la tienda, galería con visor, cómo encargar y contacto con mapa |
| `bodas.html` | **Ramos de novia y arreglos de boda** (nueva) |
| `eventos.html` | **Eventos corporativos y sociales** (nueva) |
| `galeria.html` | **Galería de trabajos** con filtros y ampliación (nueva) |
| `ramos.html`, `orquideas.html`, `rosas.html`, `variedad-de-flores.html`, `fechas-especiales.html`, `macetas.html`, `cactus-y-plantas.html`, `rosas-eternas.html`, `packs-de-regalo.html` | Colecciones |
| `sobre-nosotros.html` | La floristería |

## Estructura técnica

- `assets/css/styles.css`: estilos base originales.
- `assets/css/premium.css`: capa de diseño premium (paleta, tipografía Cormorant Garamond + DM Sans + Pinyon Script, menú, adornos, animaciones y adaptación a móvil). Se carga después de `styles.css`.
- `assets/js/site.js`: menú de escritorio y móvil, animaciones al hacer scroll, pétalos, pestañas de ideas, filtros y visor de galería, botones de WhatsApp por colección y botón flotante.
- `tools/build.py`: **genera la cabecera, el menú, el pie de página y los adornos comunes en todas las páginas.** Si cambias el menú o el pie, edítalo ahí y ejecuta:

  ```bash
  python tools/build.py
  ```

  Es seguro ejecutarlo varias veces. También actualiza el número de versión de CSS/JS para evitar cachés antiguas.

## WhatsApp por colección

Cada botón de WhatsApp abre un mensaje ya escrito con el nombre de la colección, por ejemplo: «¡Hola, Siempre Vive! 🌷 Me interesa la colección «Ramos»…».

- Dentro de una página de colección, los botones usan automáticamente el nombre de esa colección.
- Para forzar otro tema en un botón concreto: `data-wa="Nombre"`. Con `data-wa=""` el mensaje es general.
- Número de la demostración: **622 74 97 70**.

## Adornos florales

Los PNG originales de `assets/images/adornos_floristeria_siempre_vive (2)/` se han recortado y optimizado a WebP en `assets/images/adornos/` (de ~2 MB a 40–240 KB cada uno). Se colocan en esquinas, separadores y márgenes, nunca sobre títulos, con una animación suave de balanceo. En móvil se reducen y se recolocan.

## Pendiente antes de usarla como web definitiva

- **Fotografías originales:** la galería y las páginas de bodas y eventos usan fotos de banco (Pexels) e ilustraciones. Están marcadas en la web como «pendientes de sustituir por fotos originales de Siempre Vive». Solo la fachada y la bicicleta son fotos reales del negocio.
- Confirmar con el negocio la dirección, el horario, los servicios de bodas y eventos (montaje, plazos, etc.) y los textos finales.
- La foto de la fachada muestra un número de teléfono antiguo; su encuadre intenta dejarlo fuera de vista.
- Añadir una URL absoluta a las imágenes Open Graph cuando se conozca el dominio.
- En `assets/images/` siguen los PNG originales `Imagen de ChatGPT…` (unos 25 MB). La web ya no los usa (usa `ilustracion-XX.webp`); se pueden borrar antes de publicar para aligerar la carpeta.

Copia de seguridad de la versión anterior: `../siempreviveclaude_backup_original/`.

Fuentes y créditos de las imágenes en `FOTOGRAFIAS.md`.
