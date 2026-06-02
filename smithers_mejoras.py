#!/usr/bin/env python3
"""
Smithers Web Improvement Script
Applies G2 (SEO) + G3 (Brand) improvements to all HTML pages.
Run: python3 smithers_mejoras.py
"""

import os
import re
import json
import glob

# ===== CONFIG =====
WEB_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://smithersrestaurant.com"
GLOVO_URL = "https://glovoapp.com/es/es/madrid/stores/smithers-restaurant-madrid"
GA4_ID = "G-MG3Y3TKP8M"

# Page-specific SEO data
PAGE_DATA = {
    "index": {
        "title": "Smithers Restaurant | Bar & Restaurante en Madrid, Julián Camarillo",
        "desc": "Descubre Smithers Restaurant en Madrid. Menú del día desde 16,50€, desayunos, take away y eventos. Calidad y buen ambiente en C/ Albasanz 16.",
        "og_image": "/img/og-smithers.jpg"
    },
    "carta": {
        "title": "Carta de Smithers Restaurant | Cocina casera en Madrid",
        "desc": "Explora nuestra carta con 42 platos: desde costillas BBQ y hamburguesas hasta torreznos y postres caseros. Pide online o visita nuestro local.",
        "og_image": "/img/og-smithers.jpg"
    },
    "menu-del-dia": {
        "title": "Menú del día Smithers | 16,50€ en Madrid",
        "desc": "Menú del día de lunes a viernes por 16,50€ en Smithers. Primer plato, segundo, postre, pan y bebida incluidos. También disponible para llevar.",
        "og_image": "/img/og-smithers.jpg"
    },
    "desayunos": {
        "title": "Desayunos Smithers | De 7:00 a 12:00 en Madrid",
        "desc": "Desayunos variados desde las 7:00h. Café, tostadas, churros, zumos y menús completos. Empieza el día con energía en Smithers.",
        "og_image": "/img/og-smithers.jpg"
    },
    "menu-shelby": {
        "title": "Menú Shelby Smithers | 14,50€ en Madrid",
        "desc": "Menú Shelby desde 14,50€. Hamburguesa, bebida y postre. La mejor relación calidad-precio de Julián Camarillo.",
        "og_image": "/img/og-smithers.jpg"
    },
    "eventos": {
        "title": "Eventos y catering en Smithers Restaurant Madrid",
        "desc": "Celebra tu evento en Smithers: grupos hasta 140 personas, cócteles hasta 180. Catering para empresas. Presupuesto sin compromiso.",
        "og_image": "/img/og-smithers.jpg"
    },
    "catering": {
        "title": "Catering Smithers | Servicio de cátering para empresas en Madrid",
        "desc": "Catering corporativo y para eventos en Madrid. Menús personalizados, entrega en oficinas. Calidad de restaurante en tu evento.",
        "og_image": "/img/og-smithers.jpg"
    },
    "contacto": {
        "title": "Contacto Smithers Restaurant | Madrid, C/ Albasanz 16",
        "desc": "Visítanos en C/ Albasanz 16, 28037 Madrid. Llámanos al 911 699 622 o escríbenos a smithersrestaurant@gmail.com. Horario: L-V 7:00-17:00.",
        "og_image": "/img/og-smithers.jpg"
    },
    "aviso-legal": {
        "title": "Aviso legal - Smithers Restaurant Madrid",
        "desc": "Aviso legal de Smithers Restaurant. Stewart Avenue S.L.U. C/ Albasanz 16, 28037 Madrid. Condiciones de uso del sitio web.",
        "og_image": "/img/og-smithers.jpg"
    },
    "privacidad": {
        "title": "Política de privacidad - Smithers Restaurant Madrid",
        "desc": "Política de privacidad y cookies de Smithers Restaurant. Información sobre tratamiento de datos y tus derechos.",
        "og_image": "/img/og-smithers.jpg"
    }
}

def get_page_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def has_tag(html, tag):
    """Check if a specific tag/pattern already exists in the HTML head"""
    return tag in html

def add_to_head(html, content):
    """Insert content before </head>"""
    return html.replace("</head>", content + "\n</head>")

def add_to_body_end(html, content):
    """Insert content before </body>"""
    return html.replace("</body>", content + "\n</body>")

