import hou

# ===== DREMPEL HDA =====
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
    DREMPEL_STIL     = geo.parm('drempel_stil').eval()
    KONUM_X          = geo.parm('drempel_konum_x').eval()
    KONUM_Y          = geo.parm('drempel_konum_y').eval()
    KONUM_Z          = geo.parm('drempel_konum_z').eval()

    T_UST_GENISLIK   = geo.parm('t_ust_genislik').eval()
    T_UST_UZUNLUK    = geo.parm('t_ust_uzunluk').eval()
    T_UST_SAY        = geo.parm('t_ust_say').eval()
    T_UST_KAT        = geo.parm('t_ust_kat').eval()
    T_SUTUN_GENISLIK = geo.parm('t_sutun_genislik').eval()
    T_SUTUN_UZUNLUK  = geo.parm('t_sutun_uzunluk').eval()
    T_KALINLIK       = geo.parm('t_kalinlik').eval()
    T_ARALIK         = geo.parm('t_aralik').eval()
    T_SUTUN_SAY      = geo.parm('t_sutun_say').eval()
    T_SUTUN_ARALIK   = geo.parm('t_sutun_aralik').eval()
    T_UZUN_BOY       = geo.parm('t_uzun_boy').eval()
    T_KISA_BOY       = geo.parm('t_kisa_boy').eval()

    H_UST_GENISLIK   = geo.parm('h_ust_genislik').eval()
    H_SUTUN_GENISLIK = geo.parm('h_sutun_genislik').eval()
    H_SUTUN_SAY      = geo.parm('h_sutun_say').eval()
    H_SUTUN_ARALIK   = geo.parm('h_sutun_aralik').eval()
    H_UZUN_BOY       = geo.parm('h_uzun_boy').eval()
    H_KISA_BOY       = geo.parm('h_kisa_boy').eval()
    H_YUKSEKLIK      = geo.parm('h_yukseklik').eval()

except Exception as e:
    print('Parametre hatasi:', e)
    DREMPEL_STIL     = 1
    KONUM_X          = 0
    KONUM_Y          = 0
    KONUM_Z          = 0
    T_UST_GENISLIK   = 0.2
    T_UST_UZUNLUK    = 0.1
    T_UST_SAY        = 10
    T_UST_KAT        = 1
    T_SUTUN_GENISLIK = 0.2
    T_SUTUN_UZUNLUK  = 0.1
    T_KALINLIK       = 0.05
    T_ARALIK         = 0.02
    T_SUTUN_SAY      = 3
    T_SUTUN_ARALIK   = 1.0
    T_UZUN_BOY       = 5
    T_KISA_BOY       = 2
    H_UST_GENISLIK   = 0.3
    H_SUTUN_GENISLIK = 0.1
    H_SUTUN_SAY      = 3
    H_SUTUN_ARALIK   = 1.0
    H_UZUN_BOY       = 1.0
    H_KISA_BOY       = 0.5
    H_YUKSEKLIK      = 0.05

# Tek sayıya zorla
if T_SUTUN_SAY % 2 == 0:
    T_SUTUN_SAY += 1
    try:
        geo.parm('t_sutun_say').set(T_SUTUN_SAY)
    except:
        pass
if H_SUTUN_SAY % 2 == 0:
    H_SUTUN_SAY += 1
    try:
        geo.parm('h_sutun_say').set(H_SUTUN_SAY)
    except:
        pass

drempel_elemanlar = []

def kutu(isim, sx, sy, sz, tx=0, ty=0, tz=0):
    n = geo.createNode('box', isim)
    n.parm('sizex').set(sx)
    n.parm('sizey').set(sy)
    n.parm('sizez').set(sz)
    n.parm('tx').set(tx)
    n.parm('ty').set(ty)
    n.parm('tz').set(tz)
    m = n.createOutputNode('material')
    m.parm('shop_materialpath1').set('/mat/beyaz_cizgi')
    return m

