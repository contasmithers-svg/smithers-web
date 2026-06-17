# AUDITORÍA DE ENLACES INTERNOS — Smithers Web
Proyecto: /home/gondss/Escritorio/KAI/pagina-web/smithers-web
Fecha: junio 2026
Archivos .html: 14
  • 404.html (5276 bytes)
  • aviso-legal.html (10893 bytes)
  • carta.html (26870 bytes)
  • delivery.html (14579 bytes)
  • desayunos.html (27376 bytes)
  • entre-panes.html (17939 bytes)
  • eventos.html (14057 bytes)
  • index.html (22297 bytes)
  • legal.html (11504 bytes)
  • menu-del-dia.html (22980 bytes)
  • menu-shelby.html (18001 bytes)
  • privacidad.html (13147 bytes)
  • reservas.html (16688 bytes)
  • take-away.html (17296 bytes)

Archivo _redirects analizado — 18 reglas de redirección.

──────────────────────────────────────────────────────────────────────
## 1. ENLACES CON EXTENSIÓN .html EN href
──────────────────────────────────────────────────────────────────────
✅ 0 incidencias. No se encontró ningún href que contenga ".html".
   Todos los enlaces internos usan URLs limpias (clean URLs).

──────────────────────────────────────────────────────────────────────
## 2. VERIFICACIÓN DE ENLACES — ¿Existen los destinos?
──────────────────────────────────────────────────────────────────────
Total hrefs únicos: 49
  • Enlaces externos: 28
  • Anclas internas (#): 0
  • Enlaces internos válidos (clean URL / archivo): 21
  • Enlaces internos ROTOS: 0

✅ No hay enlaces rotos.

### Resumen de enlaces internos (clean URLs)

  • / → archivo local (0 usos)
  • /apple-touch-icon.png → archivo local (0 usos)
  • /assets/css/premium.css?v=30 → archivo local (0 usos)
  • /aviso-legal → archivo aviso-legal.html (0 usos)
  • /carta → archivo carta.html (0 usos)
  • /delivery → archivo delivery.html (0 usos)
  • /desayunos → archivo desayunos.html (0 usos)
  • /entre-panes → archivo entre-panes.html (0 usos)
  • /eventos → archivo eventos.html (0 usos)
  • /favicon-96x96.png → archivo local (0 usos)
  • /favicon.ico → archivo local (0 usos)
  • /favicon.svg → archivo local (0 usos)
  • /menu-del-dia → archivo menu-del-dia.html (0 usos)
  • /menu-shelby → archivo menu-shelby.html (0 usos)
  • /privacidad → archivo privacidad.html (0 usos)
  • /take-away → archivo take-away.html (0 usos)
  • apple-touch-icon.png → archivo local (0 usos)
  • assets/css/premium.css?v=30 → archivo local (0 usos)
  • favicon-96x96.png → archivo local (0 usos)
  • favicon.ico → archivo local (0 usos)
  • favicon.svg → archivo local (0 usos)

### Enlaces externos (dominios)
  • glovoapp.com: 26 usos
  • wa.me: 13 usos
  • www.aepd.es: 1 usos
  • www.facebook.com: 16 usos
  • www.google.com: 67 usos
  • www.instagram.com: 16 usos
  • www.smithersrestaurant.com: 14 usos

──────────────────────────────────────────────────────────────────────
## 3. MEZCLA DE ESTILOS ABSOLUTOS/RELATIVOS
──────────────────────────────────────────────────────────────────────
  • Enlaces absolutos (/ruta): 16
  • Enlaces relativos (ruta/../): 5

**Estilo usado para favicon/css:**

  • Archivos que usan *absolutos* (/favicon.ico, etc):
      aviso-legal.html
      privacidad.html
  • Archivos que usan *relativos* (favicon.ico, etc):
      404.html
      carta.html
      delivery.html
      desayunos.html
      entre-panes.html
      eventos.html
      index.html
      legal.html
      menu-del-dia.html
      menu-shelby.html
      reservas.html
      take-away.html

  • Inconsistencia: 2 archivos con estilo absoluto, 12 con estilo relativo.

⚠ Inconsistencia en CSS: 1 usos absolutos (/assets/css/...) vs 1 usos relativos

⚠ Otros enlaces relativos (no favicon):
   href="assets/css/premium.css?v=30" → 404.html:23

──────────────────────────────────────────────────────────────────────
## 4. IMÁGENES QUE NO EXISTEN
──────────────────────────────────────────────────────────────────────
Total src/srcset únicos: 62
  • Externas: 2
  • Locales existentes: 58
  • Locales NO ENCONTRADAS: 2

❌ IMÁGENES NO ENCONTRADAS en el sistema de archivos:
   • src="/img/facebook-icon.svg" → /home/gondss/Escritorio/KAI/pagina-web/smithers-web/img/facebook-icon.svg
       aviso-legal.html:158
       privacidad.html:200
   • src="/img/instagram-icon.svg" → /home/gondss/Escritorio/KAI/pagina-web/smithers-web/img/instagram-icon.svg
       aviso-legal.html:155
       privacidad.html:197

**Análisis:** Estos iconos SVG de redes sociales están referenciados con ruta
`/img/...` (raíz del proyecto), pero los únicos assets están bajo `assets/img/`.
La carpeta `img/` no existe en el proyecto. Estos iconos deben crearse o copiarse.


──────────────────────────────────────────────────────────────────────
## 5. CONSISTENCIA DE NAVEGACIÓN (NAV)
──────────────────────────────────────────────────────────────────────
Nav de referencia: 404.html
  Links: ['/', '/menu-del-dia', '/menu-shelby', '/carta', '/entre-panes', '/desayunos', '/take-away', '/delivery', '/eventos', 'https://www.instagram.com/smithers_restaurant/', 'https://www.facebook.com/people/Smithers-Restaurant/61588168375109/', 'https://www.google.com/maps/reserve/v/dine/c/pQjQPGMnnkc']

❌ 1 archivo(s) con nav diferente:
  • legal.html:
      FALTAN: {'https://www.google.com/maps/reserve/v/dine/c/pQjQPGMnnkc'}

⚠ El botón "Reservar" (Google Maps Reserve) falta en: ['legal.html']

──────────────────────────────────────────────────────────────────────
## 5b. NAV MÓVIL (mobile-hero-nav)
──────────────────────────────────────────────────────────────────────
Referencia: 404.html → ['/']

Total con mobile-nav: 11
Patrones encontrados: 4
  • 1 archivos: ('/',)
  • 2 archivos: ('/', '/menu-del-dia', '/menu-shelby', '/carta', '/entre-panes', '/desayunos', '/take-away', '/delivery', '/eventos', 'https://www.google.com/maps/reserve/v/dine/c/pQjQPGMnnkc')
  • 7 archivos: ('/', '/menu-del-dia', '/menu-shelby', '/carta', '/entre-panes', '/desayunos', '/take-away', '/delivery', '/eventos')
  • 1 archivos: ('/menu-del-dia', '/menu-shelby', '/carta', '/entre-panes', '/desayunos', '/take-away', '/delivery', '/eventos')

⚠ "Inicio" (/) falta en mobile-nav de: ['index.html']
⚠ Botón "Reservar" en mobile-nav falta en 9 archivos: ['404.html', 'delivery.html', 'desayunos.html', 'eventos.html', 'index.html', 'menu-del-dia.html', 'menu-shelby.html', 'reservas.html', 'take-away.html']


──────────────────────────────────────────────────────────────────────
## 6. ENLACES A PÁGINAS LEGACY
──────────────────────────────────────────────────────────────────────
⚠ **legal.html** existe como archivo separado. Contenido:
   <!doctype html>
   <html lang="es"><head>
   <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
   <meta name="geo.region" content="ES-MD">
   <meta name="geo.placename" content="Madrid">
   <meta name="geo.position" content="40.4342;-3.6321">
   <meta name="ICBM" content="40.4342, -3.6321">
   <title>Aviso legal - Smithers Restaurant Madrid</title><meta name="description" content="Aviso legal, política de privacidad y condiciones de uso de Smithers Restaurant en C/ Albasanz 16, Madrid.">
   <link rel="stylesheet" href="assets/css/premium.css?v=30">
   <meta property="og:title" content="Aviso legal - Smithers Restaurant Madrid"><meta property="og:description" content="Aviso legal, política de privacidad y condiciones de uso de Smithers Restaurant en C/ Albasanz 16, Madrid."><meta property="og:type" content="website">
   <meta property="og:image" content="https://www.smithersrestaurant.com/img/og-smithers.jpg">
   <script type="application/ld+json">
   {
   "@context": "https://schema.org",
   "@type": "Restaurant",
   "@id": "https://www.smithersrestaurant.com/#restaurant",
   "name": "Smithers Restaurant",
   "image": [
   "https://www.smithersrestaurant.com/img/og-smithers.jpg"


❌ ENLACES LEGACY AUTÉNTICOS (1):
   href="https://www.smithersrestaurant.com/legal" → /legal (legacy — ahora es /aviso-legal)
       legal.html:127

### Legacy redirects activos en _redirects:
  • /bocadillos → /entre-panes
  • /contacto → /
  • /contacto.html → /
  • /reservation → /reservas
  • /legal → /aviso-legal
  • /legal.html → /aviso-legal

──────────────────────────────────────────────────────────────────────
## RESUMEN FINAL
──────────────────────────────────────────────────────────────────────

**Total de categorías con incidencias: 5 / 7**

✅ hrefs con .html: 0
✅ Enlaces rotos (no existen como archivo/clean URL/redirect): 0
❌ Mezcla estilos (absolutos/relativos en recursos iguales): ⚠ True
❌ Imágenes no encontradas: ⚠ 2
❌ Inconsistencia navegación (nav principal): ⚠ 1
❌ Inconsistencia navegación móvil: ⚠ True
❌ Páginas legacy (legal.html existe como archivo separado): ⚠ 1
