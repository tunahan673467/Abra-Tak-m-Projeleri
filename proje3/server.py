import zmq
import json
import os

# Veri tabanı dosyamız (İçinde veriler olan ornek.json)
DB_FILE = "ornek.json"

# Dosya yoksa oluştur (Hata almamak için güvenlik önlemi)
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_books():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_books(books):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print(" Kütüphane Sunucusu Aktif! (Port: 5555)")

    while True:
        message = socket.recv_json()
        print(f"📩 Gelen İstek: {message}")
        
        komut = message.get("komut")
        cevap = {"durum": "hata", "mesaj": "Bilinmeyen komut"}
        
        kitaplar = load_books()

        # --- KİTAP ARAMA ---
        if komut == "ara":
            aranan = message.get("kitap_adi", "").lower()
            sonuc = [k for k in kitaplar if aranan in k["ad"].lower()]
            cevap = {"durum": "basarili", "veriler": sonuc}

        # --- KİTAP EKLEME ---
        elif komut == "ekle":
            yeni_kitap = {
                "id": len(kitaplar) + 1,
                "ad": message.get("kitap_adi"),
                "yazar": message.get("yazar"),
                "durum": "rafta"
            }
            kitaplar.append(yeni_kitap)
            save_books(kitaplar)
            cevap = {"durum": "basarili", "mesaj": "Kitap eklendi."}

        
        elif komut == "odunc_al":
            aranan_ad = message.get("kitap_adi", "").lower().strip()
            islem_yapildi = False
            
            for k in kitaplar:
                
                if k["ad"].lower() == aranan_ad:
                    if k["durum"] == "rafta":
                        k["durum"] = "odunc_verildi"
                        save_books(kitaplar)
                        cevap = {"durum": "basarili", "mesaj": f"'{k['ad']}' kitabı size verildi. İyi okumalar!"}
                        islem_yapildi = True
                    else:
                        cevap = {"durum": "hata", "mesaj": f"'{k['ad']}' kitabı şu an başkasında!"}
                        islem_yapildi = True
                    break 
            if not islem_yapildi:
                cevap = {"durum": "hata", "mesaj": "Bu isimde bir kitap bulunamadı."}

        
        
        elif komut == "teslim_et":
            aranan_ad = message.get("kitap_adi", "").lower().strip()
            islem_yapildi = False

            for k in kitaplar:
                if k["ad"].lower() == aranan_ad:
                    if k["durum"] == "odunc_verildi":
                        k["durum"] = "rafta"
                        save_books(kitaplar)
                        cevap = {"durum": "basarili", "mesaj": f"'{k['ad']}' iade alındı. Teşekkürler!"}
                        islem_yapildi = True
                    else:
                        cevap = {"durum": "hata", "mesaj": f"'{k['ad']}' zaten kütüphane rafında duruyor."}
                        islem_yapildi = True
                    break
            
            if not islem_yapildi:
                cevap = {"durum": "hata", "mesaj": "Kütüphanemize ait böyle bir kitap yok."}

        socket.send_json(cevap)

if __name__ == "__main__":
    main()