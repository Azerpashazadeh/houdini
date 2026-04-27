import hou

# ===== BLOK MARKERİNG HDA =====
geo = hou.pwd()

# Eski node'lari temizle
for child in geo.children():
    child.destroy()

# Materyal olustur
mat_node = hou.node('/mat')
if mat_node and not mat_node.node('beyaz_cizgi'):
    beyaz = mat_node.createNode('principledshader::2.0', 'beyaz_cizgi')
    beyaz.parm('basecolorr').set(0.95)
    beyaz.parm('basecolorg').set(0.95)
    beyaz.parm('basecolorb').set(0.95)
    beyaz.parm('rough').set(0.8)
    beyaz.parm('emitcolorr').set(0.95)
    beyaz.parm('emitcolorg').set(0.95)
    beyaz.parm('emitcolorb').set(0.95)
    beyaz.parm('emitint').set(1.0)

# ===== PARAMETRELERİ OKU =====
try:
    ADET        = geo.parm('blok_adet').eval()
    GENISLIK    = geo.parm('blok_genislik').eval()
    KALINLIK    = geo.parm('blok_kalinlik').eval()
    UZUNLUK     = geo.parm('blok_uzunluk').eval()
    ARA_MESAFE  = geo.parm('blok_ara_mesafe').eval()
    BASLANGIC_Z = geo.parm('blok_baslangic').eval()
    ROTATE      = geo.parm('blok_rotate').eval()
    KONUM_X     = geo.parm('blok_konum_x').eval()
    KONUM_Y     = geo.parm('blok_konum_y').eval()
    KONUM_Z     = geo.parm('blok_konum_z').eval()
except Exception as e:
    print('Parametre hatasi:', e)
    ADET        = 4
    GENISLIK    = 2.0
    KALINLIK    = 0.003
    UZUNLUK     = 0.4
    ARA_MESAFE  = 0.8
    BASLANGIC_Z = 0.0
    ROTATE      = 0
    KONUM_X     = 0
    KONUM_Y     = 0
    KONUM_Z     = 0

# ===== BLOK ŞERİTLERİ =====
bloklar = []
for i in range(ADET):
    n = geo.createNode('box', f'blok_{i}')
    n.parm('sizex').set(GENISLIK)
    n.parm('sizey').set(KALINLIK)
    n.parm('sizez').set(UZUNLUK)
    n.parm('tx').set(0)
    n.parm('ty').set(0.001)
    n.parm('tz').set(BASLANGIC_Z + i * ARA_MESAFE)
    m = n.createOutputNode('material')
    m.parm('shop_materialpath1').set('/mat/beyaz_cizgi')
    bloklar.append(m)

merge = geo.createNode('merge', 'blok_merge')
for i, b in enumerate(bloklar):
    merge.setInput(i, b)

xform = merge.createOutputNode('xform', 'blok_rotate')
xform.parm('ry').set(ROTATE)

konum = xform.createOutputNode('xform', 'blok_konum')
konum.parm('tx').set(KONUM_X)
konum.parm('ty').set(KONUM_Y)
konum.parm('tz').set(KONUM_Z)

konum.setDisplayFlag(True)
geo.layoutChildren()
print('Blok Markering hazir!')
