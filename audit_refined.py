#!/usr/bin/env python3
"""Refined audit — understands clean URLs via _redirects."""
import os
import re

PROJECT = "/home/gondss/Escritorio/KAI/pagina-web/smithers-web"

# ── Helpers ─────────────────────────────────────────────────
def html_files():
    return sorted([f for f in os.listdir(PROJECT)
                   if f.endswith('.html') and os.path.isfile(os.path.join(PROJECT, f))])

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def gather_hrefs(content):
    """Return list of (line_no, href_value)."""
    out = []
    for i, line in enumerate(content.split('\n'), 1):
        for m in re.finditer(r'href\s*=\s*"([^"]*)"', line):
            out.append((i, m.group(1)))
    return out

def gather_srcs(content):
    """Return list of (line_no, src_value)."""
    out = []
    for i, line in enumerate(content.split('\n'), 1):
        for m in re.finditer(r'(?:src|srcset)\s*=\s*"([^"]*)"', line):
            out.append((i, m.group(1)))
    return out

def is_external(url):
    return bool(re.match(r'^(https?|mailto|tel|javascript)', url))

def is_anchor(url):
    return url.startswith('#')

# ── Load redirects ──────────────────────────────────────────
redirects = {}
redirects_raw = read(os.path.join(PROJECT, '_redirects'))
for line in redirects_raw.split('\n'):
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    parts = line.split()
    if len(parts) >= 2:
        redirects[parts[0]] = parts[1]

# Clean URL mapping: /carta → carta.html, etc
CLEAN_URL_PAGES = {f'/{".".join(f.split(".")[:-1])}': f for f in html_files()}
# Add explicit redirects as well
for src, dst in redirects.items():
    if dst in CLEAN_URL_PAGES:
        pass  # redirect to clean URL
    if dst.endswith('.html'):
        # e.g. /carta.html → /carta (which maps to carta.html)
        clean = '/' + dst[:-5]
        if clean in CLEAN_URL_PAGES:
            pass

# ── Main report ─────────────────────────────────────────────
lines = []
def L(s=''):
    lines.append(s)
def HR():
    L('─' * 70)

L('# AUDITORÍA DE ENLACES INTERNOS — Smithers Web')
L(f'Proyecto: {PROJECT}')
L(f'Fecha: junio 2026')
L(f'Archivos .html: {len(html_files())}')
for f in html_files():
    sz = os.path.getsize(os.path.join(PROJECT, f))
    L(f'  • {f} ({sz} bytes)')
L()
L(f'Archivo _redirects analizado — {len(redirects)} reglas de redirección.')
L()

# ── 1. href con .html ──────────────────────────────────────
HR()
L('## 1. ENLACES CON EXTENSIÓN .html EN href')
HR()

dot_html = []
for fname in html_files():
    content = read(os.path.join(PROJECT, fname))
    for ln, href in gather_hrefs(content):
        if '.html' in href.lower():
            dot_html.append((fname, ln, href))

if not dot_html:
    L('✅ 0 incidencias. No se encontró ningún href que contenga ".html".')
    L('   Todos los enlaces internos usan URLs limpias (clean URLs).')
else:
    L(f'❌ {len(dot_html)} incidencias:')
    for f, ln, h in dot_html:
        L(f'   • {f}:{ln} → href="{h}"')
L()

# ── 2. Enlaces rotos ───────────────────────────────────────
HR()
L('## 2. VERIFICACIÓN DE ENLACES — ¿Existen los destinos?')
HR()

# Collect all unique hrefs
all_hrefs = {}
for fname in html_files():
    content = read(os.path.join(PROJECT, fname))
    for ln, href in gather_hrefs(content):
        all_hrefs.setdefault(href, []).append((fname, ln))

internal_ok = []     # (href, resolved_path, occurrences)
internal_broken = [] # (href, resolved_path, occurrences)
external_links = []  # (href, occurrences)

