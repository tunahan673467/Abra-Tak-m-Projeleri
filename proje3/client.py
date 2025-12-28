import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    print(" Gelişmiş Kütüphane Sistemine Hoşgeldiniz!")

    while True:
        print("\n---  İŞLEM MENÜSÜ ---")
        print("1. Kitap Ekle")
        print("2. Kitap Ara")
        print("3. Kitap Ödünç Al (İsimle)")
        print("4. Kitap Teslim Et / İade (İsimle)")
        print("5. Çıkış")
        secim = input("Seçiminiz (1-5): ")

        istek_paketi = {}

        if secim == "1":
            ad = input("Kitap Adı: ")
            yazar = input("Yazar: ")
            istek_paketi = {"komut": "ekle", "kitap_adi": ad, "yazar": yazar}

        elif secim == "2":
            ad = input("Aranacak Kitap Adı: ")
            istek_paketi = {"komut": "ara", "kitap_adi": ad}

        elif secim == "3":
            # Artık ID yerine isim soruyoruz
            ad = input("Ödünç Almak İstediğiniz Kitabın Tam Adı: ")
            istek_paketi = {"komut": "odunc_al", "kitap_adi": ad}

        elif secim == "4":
            
            ad = input("İade Edeceğiniz Kitabın Adı: ")
            istek_paketi = {"komut": "teslim_et", "kitap_adi": ad}

        elif secim == "5":
            break
        else:
            print("Geçersiz seçim.")
            continue

       
        print("⏳ İşlem yapılıyor...")
        socket.send_json(istek_paketi)
        sunucu_cevabi = socket.recv_json()
        
        # Cevabı Ekrana Bas
        if sunucu_cevabi["durum"] == "basarili":
            print(f"✅ {sunucu_cevabi.get('mesaj', 'İşlem Başarılı')}")
            
            # Eğer arama işlemiyse detayları dök
            if secim == "2" and "veriler" in sunucu_cevabi:
                for k in sunucu_cevabi["veriler"]:
                    print(f"    {k['ad']} - {k['yazar']} [Durum: {k['durum']}]")
        else:
            print(f" HATA: {sunucu_cevabi.get('mesaj')}")

if __name__ == "__main__":
    main()