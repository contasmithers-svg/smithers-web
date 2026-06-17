#!/usr/bin/env python3
"""Scans all HTML files in the project and produces a comprehensive link audit."""
import os
import re
import sys

PROJECT = "/home/gondss/Escritorio/KAI/pagina-web/smithers-web"
HTML_PATTERN = re.compile(r'\.html$', re.I)

def get_html_files():
    files = []
    for f in os.listdir(PROJECT):
        if HTML_PATTERN.search(f) and os.path.isfile(os.path.join(PROJECT, f)):
            files.append(f)
    return sorted(files)

def extract_hrefs_and_srcs(filepath):
    """Return (hrefs_with_lines, srcs_with_lines) for the file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    hrefs = []  # (line_no, href_value)
    srcs = []   # (line_no, src_value)
    
    for i, line in enumerate(lines, 1):
        # Find all href="..." — be careful not to match inside <script>
        for m in re.finditer(r'href\s*=\s*"([^"]*)"', line):
            hrefs.append((i, m.group(1)))
        # Find all src="..."
        for m in re.finditer(r'src\s*=\s*"([^"]*)"', line):
            srcs.append((i, m.group(1)))
        # Also srcset
        for m in re.finditer(r'srcset\s*=\s*"([^"]*)"', line):
            srcs.append((i, m.group(1)))
    
    return hrefs, srcs

def is_external(url):
    return bool(re.match(r'^(https?|mailto|tel|javascript|#)', url))

def is_anchor(url):
    return url.startswith('#')

def resolve_path(url, base_file):
    """Try to resolve a relative URL to an absolute filesystem path."""
    if is_external(url) or is_anchor(url):
        return None
    # Clean query strings
    clean = url.split('?')[0].split('#')[0]
    if not clean:
        return None
    if clean.startswith('/'):
        # Absolute from web root
        return os.path.join(PROJECT, clean.lstrip('/'))
    else:
        # Relative to the HTML file's directory
        base_dir = os.path.dirname(os.path.join(PROJECT, base_file))
        return os.path.normpath(os.path.join(base_dir, clean))

def main():
    html_files = get_html_files()
    print(f"=== AUDITORÍA DE ENLACES — Smithers Web ===")
    print(f"Proyecto: {PROJECT}")
    print(f"Archivos .html encontrados: {len(html_files)}")
    for f in html_files:
        size = os.path.getsize(os.path.join(PROJECT, f))
        print(f"   {f} ({size} bytes)")
    print()
    
    # ====== 1. hrefs con .html ======
    print("=" * 70)
    print("1. ENLACES CON EXTENSIÓN .html EN HREF")
    print("=" * 70)
    
    dot_html_count = 0
    dot_html_details = []
    
    for fname in html_files:
        fpath = os.path.join(PROJECT, fname)
        hrefs, _ = extract_hrefs_and_srcs(fpath)
        for line_no, href_val in hrefs:
            if '.html' in href_val.lower():
                dot_html_count += 1
                dot_html_details.append((fname, line_no, href_val))
    
    if dot_html_count == 0:
        print("✓ NO se encontraron hrefs con extensión .html")
        print("  Todos los enlaces internos usan URLs limpias (clean URLs: /carta en vez de /carta.html)")
    else:
        print(f"✗ INCIDENCIAS: {dot_html_count}")
        for fname, ln, href in dot_html_details:
            print(f"   {fname}:{ln} → href=\"{href}\"")
    print()
    
    # ====== 2. TODOS LOS HREFS ÚNICOS Y VERIFICACIÓN DE EXISTENCIA ======
    print("=" * 70)
    print("2. VERIFICACIÓN DE ENLACES (INTERNOS Y EXTERNOS)")
    print("=" * 70)
    
    all_hrefs = {}  # href_value -> [(file, line)]
    all_srcs = {}   # src_value -> [(file, line)]
    
    for fname in html_files:
        fpath = os.path.join(PROJECT, fname)
        hrefs, srcs = extract_hrefs_and_srcs(fpath)
        for ln, val in hrefs:
            all_hrefs.setdefault(val, []).append((fname, ln))
        for ln, val in srcs:
            all_srcs.setdefault(val, []).append((fname, ln))
    
    # Check internal hrefs existence
    broken_internal = []
    external_links = []
    internal_valid = []
    anchors_only = []
    
    for href_val, occurrences in sorted(all_hrefs.items()):
        if is_anchor(href_val):
            anchors_only.append((href_val, occurrences))
            continue
        if is_external(href_val):
            external_links.append((href_val, occurrences))
            continue
        
        resolved = resolve_path(href_val, occurrences[0][0])
        if resolved:
            if os.path.exists(resolved):
                internal_valid.append((href_val, resolved, occurrences))
            else:
                broken_internal.append((href_val, resolved, occurrences))
    
    print(f"Total hrefs únicos: {len(all_hrefs)}")
    print(f"  - Anclas (#): {len(anchors_only)}")
    print(f"  - Enlaces externos: {len(external_links)}")
    print(f"  - Enlaces internos válidos: {len(internal_valid)}")
    print(f"  - Enlaces internos ROTOS: {len(broken_internal)}")
    
    if broken_internal:
        print()
        print("✗ ENLACES ROTOS (no apuntan a archivo existente):")
        for href_val, resolved_path, occurrences in broken_internal:
            print(f"   href=\"{href_val}\" → resuelto: {resolved_path}")
            for ofile, oline in occurrences:
                print(f"       {ofile}:{oline}")
    
    print()
    print("ENLACES EXTERNOS USADOS:")
    ext_domains = set()
    for href_val, occurrences in external_links:
        domain = href_val.split('/')[2] if '://' in href_val else href_val.split(':')[0]
        ext_domains.add(domain)
        first_file = occurrences[0][0]
        first_line = occurrences[0][1]
        count = len(occurrences)
        print(f"   {href_val[:80]}{'...' if len(href_val)>80 else ''}")
        print(f"       → usado {count} vez/veces (primera vez: {first_file}:{first_line})")
    
    print()
    print("ENLACES INTERNOS VÁLIDOS:")
    for href_val, resolved_path, occurrences in sorted(internal_valid):
        rel_path = os.path.relpath(resolved_path, PROJECT)
        count = len(occurrences)
        first_file = occurrences[0][0]
        print(f"   href=\"{href_val}\" → {rel_path} ({count}x, primer uso: {first_file})")
    
    print()
    
    # ====== 3. MEZCLA ABSOLUTOS VS RELATIVOS ======
    print("=" * 70)
    print("3. MEZCLA DE ESTILOS (ABSOLUTOS vs RELATIVOS)")
    print("=" * 70)
    
    abs_internal = []   # /something
    rel_internal = []   # something or ../something
    abs_external = []   # https://...
    
    for href_val, occurrences in all_hrefs.items():
        if is_anchor(href_val):
            continue
        if is_external(href_val) and href_val.startswith('http'):
            abs_external.append((href_val, occurrences))
        elif href_val.startswith('/'):
            abs_internal.append((href_val, occurrences))
        elif not is_external(href_val):
            rel_internal.append((href_val, occurrences))
    
    print(f"Enlaces externos (https://...): {len(abs_external)} únicos")
    print(f"Enlaces internos absolutos (/ruta): {len(abs_internal)} únicos")
    print(f"Enlaces internos relativos (ruta/../ruta): {len(rel_internal)} únicos")
    
    if rel_internal:
        print()
        print("✗ Enlaces relativos encontrados (no empiezan por /):")
        for href_val, occurrences in sorted(rel_internal):
            first_file = occurrences[0][0]
            print(f"   href=\"{href_val}\" (primera vez: {first_file}:{occurrences[0][1]})")
    
    if abs_internal:
        print()
        print("✓ Enlaces internos absolutos (/ruta) — estilo recomendado:")
        for href_val, occurrences in sorted(abs_internal):
            print(f"   href=\"{href_val}\" ({len(occurrences)} ocurrencias)")
    
    print()
    
    # ====== 4. VERIFICAR src DE IMÁGENES ======
    print("=" * 70)
    print("4. VERIFICACIÓN DE IMÁGENES (src / srcset)")
    print("=" * 70)
    
    existing_src = []
    missing_src = []
    external_src = []
    
    for src_val, occurrences in sorted(all_srcs.items()):
        if is_external(src_val):
            external_src.append((src_val, occurrences))
            continue
        
        # Handle srcset with multiple images
        for part in src_val.split(','):
            part = part.strip().split(' ')[0].strip()
            if not part:
                continue
            resolved = resolve_path(part, occurrences[0][0])
            if resolved:
                if os.path.exists(resolved):
                    existing_src.append((part, resolved, occurrences))
                else:
                    missing_src.append((part, resolved, occurrences))
    
    print(f"Total src/srcset únicos: {len(all_srcs)}")
    print(f"  - Fuentes externas: {len(external_src)}")
    print(f"  - Fuentes locales existentes: {len(existing_src)}")
    print(f"  - Fuentes locales NO ENCONTRADAS: {len(missing_src)}")
    
    if missing_src:
        print()
        print("✗ IMÁGENES NO ENCONTRADAS:")
        for src_val, resolved_path, occurrences in missing_src:
            print(f"   src=\"{src_val}\" → resuelto: {resolved_path}")
            for ofile, oline in occurrences:
                print(f"       {ofile}:{oline}")
    
    print()
    
    # ====== 5. CONSISTENCIA DE NAVEGACIÓN ======
    print("=" * 70)
    print("5. CONSISTENCIA DE NAVEGACIÓN (NAV)")
    print("=" * 70)
    
    main_nav_pattern = re.compile(
        r'<a\s+href="/(?:menu-del-dia|menu-shelby|carta|entre-panes|desayunos|take-away|delivery|eventos)">'
    )
    
    nav_sets = {}
    for fname in html_files:
        fpath = os.path.join(PROJECT, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the first <nav> block
        nav_match = re.search(r'<nav[^>]*>(.*?)</nav>', content, re.DOTALL)
        if nav_match:
            nav_content = nav_match.group(1)
            links_found = re.findall(r'<a\s+[^>]*href="([^"]*)"[^>]*>', nav_content)
            # Filter to internal navigation links
            nav_links = [l for l in links_found if not l.startswith('#') and 
                        not is_external(l) or 
                        'instagram' in l or 'facebook' in l or 
                        'google.com/maps/reserve' in l]
            nav_sets[fname] = nav_links
    
    # Compare all navs
    mismatches = []
    if nav_sets:
        first_file = list(nav_sets.keys())[0]
        reference_nav = nav_sets[first_file]
        print(f"Nav de referencia: {first_file}")
        print(f"  Links: {reference_nav}")
        print()
        
        mismatches = []
        for fname, nav_links in nav_sets.items():
            if nav_links != reference_nav:
                mismatches.append((fname, nav_links))
        
        if mismatches:
            print(f"✗ INCONSISTENCIAS ({len(mismatches)} archivos con nav diferente):")
            for fname, nav_links in mismatches:
                diff = set(nav_links) ^ set(reference_nav)
                print(f"   {fname}:")
                print(f"     Referencia: {[l for l in reference_nav if l not in nav_links]}")
                print(f"     Diferencia: {[l for l in nav_links if l not in reference_nav]}")
        else:
            print(f"✓ Todos los {len(nav_sets)} archivos tienen el MISMO nav")
        
        # Check mobile nav too
        print()
        print("NAV MÓVIL (mobile-hero-nav):")
        mobile_navs = {}
        for fname in html_files:
            fpath = os.path.join(PROJECT, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            mn = re.search(r'<div\s+class="mobile-hero-nav"[^>]*>(.*?)</div>', content, re.DOTALL)
            if mn:
                links = re.findall(r'<a\s+href="([^"]*)"', mn.group(1))
                mobile_navs[fname] = links
        
        if mobile_navs:
            ref_mobile = list(mobile_navs.values())[0]
            mobile_mismatches = [(f, l) for f, l in mobile_navs.items() if l != ref_mobile]
            if mobile_mismatches:
                print(f"✗ Mobile nav inconsistente en {len(mobile_mismatches)} archivos")
                for fname, links in mobile_mismatches:
                    print(f"   {fname}: {links}")
            else:
                print(f"✓ Todos los {len(mobile_navs)} archivos con mobile-nav son iguales")
    
    print()
    
    # ====== 6. PÁGINAS LEGACY ======
    print("=" * 70)
    print("6. ENLACES A PÁGINAS LEGACY")
    print("=" * 70)
    
    legacy_patterns = ['bocadillos', 'reservation', 'contacto', 'legal']
    legacy_found = []
    
    for href_val, occurrences in all_hrefs.items():
        href_lower = href_val.lower()
        for pattern in legacy_patterns:
            if pattern in href_lower and not href_lower.endswith('.css') and not href_lower.endswith('.js'):
                legacy_found.append((href_val, pattern, occurrences))
    
    if legacy_found:
        print(f"✗ ENLACES A PÁGINAS LEGACY ({len(legacy_found)}):")
        for href_val, pattern, occurrences in legacy_found:
            print(f"   href=\"{href_val}\" (coincide con patrón '{pattern}')")
            for ofile, oline in occurrences:
                print(f"       {ofile}:{oline}")
    else:
        print("✓ No se encontraron enlaces a páginas legacy (bocadillos, reservation, contacto, legal)")
    
    print()
    print("=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    
    issues = 0
    if dot_html_count > 0:
        issues += dot_html_count
        print(f"  1. hrefs con .html: {dot_html_count} incidencias")
    else:
        print("  1. hrefs con .html: 0 incidencias ✓")
    
    if broken_internal:
        issues += len(broken_internal)
        print(f"  2. Enlaces rotos: {len(broken_internal)} incidencias")
    else:
        print("  2. Enlaces rotos: 0 incidencias ✓")
    
    # mixed styles - only flag if there are relative internal links
    if rel_internal:
        # Check if they're actually all OK (e.g. favicon.ico is relative but valid)
        # Only report as issue if they mix with absolute internal links AND aren't just favicons
        non_favicon_rel = [(h, o) for h, o in rel_internal if h != 'favicon.ico' and h != 'favicon-96x96.png' and h != 'favicon.svg' and h != 'apple-touch-icon.png']
        if non_favicon_rel:
            print(f"  3. Mezcla absolutos/relativos: {len(non_favicon_rel)} enlaces relativos (no favicon)")
            issues += len(non_favicon_rel)
        else:
            print("  3. Mezcla absolutos/relativos: 0 incidencias (relativos solo favicons) ✓")
    else:
        print("  3. Mezcla absolutos/relativos: 0 incidencias ✓")
    
    if missing_src:
        issues += len(missing_src)
        print(f"  4. Imágenes no encontradas: {len(missing_src)} incidencias")
    else:
        print("  4. Imágenes no encontradas: 0 incidencias ✓")
    
    if mismatches:
        issues += len(mismatches)
        print(f"  5. Inconsistencias navegación: {len(mismatches)} archivos con nav diferente")
    else:
        print("  5. Consistencia navegación: 0 incidencias ✓")
    
    if legacy_found:
        issues += len(legacy_found)
        print(f"  6. Enlaces legacy: {len(legacy_found)} incidencias")
    else:
        print("  6. Enlaces legacy: 0 incidencias ✓")
    
    print()
    print(f"TOTAL INCIDENCIAS: {issues}")
    if issues == 0:
        print("ESTADO: ✓ AUDITORÍA SUPERADA — Sin incidencias")
    else:
        print(f"ESTADO: ⚠ SE ENCONTRARON {issues} INCIDENCIAS — Revisar detalles arriba")

if __name__ == '__main__':
    main()