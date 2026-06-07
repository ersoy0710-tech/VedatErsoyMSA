# UPGMA algoritması ile rehber ağaç oluşturma
# En yakın iki diziyi bulup birleştirir, ta ki tek ağaç kalana kadar

import copy

class Dugum:
    def __init__(self, isim=None, sol=None, sag=None):
        self.isim = isim  # yaprak dugum ise dizi adi
        self.sol = sol
        self.sag = sag

    def yaprak_mi(self):
        return self.sol is None and self.sag is None

    def yapraklari_getir(self):
        if self.yaprak_mi():
            return [self.isim]
        yapraklar = []
        if self.sol:
            yapraklar += self.sol.yapraklari_getir()
        if self.sag:
            yapraklar += self.sag.yapraklari_getir()
        return yapraklar


def upgma(isimler, matris):
    dugumler = [Dugum(isim=isim) for isim in isimler]
    mat = copy.deepcopy(matris)
    kume_boyutlari = [1] * len(isimler)

    while len(dugumler) > 1:
        n = len(dugumler)

        # En kucuk mesafeyi bul
        min_dist = float('inf')
        min_i, min_j = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if mat[i][j] < min_dist:
                    min_dist = mat[i][j]
                    min_i, min_j = i, j

        # Yeni ic dugum olustur
        yeni = Dugum(sol=dugumler[min_i], sag=dugumler[min_j])
        boy_i = kume_boyutlari[min_i]
        boy_j = kume_boyutlari[min_j]
        yeni_boy = boy_i + boy_j

        # Yeni mesafeleri hesapla (agirlikli ortalama)
        yeni_mesafeler = []
        for k in range(n):
            if k == min_i or k == min_j:
                continue
            d = (boy_i * mat[min_i][k] + boy_j * mat[min_j][k]) / yeni_boy
            yeni_mesafeler.append(d)

        # Guncelle
        kalan = [k for k in range(n) if k != min_i and k != min_j]
        dugumler = [dugumler[k] for k in kalan] + [yeni]
        kume_boyutlari = [kume_boyutlari[k] for k in kalan] + [yeni_boy]

        yeni_mat = []
        for i, ki in enumerate(kalan):
            satir = [mat[ki][kj] for kj in kalan] + [yeni_mesafeler[i]]
            yeni_mat.append(satir)
        yeni_mat.append(yeni_mesafeler + [0.0])
        mat = yeni_mat

    return dugumler[0]
