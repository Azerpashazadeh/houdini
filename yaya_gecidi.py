import hou

# ===== YAYA GECİDİ HDA =====
obj_node = hou.pwd()

# geo node'u bul veya olustur
geo = obj_node.node('geo1')
if not geo:
    geo = obj_node.createNode('geo', 'geo1')

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
    ADET        = obj_node.parm('yaya_adet').eval()
    GENISLIK    = obj_node.parm('yaya_genislik').eval()
    KALINLIK    = obj_node.parm('yaya_kalinlik').eval()
    UZUNLUK     = obj_node.parm('yaya_uzunluk').eval()
    ARA_MESAFE  = obj_node.parm('yaya_ara_mesafe').eval()
    BASLANGIC_Z = obj_node.parm('yaya_baslangic').eval()
    ROTATE      = obj_node.parm('yaya_rotate').eval()
    KONUM_X     = obj_node.parm('yaya_konum_x').eval()
    KONUM_Y     = obj_node.parm('yaya_konum_y').eval()
except Exception as e:
    print('Parametre hatasi:', e)
    ADET        = 8
    GENISLIK    = 4.5
    KALINLIK    = 0.02
    UZUNLUK     = 0.5
    ARA_MESAFE  = 0.5
    BASLANGIC_Z = 0.0
    ROTATE      = 0
    KONUM_X     = 0
    KONUM_Y     = 0.01

# ===== YAYA ŞERİTLERİ =====
yayalar = []
for i in range(ADET):
    n = geo.createNode('box', f'serit_{i}')
    n.parm('sizex').set(GENISLIK)
    n.parm('sizey').set(KALINLIK)
    n.parm('sizez').set(UZUNLUK)
    n.parm('tx').set(0)
    n.parm('ty').set(0.01)
    n.parm('tz').set(BASLANGIC_Z + i * ARA_MESAFE)
    m = n.createOutputNode('material')
    m.parm('shop_materialpath1').set('/mat/beyaz_cizgi')
    yayalar.append(m)

merge = geo.createNode('merge', 'yaya_merge')
for i, y in enumerate(yayalar):
    merge.setInput(i, y)

xform = merge.createOutputNode('xform', 'yaya_rotate')
xform.parm('ry').set(ROTATE)

konum = xform.createOutputNode('xform', 'yaya_konum')
konum.parm('tx').set(KONUM_X)
konum.parm('ty').set(KONUM_Y)

konum.setDisplayFlag(True)
geo.layoutChildren()
print('Yaya Gecidi hazir!')