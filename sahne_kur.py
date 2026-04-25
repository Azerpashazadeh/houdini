import hou

obj = hou.node('/obj')
mat_node = hou.node('/mat')

for isim in ['asfalt', 'beton', 'bordur', 'beyaz_cizgi', 'ok_beyaz']:
    eski = mat_node.node(isim)
    if eski:
        eski.destroy()

# ===== MATERYALLER =====
asfalt = mat_node.createNode('principledshader::2.0', 'asfalt')
asfalt.parm('basecolorr').set(0.12)
asfalt.parm('basecolorg').set(0.12)
asfalt.parm('basecolorb').set(0.12)
asfalt.parm('rough').set(0.95)

beton = mat_node.createNode('principledshader::2.0', 'beton')
beton.parm('basecolorr').set(0.6)
beton.parm('basecolorg').set(0.58)
beton.parm('basecolorb').set(0.55)
beton.parm('rough').set(0.9)

bordur = mat_node.createNode('principledshader::2.0', 'bordur')
bordur.parm('basecolorr').set(0.45)
bordur.parm('basecolorg').set(0.43)
bordur.parm('basecolorb').set(0.4)
bordur.parm('rough').set(0.85)

beyaz_cizgi = mat_node.createNode('principledshader::2.0', 'beyaz_cizgi')
beyaz_cizgi.parm('basecolorr').set(0.95)
beyaz_cizgi.parm('basecolorg').set(0.95)
beyaz_cizgi.parm('basecolorb').set(0.95)
beyaz_cizgi.parm('rough').set(0.8)
beyaz_cizgi.parm('emitcolorr').set(0.95)
beyaz_cizgi.parm('emitcolorg').set(0.95)
beyaz_cizgi.parm('emitcolorb').set(0.95)
beyaz_cizgi.parm('emitint').set(1.0)

ok_beyaz = mat_node.createNode('principledshader::2.0', 'ok_beyaz')
ok_beyaz.parm('basecolorr').set(1.0)
ok_beyaz.parm('basecolorg').set(1.0)
ok_beyaz.parm('basecolorb').set(1.0)
ok_beyaz.parm('rough').set(1.0)
ok_beyaz.parm('emitcolorr').set(1.0)
ok_beyaz.parm('emitcolorg').set(1.0)
ok_beyaz.parm('emitcolorb').set(1.0)
ok_beyaz.parm('emitint').set(1.0)

# ===== SAHNE =====
geo = hou.node('/obj/trafik_yolu')


def kutu(isim, sx, sy, sz, tx=0, ty=0, tz=0, mat=''):
    n = geo.createNode('box', isim)
    n.parm('sizex').set(sx)
    n.parm('sizey').set(sy)
    n.parm('sizez').set(sz)
    n.parm('tx').set(tx)
    n.parm('ty').set(ty)
    n.parm('tz').set(tz)
    if mat:
        m = n.createOutputNode('material')
        m.parm('shop_materialpath1').set(f'/mat/{mat}')
        return m
    return n


zemin = geo.createNode('grid', 'zemin')
zemin.parm('sizex').set(8.0)
zemin.parm('sizey').set(20.0)
zemin.parm('rows').set(20)
zemin.parm('cols').set(6)
zemin_m = zemin.createOutputNode('material')
zemin_m.parm('shop_materialpath1').set('/mat/asfalt')

bsol = kutu('bordur_sol', 2.5, 0.5, 20.0, tx=-5.25, ty=0.1, mat='bordur')
bsag = kutu('bordur_sag', 2.5, 0.5, 20.0, tx=5.25, ty=0.1, mat='bordur')
csol = kutu('cizgi_sol', 0.10, 0.009, 20.0, tx=-3.9, ty=0.01, mat='beyaz_cizgi')
csag = kutu('cizgi_sag', 0.12, 0.02, 20.0, tx=3.9, ty=0.01, mat='beyaz_cizgi')

kesikler = []
for i, tz in enumerate([-8, -4, 0, 4, 8]):
    k = kutu(f'kesik_{i}', 0.12, 0.02, 1.5, ty=0.01, tz=tz, mat='beyaz_cizgi')
    kesikler.append(k)

