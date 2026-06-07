# MUSCLE - Multiple Sequence Alignment
# 3 aşama: kaba hizalama -> iyileştirilmiş ağaç -> refinement

from .distance import mesafe_matrisi_olustur
from .tree import upgma
from .align import progressive_hizala, iki_grubu_hizala


def hizalama_skoru(diziler):
    # Toplam match sayısını skor olarak kullan
    if not diziler or len(diziler) < 2:
        return 0
    skor = 0
    uzunluk = len(diziler[0])
    for pos in range(uzunluk):
        sutun = [dizi[pos] for dizi in diziler if pos < len(dizi)]
        en_sik = max(set(sutun), key=sutun.count)
        if en_sik != '-':
            skor += sutun.count(en_sik)
    return skor


def refine(isimler, diziler, tekrar=3):
    # Aşama 3: hizalamayı ikiye bölüp tekrar hizala, iyileşiyorsa güncelle
    guncel = list(diziler)
    guncel_skor = hizalama_skoru(guncel)

    for _ in range(tekrar):
        n = len(guncel)
        if n < 2:
            break
        ortadan = n // 2
        grup1 = guncel[:ortadan]
        grup2 = guncel[ortadan:]

        yeni1, yeni2 = iki_grubu_hizala(grup1, grup2)
        yeni = yeni1 + yeni2
        yeni_skor = hizalama_skoru(yeni)

        if yeni_skor > guncel_skor:
            guncel = yeni
            guncel_skor = yeni_skor

    return guncel


def muscle(diziler, verbose=False):
    """
    MUSCLE ile çoklu dizi hizalaması yapar.

    diziler: [("isim", "ATCG..."), ...]
    Döndürür: [("isim", "hizalanmis_dizi"), ...]
    """
    if len(diziler) < 2:
        raise ValueError("En az 2 dizi gerekli.")

    isimler = [isim for isim, _ in diziler]
    dizi_sozlugu = {isim: dizi for isim, dizi in diziler}

    # --- AŞAMA 1: k-mer mesafesiyle kaba hizalama ---
    if verbose:
        print("Aşama 1: k-mer mesafe matrisi hesaplanıyor...")
    matris = mesafe_matrisi_olustur(diziler)

    if verbose:
        print("Aşama 1: UPGMA ağacı oluşturuluyor...")
    agac = upgma(isimler, matris)

    if verbose:
        print("Aşama 1: Progressive hizalama yapılıyor...")
    hizalanmis = progressive_hizala(agac, dizi_sozlugu)

    # --- AŞAMA 2: Hizalanmış dizilerle yeni mesafe matrisi ---
    if verbose:
        print("Aşama 2: Yeni mesafe matrisi hesaplanıyor...")
    hizalanmis_diziler = list(zip(isimler, hizalanmis))
    matris2 = mesafe_matrisi_olustur(hizalanmis_diziler)

    if verbose:
        print("Aşama 2: Yeni UPGMA ağacı ve hizalama...")
    agac2 = upgma(isimler, matris2)
    hizalanmis = progressive_hizala(agac2, dizi_sozlugu)

    # --- AŞAMA 3: Refinement ---
    if verbose:
        print("Aşama 3: Refinement yapılıyor...")
    hizalanmis = refine(isimler, hizalanmis)

    if verbose:
        print(f"Tamamlandı! Skor: {hizalama_skoru(hizalanmis)}")

    return list(zip(isimler, hizalanmis))
