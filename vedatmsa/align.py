# Needleman-Wunsch global alignment
# İki diziyi en iyi şekilde hizalar (gap ekleyerek)

ESLEME = 1      # aynı karakter
UYUMSUZ = -1    # farklı karakter
GAP = -2        # boşluk cezası


def needleman_wunsch(dizi1, dizi2):
    m, n = len(dizi1), len(dizi2)

    tablo = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        tablo[i][0] = i * GAP
    for j in range(n + 1):
        tablo[0][j] = j * GAP

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            eslesme = ESLEME if dizi1[i-1].upper() == dizi2[j-1].upper() else UYUMSUZ
            capraz = tablo[i-1][j-1] + eslesme
            yukari = tablo[i-1][j] + GAP
            sol    = tablo[i][j-1] + GAP
            tablo[i][j] = max(capraz, yukari, sol)

    hiz1, hiz2 = [], []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            eslesme = ESLEME if dizi1[i-1].upper() == dizi2[j-1].upper() else UYUMSUZ
            if tablo[i][j] == tablo[i-1][j-1] + eslesme:
                hiz1.append(dizi1[i-1])
                hiz2.append(dizi2[j-1])
                i -= 1; j -= 1
            elif tablo[i][j] == tablo[i-1][j] + GAP:
                hiz1.append(dizi1[i-1])
                hiz2.append('-')
                i -= 1
            else:
                hiz1.append('-')
                hiz2.append(dizi2[j-1])
                j -= 1
        elif i > 0:
            hiz1.append(dizi1[i-1]); hiz2.append('-'); i -= 1
        else:
            hiz1.append('-'); hiz2.append(dizi2[j-1]); j -= 1

    return ''.join(reversed(hiz1)), ''.join(reversed(hiz2))


def konsensus_al(diziler):
    # Gruptaki dizilerin konsensüsünü çıkar
    if not diziler:
        return ""
    uzunluk = len(diziler[0])
    sonuc = []
    for pos in range(uzunluk):
        sutun = [d[pos] for d in diziler if pos < len(d) and d[pos] != '-']
        if sutun:
            sonuc.append(max(set(sutun), key=sutun.count))
        else:
            sonuc.append('-')
    return ''.join(sonuc)


def gap_ekle(diziler, referans_hizalanmis):
    # referans_hizalanmis'teki gap pozisyonlarına göre gruba gap ekle
    sonuc = []
    for dizi in diziler:
        temiz = list(dizi.replace('-', ''))
        yeni = []
        idx = 0
        for c in referans_hizalanmis:
            if c == '-':
                yeni.append('-')
            else:
                yeni.append(temiz[idx] if idx < len(temiz) else '-')
                idx += 1
        # kalan karakterler
        while idx < len(temiz):
            yeni.append(temiz[idx])
            idx += 1
        sonuc.append(''.join(yeni))
    return sonuc


def iki_grubu_hizala(grup1, grup2):
    # Konsensüsü temsilci olarak kullan
    temsilci1 = konsensus_al(grup1)
    temsilci2 = konsensus_al(grup2)

    hiz1, hiz2 = needleman_wunsch(temsilci1, temsilci2)

    yeni_grup1 = gap_ekle(grup1, hiz1)
    yeni_grup2 = gap_ekle(grup2, hiz2)

    # Uzunlukları eşitle
    max_uzunluk = max(len(d) for d in yeni_grup1 + yeni_grup2)
    yeni_grup1 = [d.ljust(max_uzunluk, '-') for d in yeni_grup1]
    yeni_grup2 = [d.ljust(max_uzunluk, '-') for d in yeni_grup2]

    return yeni_grup1, yeni_grup2


def progressive_hizala(agac, dizi_sozlugu):
    if agac.yaprak_mi():
        return [dizi_sozlugu[agac.isim]]

    sol_diziler = progressive_hizala(agac.sol, dizi_sozlugu)
    sag_diziler = progressive_hizala(agac.sag, dizi_sozlugu)

    yeni_sol, yeni_sag = iki_grubu_hizala(sol_diziler, sag_diziler)
    return yeni_sol + yeni_sag