def add_schema(html, page_name):
    """Add Schema.org JSON-LD for Restaurant (only on index) or specific page"""
    schema_tag = '<script type="application/ld+json">'
    
    if page_name == "index":
        schema = {
            "@context": "https://schema.org",
            "@type": "Restaurant",
            "name": "Smithers Restaurant",
            "image": "https://smithersrestaurant.com/img/og-smithers.jpg",
            "url": "https://smithersrestaurant.com",
            "telephone": "+34911699622",
            "email": "smithersrestaurant@gmail.com",
            "servesCuisine": "Española, Internacional",
            "priceRange": "€€",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "C/ Albasanz 16",
                "addressLocality": "Madrid",
                "postalCode": "28037",
                "addressCountry": "ES"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": 40.4342,
                "longitude": -3.6321
            },
            "openingHoursSpecification": [
                {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                    "opens": "07:00",
                    "closes": "17:00"
                }
            ],
            "hasMenu": [
                {
                    "@type": "Menu",
                    "name": "Carta",
                    "url": "https://smithersrestaurant.com/carta.html"
                },
                {
                    "@type": "Menu",
                    "name": "Menú del día",
                    "url": "https://smithersrestaurant.com/menu-del-dia.html"
                },
                {
                    "@type": "Menu",
                    "name": "Menú Shelby",
                    "url": "https://smithersrestaurant.com/menu-shelby.html"
                },
                {
                    "@type": "Menu",
                    "name": "Desayunos",
                    "url": "https://smithersrestaurant.com/desayunos.html"
                }
            ],
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.3",
                "reviewCount": "120"
            },
            "acceptsReservations": "True",
            "sameAs": [
                "https://www.instagram.com/smithers_restaurant/",
                "https://www.facebook.com/people/Smithers-Restaurant/61588168375109/",
                "https://maps.google.com/maps?cid=0"
            ]
        }
    elif page_name == "eventos":
        schema = {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": "Eventos en Smithers Restaurant",
            "location": {
                "@type": "Place",
                "name": "Smithers Restaurant",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "C/ Albasanz 16",
                    "addressLocality": "Madrid",
                    "postalCode": "28037",
                    "addressCountry": "ES"
                }
            }
        }
    elif page_name == "catering":
        schema = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": "Catering Smithers Restaurant",
            "provider": {
                "@type": "Restaurant",
                "name": "Smithers Restaurant",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "C/ Albasanz 16",
                    "addressLocality": "Madrid",
                    "postalCode": "28037",
                    "addressCountry": "ES"
                }
            }
        }
    else:
        schema = None
    
    if schema:
        new_block = schema_tag + "\n" + json.dumps(schema, indent=2, ensure_ascii=False) + "\n</script>"
        if schema_tag in html:
            # Replace existing schema block (from <script to </script>)
            end_idx = html.find("</script>", html.find(schema_tag))
            old_block = html[html.find(schema_tag):end_idx + 9]
            return html.replace(old_block, new_block)
        else:
            # Insert before </head>
            return html.replace("</head>", new_block + "\n</head>")
    return html

def add_faq_schema(html):
    """Add FAQPage schema if not present"""
    if "FAQPage" in html:
        return html
    
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "¿Dónde está Smithers Restaurant?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Estamos en C/ Albasanz 16, 28037 Madrid, en la zona de Julián Camarillo."
                }
            },
            {
                "@type": "Question",
                "name": "¿Cuál es el horario de Smithers?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Abrimos de lunes a viernes de 7:00 a 17:00."
                }
            },
            {
                "@type": "Question",
                "name": "¿Cuánto cuesta el menú del día?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "El menú del día cuesta 16,50€ e incluye primer plato, segundo, postre, pan y bebida."
                }
            },
            {
                "@type": "Question",
                "name": "¿Hacen take away?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Sí, puedes pedir para llevar desde 13,90€. También tenemos servicio a domicilio a través de Glovo."
                }
            }
        ]
    }
    
    script = '\n<script type="application/ld+json">\n' + json.dumps(faq, indent=2, ensure_ascii=False) + '\n</script>'
    # Insert FAQ before </head> (there may already be another schema script)
    return html.replace("</head>", script + "\n</head>")