if DREMPEL_STIL == 0:
    # ========== T STİLİ (TUGLA) ==========
    sutun_toplam = T_SUTUN_SAY + 2
    sutun_toplam_genislik = (sutun_toplam - 1) * T_SUTUN_ARALIK + T_SUTUN_GENISLIK
    ust_toplam = T_UST_SAY * (T_UST_GENISLIK + T_ARALIK) - T_ARALIK
    while ust_toplam < sutun_toplam_genislik:
        T_UST_SAY += 1
        ust_toplam = T_UST_SAY * (T_UST_GENISLIK + T_ARALIK) - T_ARALIK

    ust_alt_z = -((T_UST_KAT - 1) * (T_UST_UZUNLUK + T_ARALIK) + T_UST_UZUNLUK / 2)

    for kat in range(T_UST_KAT):
        tz_kat = -(kat * (T_UST_UZUNLUK + T_ARALIK))
        for i in range(T_UST_SAY):
            tx = i * (T_UST_GENISLIK + T_ARALIK) + T_UST_GENISLIK / 2
            drempel_elemanlar.append(kutu(f'ust_kat{kat}_{i}', T_UST_GENISLIK, T_KALINLIK, T_UST_UZUNLUK, tx=tx, ty=0.01, tz=tz_kat))

    # Esit aralik — kenar sutunlar ust sira ile hizali
    t_aralik_hesap = (ust_toplam - T_SUTUN_GENISLIK) / (sutun_toplam - 1)
    for s in range(sutun_toplam):
        tx = T_SUTUN_GENISLIK / 2 + s * t_aralik_hesap

        boy = T_UZUN_BOY if s % 2 == 0 else T_KISA_BOY
        for j in range(boy):
            tz = ust_alt_z - (j * (T_SUTUN_UZUNLUK + T_ARALIK)) - T_SUTUN_UZUNLUK / 2
            drempel_elemanlar.append(kutu(f'sutun_{s}_{j}', T_SUTUN_GENISLIK, T_KALINLIK, T_SUTUN_UZUNLUK, tx=tx, ty=0.01, tz=tz))

else:
    # ========== H STİLİ (HAT) ==========
    toplam_sutun = H_SUTUN_SAY + 2
    ust_toplam = (H_SUTUN_SAY + 1) * H_SUTUN_ARALIK + H_SUTUN_GENISLIK

    drempel_elemanlar.append(kutu('ust_hat', ust_toplam, H_YUKSEKLIK, H_UST_GENISLIK, tx=ust_toplam/2, ty=0.01, tz=0))

    ust_alt_z = -(H_UST_GENISLIK / 2)
    uzun_merkez_z = ust_alt_z - (H_UZUN_BOY / 2)
    kisa_merkez_z = ust_alt_z - (H_KISA_BOY / 2)

    # Esit aralik — kenar sutunlar ust hat ile hizali
    h_aralik_hesap = (ust_toplam - H_SUTUN_GENISLIK) / (toplam_sutun - 1)
    for s in range(toplam_sutun):
        tx = H_SUTUN_GENISLIK / 2 + s * h_aralik_hesap

        if s % 2 == 0:
            drempel_elemanlar.append(kutu(f'sutun_{s}', H_SUTUN_GENISLIK, H_YUKSEKLIK, H_UZUN_BOY, tx=tx, ty=0.01, tz=uzun_merkez_z))
        else:
            drempel_elemanlar.append(kutu(f'sutun_{s}', H_SUTUN_GENISLIK, H_YUKSEKLIK, H_KISA_BOY, tx=tx, ty=0.01, tz=kisa_merkez_z))

merge = geo.createNode('merge', 'drempel_merge')
for i, e in enumerate(drempel_elemanlar):
    merge.setInput(i, e)

konum = merge.createOutputNode('xform', 'drempel_konum')
konum.parm('tx').set(KONUM_X)
konum.parm('ty').set(KONUM_Y)
konum.parm('tz').set(KONUM_Z)

konum.setDisplayFlag(True)
geo.layoutChildren()
print('Drempel hazir!')