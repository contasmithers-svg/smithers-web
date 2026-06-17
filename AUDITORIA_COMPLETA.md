# 🏆 AUDITORÍA EXHAUSTIVA — Smithers Restaurant Web
**Fecha:** 17 junio 2026 | **Proyecto:** /home/gondss/Escritorio/KAI/pagina-web/smithers-web/
**Páginas:** 14 HTML · 1 CSS · 2 JS | **Dominio:** www.smithersrestaurant.com

---

## 🔴 CRÍTICOS (hay que arreglar YA)

| # | Incidencia | Localización | Solución |
|:-:|:-----------|:-------------|:---------|
| 1 | **legal.html**: BreadcrumbList en JSON-LD apunta a `/privacidad` en vez de `/legal` (copypaste) | legal.html (schema JSON-LD) | Cambiar `"item": {"@id": ".../privacidad"}` por `".../legal"` |
| 2 | **2 SVGs rotos**: `img/facebook-icon.svg` e `img/instagram-icon.svg` no existen | privacidad.html, aviso-legal.html (footer) | Crear los SVG o borrar referencias |
| 3 | **Sin estilos de focus visible** — usuarios de teclado no ven dónde están | premium.css | Añadir `a:focus-visible{outline:2px solid #c8a45c}` |

## 🟡 ALTOS

| # | Incidencia | Localización | Solución |
|:-:|:-----------|:-------------|:---------|
| 4 | **Falta `<main>`** en 12/14 páginas — landmark principal ausente | Todas excepto privacidad.html y aviso-legal.html | Envolver contenido principal en `<main id="main">` |
| 5 | **Sin skip-navigation** — imposible saltar nav con teclado/lector | Todas las páginas | Añadir `<a href="#main" class="skip-link">Saltar al contenido</a>` |
| 6 | **Sin `width`/`height` en imágenes** — causa CLS (Layout Shift) en todas las páginas | Todas las páginas con imágenes | Añadir width/height a cada `<img>` |
| 7 | **Iconos sociales SVG sin `aria-hidden="true"`** — se leen como basura | Nav de todas las páginas | Añadir `aria-hidden="true"` a los SVGs |
| 8 | **Meta descripción no coincide con OG description** en 3 páginas | take-away.html, reservas.html, delivery.html | Unificar meta description y og:description |
| 9 | **legal.html** es página duplicada con contenido placeholder y sin botón Reservar | legal.html | Eliminar archivo (ya redirige /legal → /aviso-legal) |

## 🟠 MEDIOS

| # | Incidencia | Localización | Solución |
|:-:|:-----------|:-------------|:---------|
| 10 | **Contraste insuficiente**: texto `#888`(13px) sobre fondo crema en footer | Todas (footer) | Cambiar a `#666` o más oscuro |
| 11 | **Touch targets borderline**: botones móvil inferior ~38px (mín 44px) | mobile-actions en todas | Aumentar padding |
| 12 | **cookies.js (13KB)** en `<head>` con defer — mejor moverlo antes de `</body>` | Todas las páginas | Mover script al final del body |
| 13 | **Logo PNG de 58KB** innecesariamente grande para 48×48px | assets/img/ | Comprimir a ~10KB |
| 14 | **Nav móvil inconsistente**: index.html sin enlace a Inicio; solo 2/11 tienen botón Reservar | mobile-hero-nav en varias | Unificar criterio |
| 15 | **`index.html`** sin `@id` en el bloque Restaurant del schema JSON-LD | index.html (JSON-LD) | Añadir `"@id": "https://www.smithersrestaurant.com"` |

## 🟢 BAJOS