# ===== PARAMETRELER =====
try:
    node = hou.node('/obj/trafik_yolu')

    ADET              = node.parm('yaya_adet').eval()
    GENISLIK          = node.parm('yaya_genislik').eval()
    KALINLIK          = node.parm('yaya_kalinlik').eval()
    UZUNLUK           = node.parm('yaya_uzunluk').eval()
    ARA_MESAFE        = node.parm('yaya_ara_mesafe').eval()
    BASLANGIC_Z       = node.parm('yaya_baslangic').eval()
    ROTATE            = node.parm('yaya_rotate').eval()
    KONUM_X           = node.parm('yaya_konum_x').eval()
    KONUM_Y           = node.parm('yaya_konum_y').eval()

    BLOK_ADET         = node.parm('blok_adet').eval()
    BLOK_GENISLIK     = node.parm('blok_genislik').eval()
    BLOK_KALINLIK     = node.parm('blok_kalinlik').eval()
    BLOK_UZUNLUK      = node.parm('blok_uzunluk').eval()
    BLOK_ARA_MESAFE   = node.parm('blok_ara_mesafe').eval()
    BLOK_BASLANGIC    = node.parm('blok_baslangic').eval()
    BLOK_ROTATE       = node.parm('blok_rotate').eval()
    BLOK_KONUM_X      = node.parm('blok_konum_x').eval()
    BLOK_KONUM_Y      = node.parm('blok_konum_y').eval()

    DREMPEL_STIL      = node.parm('drempel_stil').eval()
    DREMPEL_KONUM_X   = node.parm('drempel_konum_x').eval()
    DREMPEL_KONUM_Y   = node.parm('drempel_konum_y').eval()
    DREMPEL_KONUM_Z   = node.parm('drempel_konum_z').eval()

    T_UST_GENISLIK    = node.parm('t_ust_genislik').eval()
    T_UST_UZUNLUK     = node.parm('t_ust_uzunluk').eval()
    T_UST_SAY         = node.parm('t_ust_say').eval()
    T_UST_KAT         = node.parm('t_ust_kat').eval()
    T_SUTUN_GENISLIK  = node.parm('t_sutun_genislik').eval()
    T_SUTUN_UZUNLUK   = node.parm('t_sutun_uzunluk').eval()
    T_KALINLIK        = node.parm('t_kalinlik').eval()
    T_ARALIK          = node.parm('t_aralik').eval()
    T_SUTUN_SAY       = node.parm('t_sutun_say').eval()
    T_SUTUN_ARALIK    = node.parm('t_sutun_aralik').eval()
    T_UZUN_BOY        = node.parm('t_uzun_boy').eval()
    T_KISA_BOY        = node.parm('t_kisa_boy').eval()

    H_UST_GENISLIK    = node.parm('h_ust_genislik').eval()
    H_SUTUN_GENISLIK  = node.parm('h_sutun_genislik').eval()
    H_SUTUN_SAY       = node.parm('h_sutun_say').eval()
    H_SUTUN_ARALIK    = node.parm('h_sutun_aralik').eval()
    H_UZUN_BOY        = node.parm('h_uzun_boy').eval()
    H_KISA_BOY        = node.parm('h_kisa_boy').eval()
    H_YUKSEKLIK       = node.parm('h_yukseklik').eval()

except:
    ADET              = 6
    GENISLIK          = 4.5
    KALINLIK          = 0.02
    UZUNLUK           = 0.4
    ARA_MESAFE        = 0.8
    BASLANGIC_Z       = 7.0
    ROTATE            = 0
    KONUM_X           = 0
    KONUM_Y           = 0.01

    BLOK_ADET         = 4
    BLOK_GENISLIK     = 2.0
    BLOK_KALINLIK     = 0.02
    BLOK_UZUNLUK      = 0.4
    BLOK_ARA_MESAFE   = 0.8
    BLOK_BASLANGIC    = -5.0
    BLOK_ROTATE       = 0
    BLOK_KONUM_X      = 0
    BLOK_KONUM_Y      = 0.01

    DREMPEL_STIL      = 0
    DREMPEL_KONUM_X   = 0
    DREMPEL_KONUM_Y   = 0.01
    DREMPEL_KONUM_Z   = 0

    T_UST_GENISLIK    = 0.2
    T_UST_UZUNLUK     = 0.1
    T_UST_SAY         = 10
    T_UST_KAT         = 1
    T_SUTUN_GENISLIK  = 0.2
    T_SUTUN_UZUNLUK   = 0.1
    T_KALINLIK        = 0.05
    T_ARALIK          = 0.02
    T_SUTUN_SAY       = 3
    T_SUTUN_ARALIK    = 1.0
    T_UZUN_BOY        = 5
    T_KISA_BOY        = 2

    H_UST_GENISLIK    = 0.3
    H_SUTUN_GENISLIK  = 0.1
    H_SUTUN_SAY       = 3
    H_SUTUN_ARALIK    = 1.0
    H_UZUN_BOY        = 1.0
    H_KISA_BOY        = 0.5
    H_YUKSEKLIK       = 0.05