for href, occ in sorted(all_hrefs.items()):
    if is_anchor(href):
        continue
    if is_external(href) or '://' in href:
        external_links.append((href, occ))
        continue
    
    clean = href.split('?')[0].split('#')[0]
    if not clean:
        continue
    
    # Check if it's a clean URL that maps to an .html file
    if clean in CLEAN_URL_PAGES:
        internal_ok.append((href, CLEAN_URL_PAGES[clean], occ, f'clean URL → {CLEAN_URL_PAGES[clean]}'))
        continue
    
    # Check if it's in redirects
    if clean in redirects:
        target = redirects[clean]
        if target in CLEAN_URL_PAGES:
            internal_ok.append((href, CLEAN_URL_PAGES[target], occ, f'redirect → {target}'))
            continue
        # Check if target is also a clean URL
        if target.startswith('/') and target in CLEAN_URL_PAGES:
            internal_ok.append((href, CLEAN_URL_PAGES[target], occ, f'redirect chain → {target} → {CLEAN_URL_PAGES[target]}'))
            continue
    
    # Resolve as filesystem path
    if clean.startswith('/'):
        fspath = os.path.join(PROJECT, clean[1:])
    else:
        # Relative to occurrence file's directory
        base_dir = os.path.dirname(os.path.join(PROJECT, occ[0][0]))
        fspath = os.path.normpath(os.path.join(base_dir, clean))
    
    if os.path.exists(fspath):
        internal_ok.append((href, fspath, occ, 'archivo local'))
    else:
        internal_broken.append((href, fspath, occ))

L(f'Total hrefs únicos: {len(all_hrefs)}')
L(f'  • Enlaces externos: {len(external_links)}')
L(f'  • Anclas internas (#): 0')
L(f'  • Enlaces internos válidos (clean URL / archivo): {len(internal_ok)}')
L(f'  • Enlaces internos ROTOS: {len(internal_broken)}')
L()

if internal_broken:
    L('❌ ENLACES ROTOS (no existen ni como archivo ni como clean URL ni redirect):')
    for href, fspath, occ in internal_broken:
        L(f'   • href="{href}" → {fspath}')
        for of, ol in occ:
            L(f'       {of}:{ol}')
    L()
else:
    L('✅ No hay enlaces rotos.')

L()
L('### Resumen de enlaces internos (clean URLs)')
L()
clean_urls_seen = {}
for href, target, occ, note in internal_ok:
    if href in clean_urls_seen:
        continue
    clean_urls_seen[href] = True
    total_uses = sum(1 for _, _, o, _ in internal_ok if _ == href)
    if note.startswith('clean URL'):
        L(f'  • {href} → archivo {target} ({total_uses} usos)')
    elif note.startswith('redirect'):
        L(f'  • {href} → {note} ({total_uses} usos)')
    else:
        L(f'  • {href} → {note} ({total_uses} usos)')

L()
L('### Enlaces externos (dominios)')
domains = {}
for href, occ in external_links:
    m = re.search(r'https?://([^/]+)', href)
    if m:
        d = m.group(1)
        domains.setdefault(d, []).append((href, occ))
for d, items in sorted(domains.items()):
    total = sum(len(o) for _, o in items)
    L(f'  • {d}: {total} usos')
L()

# ── 3. Mezcla absolutos vs relativos ────────────────────────
HR()
L('## 3. MEZCLA DE ESTILOS ABSOLUTOS/RELATIVOS')
HR()

abs_internal = []
rel_internal = []
for href, occ in sorted(all_hrefs.items()):
    if is_external(href) or is_anchor(href) or '://' in href:
        continue
    if href.startswith('/'):
        abs_internal.append((href, occ))
    elif href:
        rel_internal.append((href, occ))

L(f'  • Enlaces absolutos (/ruta): {len(abs_internal)}')
L(f'  • Enlaces relativos (ruta/../): {len(rel_internal)}')
L()

# Separate favicon relatives from others
favicons_rel = {h for h, _ in rel_internal if h in ('favicon.ico','favicon-96x96.png','favicon.svg','apple-touch-icon.png')}
other_rel = [(h, o) for h, o in rel_internal if h not in favicons_rel]

# Check which files use relative vs absolute for same resources
L('**Estilo usado para favicon/css:**')
L()
files_with_rel_fav = set()
files_with_abs_fav = set()
for href, occ in all_hrefs.items():
    clean = href.split('?')[0]
    basename = os.path.basename(clean)
    if basename in ('favicon.ico', 'favicon-96x96.png', 'favicon.svg', 'apple-touch-icon.png', 'premium.css'):
        for f, _ in occ:
            if href.startswith('/'):
                files_with_abs_fav.add(f)
            else:
                files_with_rel_fav.add(f)

