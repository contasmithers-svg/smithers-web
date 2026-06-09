# REGISTRO DE VERSIONES — Smithers Web

## Estado actual
**Fecha:** 30/05/2026 (tarde)
**CSS v=28** en todos los HTML (12 páginas)
**Túnel activo:** https://olive-grapes-heal.loca.lt (puerto 8082)
**Servidores:** 8080 y 8082 → mismo directorio correcto

## Páginas HTML (12)
| Archivo | Tamaño | CSS v | Schemas |
|---------|--------|-------|---------|
| index.html | 16.915 B | v=28 | Restaurant + FAQPage + BreadcrumbList ✅ |
| menu-del-dia.html | 20.968 B | v=28 | Restaurant + BreadcrumbList ✅ |
| menu-shelby.html | 16.145 B | v=28 | Restaurant + BreadcrumbList ✅ |
| desayunos.html | 25.627 B | v=28 | Restaurant + BreadcrumbList ✅ |
| carta.html | 25.574 B | v=28 | Restaurant + BreadcrumbList ✅ |
| delivery.html | 13.530 B | v=28 | Restaurant + BreadcrumbList ✅ |
| take-away.html | 16.215 B | v=28 | Restaurant + BreadcrumbList ✅ |
| eventos.html | 12.845 B | v=28 | Event + Restaurant + BreadcrumbList ✅ |
| reservas.html | 15.677 B | v=28 | Restaurant + BreadcrumbList ✅ |
| aviso-legal.html | 8.779 B | v=28 | BreadcrumbList ✅ |
| legal.html | 10.689 B | v=28 | Restaurant + BreadcrumbList ✅ |
| privacidad.html | 11.035 B | v=28 | BreadcrumbList ✅ |

## Archivos clave
- **CSS:** assets/css/premium.css (24 líneas, v=28)
- **JS:** assets/js/premium.js
- **Cookies:** cookies.js (funcional con 3 categorías)
- **Robots:** robots.txt
- **Sitemap:** sitemap.xml
- **Favicon:** favicon.ico + .svg + tamaños 16/32/96 + apple-touch-icon

## Imágenes
- **Carta:** 35 fotos en assets/img/carta/
- **Desayunos:** 7 fotos en assets/img/desayunos/
- **Shelby:** 6 fotos en assets/img/shelby/ (SHELBY_COSTILLAS, SHELBY_AGUJA, SHELBY_POLLO, SHELBY_SECRETO, SHELBY_WOK, SHELBY_TERIYAKI)
- **Postres:** 5 fotos en assets/img/postres/
- **Hero:** hero-smithers.jpg (interior restaurante con comensales)
- **Cocina delivery:** cocina-delivery.jpg
- **Menú del día mesa:** menu-del-dia-mesa.jpg
- **Eventos networking:** eventos-networking.jpg
- **Logo:** logo-smithers.png

## Lo corregido en esta sesión (30/05 tarde)
- **🔴 Teléfono JSON-LD en index.html:** Tenía asteriscos literales (`+349****9622`) en vez del número real, debido a error de copia al editar el Schema. Corregido a `+34 911 699 622`. ✅
- **🟠 Errata "cockteles":** Tarjeta de Eventos en index.html ponía "cockteles" → "cócteles". ✅
- **🟠 Logo apunta a /:** Todos los enlaces `class="brand" href="index.html"` cambiados a `class="brand" href="/"` (10 archivos HTML). ✅
- **Validación:** Verificado en túnel — JSON-LD de index.html muestra `telephone: +34 911 699 622`, brand link apunta a `/`, no hay "cockteles". ✅
- **Auditoría Opus:** Opus confirmó que estructura y contenido sólidos. Pendiente subir a producción (robots.txt, sitemap.xml, PageSpeed Insights, aggregateRating opcional).

