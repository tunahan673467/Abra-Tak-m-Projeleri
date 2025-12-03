import time


def sayilari_oku(dosya_adi: str):
   
 
    try:
        with open(dosya_adi, "r", encoding="utf-8") as f:
            icerik = f.read()
    except FileNotFoundError:
        print("Hata: Belirtilen dosya bulunamadı.")
        raise

    # Virgülleri boşluğa çevir, sonra split ile ayır
    icerik = icerik.replace(",", " ")
    parcalar = icerik.split()

    sayilar = []
    for p in parcalar:
        try:
            # Tam sayı olarak dene
            sayi = int(p)
        except ValueError:
            try:
                # Olmazsa ondalık (float) dene
                sayi = float(p)
            except ValueError:
                raise ValueError(f"Geçersiz sayı değeri: '{p}'")
        sayilar.append(sayi)

    return sayilar


def bubble_sort_istatistikli(liste):
   
    a = liste.copy()
    n = len(a)

    karsilastirma = 0
    swap = 0

    bas = time.perf_counter()

    for i in range(n):
        for j in range(0, n - 1 - i):
            karsilastirma += 1
            if a[j] > a[j + 1]:
                # swap
                a[j], a[j + 1] = a[j + 1], a[j]
                swap += 1

    bit = time.perf_counter()
    sure_ms = (bit - bas) * 1000

    adim = karsilastirma + swap

    istatistik = {
        "karsilastirma": karsilastirma,
        "swap": swap,
        "adim": adim,
        "sure_ms": sure_ms,
    }

    return a, istatistik


def selection_sort_istatistikli(liste):
  
    a = liste.copy()
    n = len(a)

    karsilastirma = 0
    swap = 0

    bas = time.perf_counter()

    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            karsilastirma += 1
            if a[j] < a[min_index]:
                min_index = j

        # min_index farklıysa swap yap
        if min_index != i:
            a[i], a[min_index] = a[min_index], a[i]
            swap += 1

    bit = time.perf_counter()
    sure_ms = (bit - bas) * 1000

    adim = karsilastirma + swap

    istatistik = {
        "karsilastirma": karsilastirma,
        "swap": swap,
        "adim": adim,
        "sure_ms": sure_ms,
    }

    return a, istatistik


def rapor_olustur(
    sayilar,
    bubble_sirali,
    bubble_istatistik,
    selection_sirali,
    selection_istatistik,
    rapor_dosya_adi: str,
):
    
    satirlar = []

    satirlar.append("SIRALAMA ALGORITMALARI RAPORU")
    satirlar.append("=" * 40)
    satirlar.append("")
    satirlar.append(f"Girdi liste: {sayilar}")
    satirlar.append("")

    satirlar.append("1) BUBBLE SORT SONUC VE ISTATISTIKLERI")
    satirlar.append("-" * 40)
    satirlar.append(f"Sıralı liste       : {bubble_sirali}")
    satirlar.append(f"Karşılaştırma sayısı: {bubble_istatistik['karsilastirma']}")
    satirlar.append(f"Swap (yer değiştirme): {bubble_istatistik['swap']}")
    satirlar.append(f"Toplam adım        : {bubble_istatistik['adim']}")
    satirlar.append(
        "Süre (ms)          : {:.6f}".format(bubble_istatistik["sure_ms"])
    )
    satirlar.append("")

    satirlar.append("2) SELECTION SORT SONUC VE ISTATISTIKLERI")
    satirlar.append("-" * 40)
    satirlar.append(f"Sıralı liste       : {selection_sirali}")
    satirlar.append(f"Karşılaştırma sayısı: {selection_istatistik['karsilastirma']}")
    satirlar.append(f"Swap (yer değiştirme): {selection_istatistik['swap']}")
    satirlar.append(f"Toplam adım        : {selection_istatistik['adim']}")
    satirlar.append(
        "Süre (ms)          : {:.6f}".format(selection_istatistik["sure_ms"])
    )
    satirlar.append("")

    satirlar.append("3) KARSILASTIRMA")
    satirlar.append("-" * 40)

    # Adım sayısı karşılaştırması
    if bubble_istatistik["adim"] < selection_istatistik["adim"]:
        satirlar.append(
            f"Adım sayısı bakımından daha verimli olan: BUBBLE SORT "
            f"({bubble_istatistik['adim']} adım < {selection_istatistik['adim']} adım)"
        )
    elif bubble_istatistik["adim"] > selection_istatistik["adim"]:
        satirlar.append(
            f"Adım sayısı bakımından daha verimli olan: SELECTION SORT "
            f"({selection_istatistik['adim']} adım < {bubble_istatistik['adim']} adım)"
        )
    else:
        satirlar.append("Adım sayıları bakımından iki algoritma eşit.")

    # Süre karşılaştırması
    b_sure = bubble_istatistik["sure_ms"]
    s_sure = selection_istatistik["sure_ms"]

    if b_sure < s_sure:
        satirlar.append(
            "Süre bakımından daha hızlı olan       : BUBBLE SORT "
            "({:.6f} ms < {:.6f} ms)".format(b_sure, s_sure)
        )
    elif b_sure > s_sure:
        satirlar.append(
            "Süre bakımından daha hızlı olan       : SELECTION SORT "
            "({:.6f} ms < {:.6f} ms)".format(s_sure, b_sure)
        )
    else:
        satirlar.append("Süre bakımından iki algoritma eşit görünüyor.")

    satirlar.append("")
    satirlar.append("Not: Süreler, çalıştırılan bilgisayarın hızına göre değişebilir.")

    metin = "\n".join(satirlar) + "\n"

    with open(rapor_dosya_adi, "w", encoding="utf-8") as f:
        f.write(metin)


def main():
    giris_dosya_adi = input(
        "Sayı listesini içeren metin dosyasının adını giriniz (ör: sayilar.txt): "
    ).strip()

    try:
        sayilar = sayilari_oku(giris_dosya_adi)
    except Exception as e:
        print("Hata oluştu:", e)
        return

    print("Okunan sayılar:", sayilar)

    # Bubble Sort
    bubble_sirali, bubble_istatistik = bubble_sort_istatistikli(sayilar)

    # Selection Sort
    selection_sirali, selection_istatistik = selection_sort_istatistikli(sayilar)

    # Rapor dosya adı
    rapor_dosya_adi = input(
        "Raporun yazılacağı dosya adını giriniz (ör: rapor.txt): "
    ).strip()
    if not rapor_dosya_adi:
        rapor_dosya_adi = "siralamalar_rapor.txt"

    rapor_olustur(
        sayilar,
        bubble_sirali,
        bubble_istatistik,
        selection_sirali,
        selection_istatistik,
        rapor_dosya_adi,
    )

    print(f"Rapor oluşturuldu: {rapor_dosya_adi}")


if __name__ == "__main__":
    main()