# Tek sayıya zorla — sol ve sag her zaman uzun olsun
if T_SUTUN_SAY % 2 == 0:
    T_SUTUN_SAY += 1
    try:
        node.parm('t_sutun_say').set(T_SUTUN_SAY)
    except:
        pass
if H_SUTUN_SAY % 2 == 0:
    H_SUTUN_SAY += 1
    try:
        node.parm('h_sutun_say').set(H_SUTUN_SAY)
    except:
        pass

# ===== YAYA GEÇİDİ =====
yayalar = []
for i in range(ADET):
    n = geo.createNode('box', f'yaya_{i}')
    n.parm('sizex').set(GENISLIK)
    n.parm('sizey').set(KALINLIK)
    n.parm('sizez').set(UZUNLUK)
    n.parm('ty').set(KONUM_Y)
    n.parm('tz').set(BASLANGIC_Z + i * ARA_MESAFE)
    n.parm('tx').set(KONUM_X)
    m = n.createOutputNode('material')
    m.parm('shop_materialpath1').set('/mat/beyaz_cizgi')
    yayalar.append(m)

yaya_merge = geo.createNode('merge', 'yaya_merge')
for i, y in enumerate(yayalar):
    yaya_merge.setInput(i, y)

yaya_xform = yaya_merge.createOutputNode('xform', 'yaya_xform')
yaya_xform.parm('ry').set(ROTATE)

# ===== BLOK MARKERİNG =====
bloklar = []
for i in range(BLOK_ADET):
    n = geo.createNode('box', f'blok_{i}')
    n.parm('sizex').set(BLOK_GENISLIK)
    n.parm('sizey').set(BLOK_KALINLIK)
    n.parm('sizez').set(BLOK_UZUNLUK)
    n.parm('ty').set(BLOK_KONUM_Y)
    n.parm('tz').set(BLOK_BASLANGIC + i * BLOK_ARA_MESAFE)
    n.parm('tx').set(BLOK_KONUM_X)
    m = n.createOutputNode('material')
    m.parm('shop_materialpath1').set('/mat/beyaz_cizgi')
    bloklar.append(m)

blok_merge = geo.createNode('merge', 'blok_merge')
for i, b in enumerate(bloklar):
    blok_merge.setInput(i, b)

blok_xform = blok_merge.createOutputNode('xform', 'blok_xform')
blok_xform.parm('ry').set(BLOK_ROTATE)

# ===== DREMPEL MARKERİNG =====
drempel_elemanlar = []

