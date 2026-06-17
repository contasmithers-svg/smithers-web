import os, re

dims = {
    'logo-smithers.png': (96, 96),
    'hero-smithers.jpg': (1280, 853),
    'cocina-delivery.jpg': (1280, 853),
    'eventos-networking.jpg': (1280, 853),
    'menu-del-dia-mesa.jpg': (1280, 959),
    'calamares.jpg': (1280, 960),
    'chorizo-criollo.jpg': (1280, 960),
    'langostino-panko.jpg': (1280, 960),
}

carta_1195 = ['AGUJA.jpg','ALBONDIGAS_DE_MERLUZA.jpg','ALBONDIGAS.jpg','ATUN.jpg',
    'BACALAO.jpg','COSTILLAS.jpg','ENSALADA_GRIEGA.jpg','ENSALADA_MIXTA.jpg',
    'ENSALADA_QUESO_DE_CABRA.jpg','FIDEUA.jpg','MERLUZA_SALSA_VERDE.jpg',
    'PAELLA.jpg','POLLO_EMPANADO_ENSALADA.jpg','POLLO_EMPANADO_FRITAS.jpg']
for f in carta_1195:
    dims[f] = (1195, 896)

big_1600 = ['AGUACATE_TOMATE_HUEVO.jpg','ALCACHOFAS.jpg','ARROZ_CUBANA.jpg',
    'ARROZ_NEGRO.jpg','CALABACINES_REBOZADOS.jpg','CHIPIRONES.jpg',
    'ENSALADA_CESAR.jpg','ENSALADILLA.jpg','FLAN_CON_NATA.jpg','GUISANTES.jpg',
    'GYOZAS.jpg','HAMBURGUESA.jpg','LOMO_KATSU.jpg','NATILLAS.jpg','PIÑA.jpg',
    'PISTO.jpg','PLATO_AGUCATE_HUEVOS_TOMATE.jpg','PLATO_HUEVOS_FRITAS_PANCETA_BAJA.jpg',
    'PLATO_LACON_HUEVOS_FRITAS.jpg','PLATO_PAVO_HUEVOS_FRITAS.jpg',
    'PLATO_PAVO_HUEVOS_TOMATE.jpg','POLLO_PLANCHA_ENSALADA.jpg',
    'POLLO_PLANCHA_FRITAS.jpg','POLLO_TERIYAKI.jpg','RISOTO_DE_SETAS.jpg',
    'SECRETO.jpg','SHELBY_AGUJA.jpg','SHELBY_COSTILLAS.jpg','SHELBY_POLLO.jpg',
    'SHELBY_SECRETO.jpg','SHELBY_TERIYAKI.jpg','SHELBY_WOK.jpg',
    'TALLARINES_CARBONARA.jpg','TALLARINES_CON_CHORIZO.jpg','TARTA_DE_ZANAHORIA.jpg',
    'TARTA_QUESO.jpg','TOSTA_PAVO_HUEVO.jpg','WOK.jpg']
for f in big_1600:
    dims[f] = (1600, 1200)

def get_dim(src):
    basename = os.path.basename(src)
    return dims.get(basename)

html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
total_fixed = 0
total_imgs = 0

for html_file in html_files:
    with open(html_file, 'r') as f:
        content = f.read()
    
    original = content
    
    def add_dimensions(m):
        global total_fixed, total_imgs
        total_imgs += 1
        tag = m.group(0)
        
        if 'width="' in tag or 'width=' in tag:
            return tag
        
        src_match = re.search(r'src="([^"]+)"', tag)
        if not src_match:
            return tag
        
        dim = get_dim(src_match.group(1))
        if not dim:
            return tag
        
        w, h = dim
        tag = tag.rstrip()
        if tag.endswith('/>'):
            tag = tag[:-2] + f' width="{w}" height="{h}" />'
        elif tag.endswith('>'):
            tag = tag[:-1] + f' width="{w}" height="{h}">'
        
        total_fixed += 1
        return tag
    
    content = re.sub(r'<img\s[^>]*src="[^"]+"[^>]*>', add_dimensions, content)
    
    if content != original:
        with open(html_file, 'w') as f:
            f.write(content)
        print(f'✅ {html_file}')

print(f'\nTotal: {total_fixed}/{total_imgs} imágenes con width/height añadidos')