## Lo nuevo en esta sesión (02/06/2026)
- **🚀 Despliegue en producción con Cloudflare Pages:** Sitio subido y publicado en `smithers-restaurant.pages.dev` (primer despliegue)
- **🌐 Dominio personalizado:** `smithersrestaurant.com` conectado a Cloudflare Pages ✅
- **📡 DNS migrado de Wix a Cloudflare:** Nameservers cambiados en GoDaddy → `april.ns.cloudflare.com` / `coleman.ns.cloudflare.com`
- **🔐 SSL/HTTPS:** Certificado automático de Cloudflare activo ✅
- **📋 Subdominio www:** `www.smithersrestaurant.com` añadido como custom domain en Pages ✅
- **🧹 DNS limpiado:** Registros A de Wix (185.230.63.xxx) eliminados; CNAME www actualizado de `cdn1.wixdns.net` a `smithers-restaurant.pages.dev`
- **🗑️ Caché purgada:** Cloudflare cache purgado globalmente
- **Estado actual:** Web en producción, accesible vía `https://smithersrestaurant.com` y `https://smithers-restaurant.pages.dev`
- **Para cambios futuros:** modificar archivos, empaquetar en zip, subir a Cloudflare Pages dashboard → nuevo deployment

## 🔥 Cambios SEO — 04/06/2026
- **✅ Google Search Console:** Propiedad `smithersrestaurant.com` verificada vía TXT DNS en Cloudflare
- **✅ Cobertura:** Issues identificados (3 indexadas, 10 noindex, 6 404, 4 redirect, 1 canonical alt, 3 discovered) y corregidos
- **✅ Canónicas limpias:** Todas las canonical URLs sin `.html` (13 páginas)
- **✅ Sitemap reescrito:** 13 URLs limpias con prioridades y changefreq
- **✅ Validate Fix:** Solicitado en Search Console para los 6 issue types
- **✅ Sitemap subido:** `sitemap.xml` con URLs limpias en Search Console
- **✅ WebP:** 60 imágenes JPG/PNG → WebP (-48% peso). Todas con `<picture>` + fallback
- **✅ Horario finde:** "Cerrado sábados, domingos y festivos" en textos visibles y FAQ
- **✅ CID Google Maps real:** `17847721193954781420` en Schema sameAs (11 páginas)
- **✅ Commits:** `65d5912` (seo), `6b19fed` (canónicas+sitemap), `9c53b3d` (horario), `8fc1bec` (CID)
- **📦 Backups creados:** `smithers-web-BACKUP_20260604_114522` + `smithers-web-BACKUP_20260604_162525`

## Cambios sesión 05/06/2026 — Auditoría SEO + Landing empresas (revertida)

- **✅ Redirects 301:** `/bocadillos` → `/entre-panes` y `/reservation` → `/reservas` mediante `_redirects`
- **✅ Cloudflare ajustado:** robots.txt OFF, Bot Fight Mode OFF, Block AI Bots = "Do not block"
- **✅ Eventos.html mejorado:** sección "Así se viven los eventos" con galería + testimonios + info catering
- **❌ Landing empresas:** creada, añadida a nav/schema/sitemap, pero el usuario la rechazó — revertido todo
- **Commits:** `6a5e838` (landing + cambios), `4a3fef4` (reversión empresas)
- **Backup:** `smithers-web-BACKUP_20260605_152838`

## BACKUPS DISPONIBLES (orden cronológico inverso)

