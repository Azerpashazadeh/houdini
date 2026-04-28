import hou

# ===== HAAİENTANDEN HDA =====
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
    ADET      = geo.parm('hd_adet').eval()
    GENISLIK  = geo.parm('hd_genislik').eval()
    YUKSEKLIK = geo.parm('hd_yukseklik').eval()
    KALINLIK  = geo.parm('hd_kalinlik').eval()
    ARALIK    = geo.parm('hd_aralik').eval()
    ROTATE    = geo.parm('hd_rotate').eval()
    KONUM_X   = geo.parm('hd_konum_x').eval()
    KONUM_Y   = geo.parm('hd_konum_y').eval()
    KONUM_Z   = geo.parm('hd_konum_z').eval()
except Exception as e:
    print('Parametre hatasi:', e)
    ADET      = 8
    GENISLIK  = 0.3
    YUKSEKLIK = 0.5
    KALINLIK  = 0.01
    ARALIK    = 0.05
    ROTATE    = 0
    KONUM_X   = 0
    KONUM_Y   = 0
    KONUM_Z   = 0

# ===== ÜÇGENLERİ PYTHON SOP İLE OLUŞTUR =====
py_code = f"""
import hou
geo = hou.pwd().geometry()
geo.clear()

ADET      = {ADET}
GENISLIK  = {GENISLIK}
YUKSEKLIK = {YUKSEKLIK}
KALINLIK  = {KALINLIK}
ARALIK    = {ARALIK}

for i in range(ADET):
    cx = i * (GENISLIK + ARALIK)

    # Alt yuz (y=0)
    p0 = geo.createPoint(); p0.setPosition(hou.Vector3(cx,              0,         0))
    p1 = geo.createPoint(); p1.setPosition(hou.Vector3(cx + GENISLIK,   0,         0))
    p2 = geo.createPoint(); p2.setPosition(hou.Vector3(cx + GENISLIK/2, 0, -YUKSEKLIK))

    # Ust yuz (y=KALINLIK)
    p3 = geo.createPoint(); p3.setPosition(hou.Vector3(cx,              KALINLIK,         0))
    p4 = geo.createPoint(); p4.setPosition(hou.Vector3(cx + GENISLIK,   KALINLIK,         0))
    p5 = geo.createPoint(); p5.setPosition(hou.Vector3(cx + GENISLIK/2, KALINLIK, -YUKSEKLIK))

    # Alt yuz polygon
    poly = geo.createPolygon()
    poly.addVertex(p0); poly.addVertex(p1); poly.addVertex(p2)

    # Ust yuz polygon
    poly2 = geo.createPolygon()
    poly2.addVertex(p3); poly2.addVertex(p5); poly2.addVertex(p4)

    # Yan yuzler
    for a, b, c, d in [(p0,p1,p4,p3),(p1,p2,p5,p4),(p2,p0,p3,p5)]:
        side = geo.createPolygon()
        side.addVertex(a); side.addVertex(b); side.addVertex(c); side.addVertex(d)
"""

# Python SOP olustur
py_sop = geo.createNode('python', 'hd_geometry')
py_sop.parm('python').set(py_code)

# Materyal
mat_sop = py_sop.createOutputNode('material', 'hd_mat')
mat_sop.parm('shop_materialpath1').set('/mat/beyaz_cizgi')

# Döndür
xform = mat_sop.createOutputNode('xform', 'hd_rotate')
xform.parm('ry').set(ROTATE)

# Konumlandir
konum = xform.createOutputNode('xform', 'hd_konum')
konum.parm('tx').set(KONUM_X)
konum.parm('ty').set(KONUM_Y)
konum.parm('tz').set(KONUM_Z)

konum.setDisplayFlag(True)
geo.layoutChildren()
print('Haaientanden hazir!')