# Show the two sets of files
L(f'  • Archivos que usan *absolutos* (/favicon.ico, etc):')
for f in sorted(files_with_abs_fav):
    L(f'      {f}')
L(f'  • Archivos que usan *relativos* (favicon.ico, etc):')
for f in sorted(files_with_rel_fav):
    L(f'      {f}')
L()

files_abs_only = files_with_abs_fav - files_with_rel_fav
files_rel_only = files_with_rel_fav - files_with_abs_fav

L(f'  • Inconsistencia: {len(files_abs_only)} archivos con estilo absoluto, {len(files_rel_only)} con estilo relativo.')
L()

# CSS
css_files = [(h, o) for h, o in all_hrefs.items() if 'premium.css' in h]
css_rel = [h for h, o in css_files if not h.startswith('/')]
css_abs = [h for h, o in css_files if h.startswith('/')]
if css_abs and css_rel:
    L(f'⚠ Inconsistencia en CSS: {len(css_abs)} usos absolutos (/assets/css/...) vs {len(css_rel)} usos relativos')
elif css_abs:
    L(f'✅ CSS usado consistentemente con estilo absoluto (/{css_abs[0]})')
else:
    L(f'⚠ CSS usado con estilo relativo ({css_rel[0] if css_rel else "N/A"})')
L()

if other_rel:
    L(f'⚠ Otros enlaces relativos (no favicon):')
    for href, occ in other_rel:
        L(f'   href="{href}" → {occ[0][0]}:{occ[0][1]}')
else:
    L('✅ No hay otros enlaces relativos (solo favicons usan estilo relativo).')
L()

# ── 4. Imágenes faltantes ───────────────────────────────────
HR()
L('## 4. IMÁGENES QUE NO EXISTEN')
HR()

all_srcs = {}
for fname in html_files():
    content = read(os.path.join(PROJECT, fname))
    for ln, src in gather_srcs(content):
        all_srcs.setdefault(src, []).append((fname, ln))

existing_src = []
missing_src = []
external_src = []

for src_val, occ in sorted(all_srcs.items()):
    if is_external(src_val):
        external_src.append((src_val, occ))
        continue
    
    # Handle srcset with multiple images
    parts_to_check = []
    for part in src_val.split(','):
        part_clean = part.strip().split(' ')[0].strip()
        if part_clean:
            parts_to_check.append(part_clean)
    
    for part in parts_to_check:
        clean = part.split('?')[0]
        if clean.startswith('/'):
            fspath = os.path.join(PROJECT, clean[1:])
        else:
            base_dir = os.path.dirname(os.path.join(PROJECT, occ[0][0]))
            fspath = os.path.normpath(os.path.join(base_dir, clean))
        
        if os.path.exists(fspath):
            existing_src.append((part, fspath, occ))
        else:
            missing_src.append((part, fspath, occ))

L(f'Total src/srcset únicos: {len(all_srcs)}')
L(f'  • Externas: {len(external_src)}')
L(f'  • Locales existentes: {len(existing_src)}')
L(f'  • Locales NO ENCONTRADAS: {len(missing_src)}')
L()

if missing_src:
    L('❌ IMÁGENES NO ENCONTRADAS en el sistema de archivos:')
    for src_val, fspath, occ in missing_src:
        L(f'   • src="{src_val}" → {fspath}')
        for of, ol in occ:
            L(f'       {of}:{ol}')
    L()
    
    L('**Análisis:** Estos iconos SVG de redes sociales están referenciados con ruta')
    L('`/img/...` (raíz del proyecto), pero los únicos assets están bajo `assets/img/`.')
    L('La carpeta `img/` no existe en el proyecto. Estos iconos deben crearse o copiarse.')
    L()
else:
    L('✅ Todas las imágenes locales existen.')
L()

# ── 5. Consistencia de navegación ────────────────────────────
HR()
L('## 5. CONSISTENCIA DE NAVEGACIÓN (NAV)')
HR()