if DREMPEL_STIL == 0:
    # ========== T STİLİ (TUGLA) ==========

    # Sütunların toplam kapladığı genişlik (sol + orta + sag)
    toplam_sutun = T_SUTUN_SAY + 2
    sutun_toplam_genislik = (toplam_sutun - 1) * T_SUTUN_ARALIK + T_SUTUN_GENISLIK

    # Üst sıra genişliği — sütun genişliğinden küçükse otomatik artır
    ust_toplam = T_UST_SAY * (T_UST_GENISLIK + T_ARALIK) - T_ARALIK
    while ust_toplam < sutun_toplam_genislik:
        T_UST_SAY += 1
        ust_toplam = T_UST_SAY * (T_UST_GENISLIK + T_ARALIK) - T_ARALIK

    # Üst sıranın alt Z kenarı (sütunlar buradan başlar, boşluksuz)
    # Kat 0 merkezi: tz=0, alt kenarı: -T_UST_UZUNLUK/2
    # Kat 1 merkezi: tz=T_UST_UZUNLUK+T_ARALIK, alt kenarı: T_UST_UZUNLUK+T_ARALIK-T_UST_UZUNLUK/2
    # Son kat alt kenarı = (T_UST_KAT-1)*(T_UST_UZUNLUK+T_ARALIK) - T_UST_UZUNLUK/2
    # Ama üst sıra Z ekseninde negatife doğru gidiyor:
    # tz_kat = -kat * (T_UST_UZUNLUK + T_ARALIK)
    # Son kat alt kenarı = -(T_UST_KAT-1)*(T_UST_UZUNLUK+T_ARALIK) - T_UST_UZUNLUK/2
    ust_alt_z = -((T_UST_KAT - 1) * (T_UST_UZUNLUK + T_ARALIK) + T_UST_UZUNLUK / 2)

    # Üst yatay sıra — 1 veya 2 kat (Z ekseninde negatife doğru)
    for kat in range(T_UST_KAT):
        tz_kat = -(kat * (T_UST_UZUNLUK + T_ARALIK))
        for i in range(T_UST_SAY):
            tx = i * (T_UST_GENISLIK + T_ARALIK) + T_UST_GENISLIK / 2
            n = kutu(f'ust_kat{kat}_{i}', T_UST_GENISLIK, T_KALINLIK, T_UST_UZUNLUK,
                     tx=tx, ty=0.01, tz=tz_kat, mat='beyaz_cizgi')
            drempel_elemanlar.append(n)

    # Orta sutunlar sol ve sag kenar arasinda esit aralikla otomatik hizalanir
    otomatik_aralik = ust_toplam / (toplam_sutun - 1)

    # Tüm sütunlar tek döngüde — sol(0) + orta + sag(son)
    for s in range(toplam_sutun):
        if s == 0:
            tx = T_SUTUN_GENISLIK / 2
        elif s == toplam_sutun - 1:
            tx = ust_toplam - T_SUTUN_GENISLIK / 2
        else:
            tx = s * otomatik_aralik

        boy = T_UZUN_BOY if s % 2 == 0 else T_KISA_BOY
        for j in range(boy):
            tz = ust_alt_z - (j * (T_SUTUN_UZUNLUK + T_ARALIK)) - T_SUTUN_UZUNLUK / 2
            n = kutu(f'sutun_{s}_{j}', T_SUTUN_GENISLIK, T_KALINLIK, T_SUTUN_UZUNLUK,
                     tx=tx, ty=0.01, tz=tz, mat='beyaz_cizgi')
            drempel_elemanlar.append(n)

else:
    # ========== H STİLİ (HAT) ==========
    ust_toplam = (H_SUTUN_SAY + 1) * H_SUTUN_ARALIK + H_SUTUN_GENISLIK

    n = kutu('ust_hat', ust_toplam, H_YUKSEKLIK, H_UST_GENISLIK,
             tx=ust_toplam / 2, ty=0.01, tz=0, mat='beyaz_cizgi')
    drempel_elemanlar.append(n)

    ust_alt_z = -(H_UST_GENISLIK / 2)
    uzun_merkez_z = ust_alt_z - (H_UZUN_BOY / 2)
    kisa_merkez_z = ust_alt_z - (H_KISA_BOY / 2)

    toplam_sutun = H_SUTUN_SAY + 2
    for s in range(toplam_sutun):
        if s == 0:
            tx = H_SUTUN_GENISLIK / 2
        elif s == toplam_sutun - 1:
            tx = ust_toplam - H_SUTUN_GENISLIK / 2
        else:
            tx = s * H_SUTUN_ARALIK + H_SUTUN_GENISLIK / 2

        if s % 2 == 0:
            n = kutu(f'sutun_{s}', H_SUTUN_GENISLIK, H_YUKSEKLIK, H_UZUN_BOY,
                     tx=tx, ty=0.01, tz=uzun_merkez_z, mat='beyaz_cizgi')
        else:
            n = kutu(f'sutun_{s}', H_SUTUN_GENISLIK, H_YUKSEKLIK, H_KISA_BOY,
                     tx=tx, ty=0.01, tz=kisa_merkez_z, mat='beyaz_cizgi')
        drempel_elemanlar.append(n)

drempel_merge = geo.createNode('merge', 'drempel_merge')
for i, e in enumerate(drempel_elemanlar):
    drempel_merge.setInput(i, e)

drempel_xform = drempel_merge.createOutputNode('xform', 'drempel_xform')
drempel_xform.parm('tx').set(DREMPEL_KONUM_X)
drempel_xform.parm('ty').set(DREMPEL_KONUM_Y)
drempel_xform.parm('tz').set(DREMPEL_KONUM_Z)

# ===== BİRLEŞTİR =====
ok_import = geo.createNode('object_merge', 'ok_import')
ok_import.parm('objpath1').set('/obj/ok_atolyesi/material1')

merge = geo.createNode('merge', 'tum_sahne')
tum = [zemin_m, bsol, bsag, csol, csag] + kesikler + [yaya_xform] + [blok_xform] + [drempel_xform] + [ok_import]
for i, n in enumerate(tum):
    merge.setInput(i, n)

merge.setDisplayFlag(True)
geo.layoutChildren()
print('Sahne hazir!')