def process_html(filepath):
    """Apply all improvements to a single HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    page_name = get_page_name(filepath)
    original = html
    
    # Get page data
    data = PAGE_DATA.get(page_name, PAGE_DATA["index"])
    
    # ===== 1. TITLE (ensure it's good) =====
    title_pattern = r'<title>(.*?)</title>'
    title_match = re.search(title_pattern, html)
    if title_match:
        html = html.replace(title_match.group(0), f'<title>{data["title"]}</title>')
    else:
        html = html.replace('<head>', f'<head>\n    <title>{data["title"]}</title>')
    
    # ===== 2. META DESCRIPTION =====
    desc_pattern = r'<meta\s+name=["\']description["\'][^>]*content=["\']([^"\']*)["\']'
    if re.search(desc_pattern, html):
        html = re.sub(desc_pattern, f'<meta name="description" content="{data["desc"]}">', html)
    else:
        html = add_to_head(html, f'    <meta name="description" content="{data["desc"]}">')
    
    # ===== 3. CANONICAL =====
    canonical_url = f'{SITE_URL}/{page_name}.html' if page_name != 'index' else SITE_URL
    canonical_tag = f'<link rel="canonical" href="{canonical_url}">'
    if 'rel="canonical"' not in html and "rel='canonical'" not in html:
        html = add_to_head(html, f'    {canonical_tag}')
    
# ===== 4. OPEN GRAPH =====
    og_tags = {
        'og:title': data['title'],
        'og:description': data['desc'],
        'og:image': f'{SITE_URL}{data["og_image"]}',
        'og:url': canonical_url,
        'og:type': 'website',
        'og:site_name': 'Smithers Restaurant'
    }
    for prop, content in og_tags.items():
        # Replace existing og tag or add new one
        existing = re.search(rf'<meta\s+property="{re.escape(prop)}"[^>]*>', html)
        if existing:
            html = html.replace(existing.group(0), f'<meta property="{prop}" content="{content}">')
        else:
            html = add_to_head(html, f'    <meta property="{prop}" content="{content}">')

    # ===== 5. TWITTER CARDS =====
    twitter_tags = {
        'twitter:card': 'summary_large_image',
        'twitter:title': data['title'],
        'twitter:description': data['desc'],
        'twitter:image': f'{SITE_URL}{data["og_image"]}'
    }
    for name, content in twitter_tags.items():
        # Replace existing twitter tag or add new one
        existing = re.search(rf'<meta\s+name="{re.escape(name)}"[^>]*>', html)
        if existing:
            html = html.replace(existing.group(0), f'<meta name="{name}" content="{content}">')
        else:
            html = add_to_head(html, f'    <meta name="{name}" content="{content}">')

    # ===== 5b. ROBOTS META =====
    if 'name="robots"' not in html:
        html = add_to_head(html, '    <meta name="robots" content="index, follow">')
    
    # ===== 6. SCHEMA.ORG =====
    schema_tag = '<script type="application/ld+json">'
    schema_start_idx = html.find(schema_tag)
    if schema_start_idx != -1:
        # Replace existing schema block - generate fresh one
        temp_html = add_schema(html, page_name)
        if temp_html != html:
            html = temp_html
    else:
        html = add_schema(html, page_name)
    
    # ===== 7. FAQ SCHEMA (only on index) =====
    if page_name == 'index':
        html = add_faq_schema(html)
    
    # ===== 8. COOKIES.JS =====
    cookies_script = '<script src="/cookies.js"></script>'
    if 'cookies.js' not in html:
        html = add_to_head(html, f'    {cookies_script}')
    
    # ===== 9. FOOTER SNIPPET (Gestinar cookies) =====
    manage_link = '<span id="cookie-manage-link" onclick="if(window.SmithersCookies)window.SmithersCookies.openPreferences()">🍪 Gestionar cookies</span>'
    if 'Gestionar cookies' not in html:
        # Insert near copyright or end of footer
        html = html.replace('</footer>', f'        <p style="text-align:center;margin-top:10px;font-size:13px;">{manage_link} · Con ❤️</p>\n    </footer>')
    
    # ===== 10. GLOVO URL correction =====
    html = re.sub(
        r'href=["\']https?://(?:(?:www\.)?glovoapp\.com[^"\']*|glovoapp\.com[^"\']*)["\']',
        f'href="{GLOVO_URL}"',
        html
    )
    
    # ===== 11. GA4 (if GA4_ID set) =====
    if GA4_ID and GA4_ID != "G-XXXXXXXXXX":
        ga4_script = f'''
    <!-- Google tag (gtag.js) - Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA4_ID}', {{
            'anonymize_ip': true,
            'cookie_flags': 'SameSite=None;Secure'
        }});
    </script>'''
        if 'googletagmanager' not in html:
            html = add_to_head(html, ga4_script)
    
    # ===== Save if changed =====
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False


def create_sitemap():
    """Generate sitemap.xml"""
    urls = []
    for filename in sorted(glob.glob(os.path.join(WEB_DIR, '*.html'))):
        page_name = get_page_name(filename)
        if page_name in ('index',):
            loc = SITE_URL
        else:
            loc = f'{SITE_URL}/{page_name}.html'
        urls.append(f'''  <url>
    <loc>{loc}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>''')
    
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''
    
    with open(os.path.join(WEB_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap)
    return True


def create_robots():
    """Generate robots.txt"""
    content = '''User-agent: *
Allow: /

Sitemap: https://smithersrestaurant.com/sitemap.xml
'''
    with open(os.path.join(WEB_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    print("=== Smithers Web Improvement Script ===")
    print(f"Directory: {WEB_DIR}")
    print()
    
    html_files = sorted(glob.glob(os.path.join(WEB_DIR, '*.html')))
    print(f"Found {len(html_files)} HTML files")
    
    modified = 0
    for filepath in html_files:
        page_name = get_page_name(filepath)
        if page_name in ('index',):
            print(f"  {page_name}.html ... ", end="", flush=True)
        else:
            print(f"  {page_name}.html ... ", end="", flush=True)
        if process_html(filepath):
            print("✅ MODIFIED")
            modified += 1
        else:
            print("✓ already optimized")
    
    print(f"\nModified: {modified}/{len(html_files)}")
    
    # Create sitemap
    print("\nCreating sitemap.xml ... ", end="", flush=True)
    create_sitemap()
    print("✅")
    
    # Create robots.txt
    print("Creating robots.txt ... ", end="", flush=True)
    create_robots()
    print("✅")
    
    print("\n=== Done! ===")
    print("Next steps:")
    print("  1. Replace GA4_ID in this script or manually add the GA4 snippet")
    print("  2. Create og-smithers.jpg (1200x630px) in /img/")
    print("  3. Run: python3 generar_favicons.py")
    print("  4. Increment CSS version: premium.css?v=XX")
    print("  5. Restart server and verify in browser")

if __name__ == '__main__':
    main()