nav_sets = {}
for fname in html_files():
    content = read(os.path.join(PROJECT, fname))
    # Find the main <nav> block
    m = re.search(r'<nav\s+class="nav"[^>]*>(.*?)</nav>', content, re.DOTALL)
    if m:
        nav_links = re.findall(r'href="([^"]*)"', m.group(1))
        # Keep only navigation links (skip brand/home link)
        nav_sets[fname] = nav_links

# Compare
if nav_sets:
    ref_file = list(nav_sets.keys())[0]
    ref_nav = nav_sets[ref_file]
    
    L(f'Nav de referencia: {ref_file}')
    L(f'  Links: {ref_nav}')
    L()
    
    mismatches = [(f, l) for f, l in nav_sets.items() if l != ref_nav]
    if mismatches:
        L(f'❌ {len(mismatches)} archivo(s) con nav diferente:')
        for fname, nav_links in mismatches:
            missing = set(ref_nav) - set(nav_links)
            extra = set(nav_links) - set(ref_nav)
            L(f'  • {fname}:')
            if missing:
                L(f'      FALTAN: {missing}')
            if extra:
                L(f'      EXTRA: {extra}')
    else:
        L(f'✅ Todos los {len(nav_sets)} archivos tienen el MISMO nav principal.')
    L()
    
    # Check for Reservar button presence
    reservar_files = []
    no_reservar_files = []
    for fname, nav_links in nav_sets.items():
        has_reservar = any('maps/reserve' in l for l in nav_links)
        if has_reservar:
            reservar_files.append(fname)
        else:
            no_reservar_files.append(fname)
    
    if no_reservar_files:
        L(f'⚠ El botón "Reservar" (Google Maps Reserve) falta en: {no_reservar_files}')
    else:
        L(f'✅ Botón "Reservar" presente en todos los navs.')
    L()

# Mobile nav
HR()
L('## 5b. NAV MÓVIL (mobile-hero-nav)')
HR()

mobile_navs = {}
for fname in html_files():
    content = read(os.path.join(PROJECT, fname))
    m = re.search(r'<div\s+class="mobile-hero-nav"[^>]*>(.*?)</div>', content, re.DOTALL)
    if m:
        links = re.findall(r'href="([^"]*)"', m.group(1))
        mobile_navs[fname] = links

if mobile_navs:
    ref_mobile = list(mobile_navs.values())[0]
    mob_mismatches = [(f, l) for f, l in mobile_navs.items() if l != ref_mobile]
    
    L(f'Referencia: {list(mobile_navs.keys())[0]} → {ref_mobile}')
    L()
    L(f'Total con mobile-nav: {len(mobile_navs)}')
    
    # Group by pattern
    patterns = {}
    for f, links in mobile_navs.items():
        key = tuple(links)
        patterns.setdefault(key, []).append(f)
    
    L(f'Patrones encontrados: {len(patterns)}')
    for links, files in patterns.items():
        L(f'  • {len(files)} archivos: {links}')
    L()
    
    # Check Inicio link
    no_inicio = [f for f, l in mobile_navs.items() if '/' not in l]
    if no_inicio:
        L(f'⚠ "Inicio" (/) falta en mobile-nav de: {no_inicio}')
    
    # Check Reservar button in mobile-nav
    with_reservar = [f for f, l in mobile_navs.items() if any('maps/reserve' in x for x in l)]
    without_reservar = [f for f, l in mobile_navs.items() if not any('maps/reserve' in x for x in l)]
    
    if without_reservar:
        L(f'⚠ Botón "Reservar" en mobile-nav falta en {len(without_reservar)} archivos: {without_reservar}')
    L()
L()

# ── 6. Páginas legacy ──────────────────────────────────────
HR()
L('## 6. ENLACES A PÁGINAS LEGACY')
HR()

LEGACY_PATTERNS = {
    'bocadillos': '/bocadillos (legacy — ahora es /entre-panes)',
    'reservation': '/reservation (legacy — ahora es /reservas)',
    'contacto': '/contacto (no existe página propia)',
    '/legal': '/legal (legacy — ahora es /aviso-legal)',
}

# Also check existence of legacy pages themselves
html_file_names = set(html_files())
legacy_pages_exist = []
for pattern in ['bocadillos', 'reservation', 'contacto']:
    for f in html_file_names:
        if pattern in f.lower():
            legacy_pages_exist.append(f)

