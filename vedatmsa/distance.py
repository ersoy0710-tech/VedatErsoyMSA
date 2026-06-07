# k-mer mesafe hesabı
# İki dizi arasındaki benzerliği hızlıca ölçmek için kullanılır
# Örnek: k=3 ise "ATCG" -> ["ATC", "TCG"]

def kmer_mesafe(dizi1, dizi2, k=3):
    def kmer_bul(dizi, k):
        kmers = {}
        for i in range(len(dizi) - k + 1):
            parca = dizi[i:i+k]
            kmers[parca] = kmers.get(parca, 0) + 1
        return kmers

    kmers1 = kmer_bul(dizi1.upper(), k)
    kmers2 = kmer_bul(dizi2.upper(), k)

    tum_kmers = set(kmers1) | set(kmers2)
    ortak = sum(min(kmers1.get(kmer, 0), kmers2.get(kmer, 0)) for kmer in tum_kmers)
    toplam = sum(kmers1.values()) + sum(kmers2.values())

    if toplam == 0:
        return 1.0

    benzerlik = (2 * ortak) / toplam
    return 1.0 - benzerlik  # mesafe = 1 - benzerlik


def mesafe_matrisi_olustur(diziler, k=3):
    # diziler: [("isim", "ATCG..."), ...]
    n = len(diziler)
    matris = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            d = kmer_mesafe(diziler[i][1], diziler[j][1], k)
            matris[i][j] = d
            matris[j][i] = d

    return matris