| # | Incidencia | Localización | Solución |
|:-:|:-----------|:-------------|:---------|
| 16 | **Rutas absolutas vs relativas** inconsistentes en favicon/CSS | aviso-legal.html, privacidad.html | Unificar estilo con el resto |
| 17 | **Soft 404**: `/404` devuelve 200 (página con contenido) | 404.html en producción | No es error si es intencionado |
| 18 | **JPEGs originales pesados** (150-289KB) que tienen WebP alternativo | assets/img/ | Considerar eliminar JPEGs si WebP tiene soporte suficiente |
| 19 | **Contraste justo**: `.muted` (#695c50) sobre crema (#fff6e6) — roza el límite AA | Varias páginas | Oscurecer ligeramente |

---

## ✅ LO QUE ESTÁ PERFECTO (sin cambios necesarios)

| Categoría | Detalle |
|:----------|:--------|
| 🚀 **Redirects** | Page Rule www activa + _redirects con 18 reglas correctas, sin bucles |
| 🗺️ **Sitemap** | 12 URLs, bien formado, sin .html, prioridades correctas |
| 🤖 **robots.txt** | Bloques crawlers agresivos, permite buscadores y crawlers IA, apunta al sitemap |
| 🔍 **Canonicals** | Todas las páginas con canonical correcto (www, sin .html) |
| 📝 **Titles** | Todos < 60 caracteres |
| 📄 **Meta descriptions** | Todas < 160 caracteres |
| 🏗️ **JSON-LD** | Válido en todas, sin URLs .html, Restaurant schema completo con hasMenu |
| 🖼️ **Alt text** | Todas las imágenes con alt descriptivo |
| 📐 **Heading hierarchy** | h1→h2→h3 correcta en todas las páginas |
| 🌐 **lang="es"** | Correcto en todas |
| 📱 **Viewport** | Configurado en todas |
| 🔤 **Charset** | UTF-8 en todas |
| 🎨 **Favicon** | 5 formatos, correctamente enlazado |
| 🔒 **HSTS** | max-age=31536000; includeSubDomains; preload |
| 🛡️ **X-Frame-Options** | DENY en todas |
| 📊 **Open Graph** | 5 tags obligatorios en todas las páginas |
| 📦 **Scripts** | Todos con async/defer, sin bloqueantes |
| 🎯 **Sin enlaces .html** | 0 hrefs con .html (auditoría de 14 archivos) |
| ✅ **Sin .html en JSON-LD** | 0 ocurrencias en schema |
| 🔗 **Teléfono/WhatsApp** | Correctos y consistentes en todas las páginas |

---

## 📊 MÉTRICAS DE LA WEB

| Métrica | Valor |
|:--------|:-----|
| Total de archivos | ~134 (14 HTML, 1 CSS, 2 JS, 110 imágenes, 5 favicon, 1 OG) |
| Peso total proyecto | ~15.6 MB |
| Peso por página (media) | 320-890 KB (con imágenes) / 67-81 KB (sin imágenes) |
| Media queries | 1 breakpoint (930px) |
| CSS único | premium.css (13KB, versionado ?v=30) |
| Sin Google Fonts | ✅ — cero bloqueo por fuentes externas |
| WebP prioritario | ✅ — todas las imágenes con `<picture>` y source WebP |
| Lazy loading | ✅ — en todas las imágenes excepto hero |

---

## 🔧 ACCIONES RECOMENDADAS (por orden de prioridad)

### 🔥 Urgente (hacer ahora)
1. Corregir BreadcrumbList en legal.html (apunta a /privacidad)
2. Crear los 2 SVGs de iconos sociales o eliminarlos
3. Añadir estilos de focus visible

### 📋 Planificado (próximo deploy)
4. Envolver contenido en `<main>` en las 12 páginas que faltan
5. Añadir skip-navigation link
6. Añadir width/height a todas las imágenes (eliminar CLS)
7. Añadir aria-hidden a iconos SVG
8. Unificar meta/og:description en take-away, reservas, delivery
9. Eliminar legal.html (ya redirige)

### 🧹 Mejora continua
10. Mejorar contraste footer (#888→#666)
11. Aumentar touch targets en mobile-actions
12. Mover cookies.js al final del body
13. Comprimir PNG del logo
14. Unificar nav móvil (Inicio + Reservar en todas)
15. Añadir @id al schema de index.html