### NUEVO — 20260604_235148
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260604_235148`
**Contiene:** v=28, tras SEO completo. Search Console ✅, canónicas limpias, sitemap reescrito, WebP 60 imágenes (-48%), horario finde cerrado, CID Maps real en sameAs (11 páginas). Commit `8fc1bec`.
**Para restaurar:** `cp -a smithers-web-BACKUP_20260604_235148/* smithers-web/`

### 7. NUEVO — 20260604_162525
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260604_162525`
**Contiene:** v=28, tras añadir CID de Google Maps (IA Session).
**Para restaurar:** `cp -a smithers-web-BACKUP_20260604_162525/* smithers-web/`

### 8. NUEVO — 20260604_114522
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260604_114522`
**Contiene:** v=28, justo antes de comenzar sesión SEO — Search Console sin verificar.
**Para restaurar:** `cp -a smithers-web-BACKUP_20260604_114522/* smithers-web/`

### NUEVO — 20260602_113143
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260602_113143`
**Contiene:** v=28, estado post-despliegue Cloudflare Pages. Sitio desplegado en producción con dominio smithersrestaurant.com y www. DNS migrado de Wix a Cloudflare. Certificado SSL activo. Sin cambios en el contenido web — solo cambios de infraestructura (DNS, Cloudflare Pages, nombreservers).
**Para restaurar:** `cp -a smithers-web-BACKUP_20260602_113143/* smithers-web/`

### 1. NUEVO — 20260601_111814
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260601_111814`
**Contiene:** v=28, sin cambios en la web — sesión dedicada a cambio de email de automatización (smithers.claude → conta.smithers) en scripts Gmail, skills y documentación. Pendiente: autorización OAuth manual y cambio de email en GBP.
**Para restaurar:** `cp -a smithers-web-BACKUP_20260601_111814/* smithers-web/`

### 2. NUEVO — 20260601_101641
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260601_101641`
**Contiene:** v=28, sin cambios respecto al backup anterior — SAVE de transición tras cambio de proyecto.
**Para restaurar:** `cp -a smithers-web-BACKUP_20260601_101641/* smithers-web/`

### 2. NUEVO — 20260530_084726
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260530_084726`
**Contiene:** v=28, JSON-LD completo en todas las páginas, teléfono JSON-LD index.html corregido, typo cockteles→cócteles, brand href="/", foto eventos-networking.jpg, OrderAction en delivery/take-away, servidores 8080+8082, túnel activo.
**Para restaurar:** `cp -a smithers-web-BACKUP_20260530_084726/* smithers-web/`

### 2. ANTERIOR — 20260530_081922
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260530_081922`
**Contiene:** v=28, JSON-LD completo en todas las páginas, foto eventos-networking.jpg, typo siracha corregido, OrderAction en delivery/take-away, servidores 8080+8082, túnel activo.
**Para restaurar:** `cp -a smithers-web-BACKUP_20260530_081922/* smithers-web/`

### 3. ANTERIOR — 20260527_161057
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260527_161057`
**Contiene:** v=28, fotos nuevas (hero interior restaurante, cocina delivery, mesa menú del día), espacios ajustados en delivery y menu-del-día, servidores 8080+8082, túnel activo.
**Para restaurar:** `cp -a smithers-web-BACKUP_20260527_161057/* smithers-web/`

### 4. ANTERIOR — 20260526_170352
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260526_170352`
**Contiene:** v=28, estado tras SAVE anterior — servidores activos 8080+8082, túnel olive-grapes-heal.loca.lt operativo, CSS uniforme v=28 en 12 HTML.
**Para restaurar:** `cp -a smithers-web-BACKUP_20260526_170352/* smithers-web/`

### 5. 20260526_113931
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260526_113931`
**Contiene:** v=28, hero en móvil foto+texto separados, cards reordenadas (M. del día, M. Shelby, Take away, Desayunos, Eventos), teléfono corregido en HTML, todo el proyecto al completo.
**Para restaurar:** `cp -a smithers-web-BACKUP_20260526_113931/* smithers-web/`

### 6. 20260525_234602
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP_20260525_234602`
**Contiene:** v=25, overflows corregidos, todo el proyecto al completo.

### 7. MOVIL-ANTES
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP-MOVIL-ANTES`
**Contiene:** Estado justo antes de las correcciones de overflow en móvil.

### 8. SEOCORREGIDO-26MAY
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP-SEOCORREGIDO-26MAY`
**Contiene:** Versión con SEO aplicado (canonical, OG, Schema, GA4, sitemap).

### 9. ANTES-SONNET
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP-ANTES-SONNET`
**Contiene:** Estado antes de fusionar cambios de Sonnet.

### 10. PC-FINAL (en el proyecto)
**Ruta:** `/home/gondss/Escritorio/KAI/pagina-web/smithers-web-BACKUP-PC-FINAL`
**Contiene:** Versión aprobada del 25/05/2026 con atún en carta.

### 11. PC-FINAL (en el escritorio)
**Ruta:** `/home/gondss/Escritorio/smithers-web-BACKUP-PC-FINAL`
**Contiene:** Misma versión que el anterior, copia de seguridad extra.