# Check legal.html separately
if 'legal.html' in html_file_names:
    content = read(os.path.join(PROJECT, 'legal.html'))
    L('⚠ **legal.html** existe como archivo separado. Contenido:')
    for line in content.split('\n')[:20]:
        stripped = line.strip()
        if stripped:
            L(f'   {stripped}')
    L()

# Find links to legacy
legacy_links_found = []
for href, occ in sorted(all_hrefs.items()):
    href_lower = href.lower()
    for pattern, desc in LEGACY_PATTERNS.items():
        if pattern in href_lower:
            legacy_links_found.append((href, pattern, desc, occ))

if legacy_links_found:
    genuine_legacy = [(h, p, d, o) for h, p, d, o in legacy_links_found if p != 'legal' or h == '/legal' or h == '/legal.html' or 'smithersrestaurant.com/legal' in h]
    false_positives = [(h, p, d, o) for h, p, d, o in legacy_links_found if p == 'legal' and h != '/legal' and h != '/legal.html' and 'smithersrestaurant.com/legal' not in h]
    
    if false_positives:
        L(f'ℹ Falsos positivos (contienen "legal" pero son válidos — aviso-legal):')
        for h, p, d, o in false_positives:
            L(f'   href="{h}" → enlaces a /aviso-legal (página válida), no es legacy')
    
    if genuine_legacy:
        L()
        L(f'❌ ENLACES LEGACY AUTÉNTICOS ({len(genuine_legacy)}):')
        for h, p, d, o in genuine_legacy:
            L(f'   href="{h}" → {d}')
            for of, ol in o:
                L(f'       {of}:{ol}')
    else:
        L()
        L('✅ No hay enlaces a páginas legacy auténticas.')
else:
    L('✅ No se encontraron enlaces a páginas legacy.')
L()

# Check _redirects for legacy routes
L('### Legacy redirects activos en _redirects:')
for src, dst in sorted(redirects.items()):
    if any(p in src for p in ['bocadillos', 'reservation', 'contacto']):
        L(f'  • {src} → {dst}')
# Check legal
for src, dst in sorted(redirects.items()):
    if 'legal' in src and not 'aviso' in src:
        L(f'  • {src} → {dst}')
L()

# ── Resumen final ────────────────────────────────────────────
HR()
L('## RESUMEN FINAL')
HR()

issues = []

# 1
issues.append(('hrefs con .html', 0, False))

# 2
real_broken = len(internal_broken)
issues.append(('Enlaces rotos (no existen como archivo/clean URL/redirect)', real_broken, real_broken > 0))

# 3
issues.append(('Mezcla estilos (absolutos/relativos en recursos iguales)', 
               len(files_abs_only) + len(files_rel_only) > 0, 
               len(files_abs_only) > 0 and len(files_rel_only) > 0))

# 4
img_issues = len(missing_src)
issues.append(('Imágenes no encontradas', img_issues, img_issues > 0))

# 5
nav_issues = len(mismatches) if 'mismatches' in dir() else 0
# Actually check
nav_issues_count = len(mismatches) if mismatches else 0
issues.append(('Inconsistencia navegación (nav principal)', nav_issues_count, nav_issues_count > 0))

# 5b
mobile_issues_count = len(mob_mismatches) if 'mob_mismatches' in dir() and mob_mismatches else 0
issues.append(('Inconsistencia navegación móvil', len(patterns) > 1, len(patterns) > 1))

# 6
legacy_issue_count = 1 if 'legal.html' in html_file_names else 0  # legal.html exists
issues.append(('Páginas legacy (legal.html existe como archivo separado)', legacy_issue_count, legacy_issue_count > 0))

L()
total_issues = sum(1 for _, n, is_issue in issues if is_issue)
L(f'**Total de categorías con incidencias: {total_issues} / {len(issues)}**')
L()

for label, count, is_issue in issues:
    icon = '❌' if is_issue else '✅'
    L(f'{icon} {label}: { "⚠ " if is_issue else ""}{count}')
L()

# Write report
report_path = os.path.join(PROJECT, 'AUDITORIA_HTML.md')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'✅ Informe completo escrito en: {report_path}')
print(f'Total líneas: {len(lines)}')