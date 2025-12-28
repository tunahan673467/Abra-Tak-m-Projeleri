import json
import time


def oku_ve_kume_donustur(dosya_adi: str):
    """JSON dosyasını okuyup list1 ve list2'yi kümeye dönüştürür."""
    with open(dosya_adi, "r", encoding="utf-8") as f:
        veri = json.load(f)

    liste1 = veri.get("list1", [])
    liste2 = veri.get("list2", [])

    return set(liste1), set(liste2)


def kume_islemleri_ve_sure_hesapla(kume1, kume2):
    """Birleşim, kesişim ve fark işlemlerini yapar, süreleri milisaniye cinsinden döndürür."""
    islemler = {}

    # Birleşim
    bas = time.perf_counter()
    birlesim = sorted(kume1.union(kume2))
    bit = time.perf_counter()
    islemler["birlesim"] = {
        "sonuc": birlesim,
        "sure_milisaniye": round((bit - bas) * 1000, 6),
    }

    # Kesişim
    bas = time.perf_counter()
    kesisim = sorted(kume1.intersection(kume2))
    bit = time.perf_counter()
    islemler["kesisim"] = {
        "sonuc": kesisim,
        "sure_milisaniye": round((bit - bas) * 1000, 6),
    }

    # Fark (kume1 - kume2)
    bas = time.perf_counter()
    fark1 = sorted(kume1.difference(kume2))
    bit = time.perf_counter()
    islemler["fark_kume1_eksi_kume2"] = {
        "sonuc": fark1,
        "sure_milisaniye": round((bit - bas) * 1000, 6),
    }

    # Fark (kume2 - kume1)
    bas = time.perf_counter()
    fark2 = sorted(kume2.difference(kume1))
    bit = time.perf_counter()
    islemler["fark_kume2_eksi_kume1"] = {
        "sonuc": fark2,
        "sure_milisaniye": round((bit - bas) * 1000, 6),
    }

    return islemler




def liste_yatay(liste):
    """stringe döndürme"""
    return "[" + ", ".join(str(x) for x in liste) + "]"


def ozel_json_yaz(kume1, kume2, islemler, cikti_dosya_adi: str):
 
    kume1_str = liste_yatay(sorted(kume1))
    kume2_str = liste_yatay(sorted(kume2))

    
    sirali_anahtarlar = [
        "birlesim",
        "kesisim",
        "fark_kume1_eksi_kume2",
        "fark_kume2_eksi_kume1",
    ]

    satirlar = []
    satirlar.append("{")
    satirlar.append(f'    "kume1": {kume1_str},')
    satirlar.append(f'    "kume2": {kume2_str},')
    satirlar.append(f'    "islemler": {{')

    for i, anahtar in enumerate(sirali_anahtarlar):
        veri = islemler[anahtar]
        sonuc_str = liste_yatay(veri["sonuc"])
        sure_str = str(veri["sure_milisaniye"])

        virgul_islem = "," if i < len(sirali_anahtarlar) - 1 else ""

        satirlar.append(f'        "{anahtar}": {{')
        satirlar.append(f'            "sonuc": {sonuc_str},')
        satirlar.append(f'            "sure_milisaniye": {sure_str}')
        satirlar.append(f'        }}{virgul_islem}')

    satirlar.append("    }")
    satirlar.append("}")

    icerik = "\n".join(satirlar) + "\n"

    with open(cikti_dosya_adi, "w", encoding="utf-8") as f:
        f.write(icerik)


# ------------------------------------------------------------------- #

def main():
    girdi_dosya_adi = input("Giriş JSON dosyasının adını giriniz (ör: girdi.json): ").strip()

    try:
        kume1, kume2 = oku_ve_kume_donustur(girdi_dosya_adi)
    except FileNotFoundError:
        print("Hata: Belirtilen dosya bulunamadı.")
        return
    except json.JSONDecodeError:
        print("Hata: Dosya geçerli bir JSON formatında değil.")
        return

    print("Kümeler başarıyla oluşturuldu.")
    print("Küme 1:", kume1)
    print("Küme 2:", kume2)

    islemler = kume_islemleri_ve_sure_hesapla(kume1, kume2)

    cikti_dosya_adi = input("Sonuçların yazılacağı JSON dosyasının adını giriniz (ör: cikti.json): ").strip()
    if not cikti_dosya_adi:
        cikti_dosya_adi = "sonuc.json"

    ozel_json_yaz(kume1, kume2, islemler, cikti_dosya_adi)

    print(f"İşlemler tamamlandı. Sonuçlar '{cikti_dosya_adi}' dosyasına yazıldı.")


if __name__ == "__main__":
    main()
