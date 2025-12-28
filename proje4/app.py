from flask import Flask, request, jsonify
import json
import os


app = Flask(__name__)


DATA_FILE = "ucus_log.json"

def load_logs():
    """Uçuş loglarını dosyadan okur."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

@app.route('/get_flight', methods=['POST'])
def get_flight():
    # 1. İstekten ID'yi al (Örn: 1 numaralı takım)
    istek_verisi = request.json
    takim_id = istek_verisi.get("id")
    
    if takim_id is None:
        return jsonify({"durum": "hata", "mesaj": "ID gönderilmedi"}), 400
    
    # Gelen ID string olabilir, garanti olsun diye integer'a çeviriyoruz
    try:
        takim_id = int(takim_id)
    except ValueError:
        return jsonify({"durum": "hata", "mesaj": "ID sayı olmalı"}), 400

    ham_veri = load_logs()
    rota_noktalari = []
    
    # Karmaşık JSON içinde döngüyle veriyi ara
    
    for zaman_dilimi in ham_veri:
        if "konumBilgileri" in zaman_dilimi:
            for iha in zaman_dilimi["konumBilgileri"]:
                # İstenen takım numarasını bulduk mu?
                if iha.get("takim_numarasi") == takim_id:
                    # Bulduysak koordinatlarını listeye ekle
                    nokta = {
                        "lat": iha.get("iha_enlem"),
                        "lon": iha.get("iha_boylam"),
                        "alt": iha.get("iha_irtifa")
                    }
                    rota_noktalari.append(nokta)
    
    # Sonucu kontrol et ve gönder
    if not rota_noktalari:
        return jsonify({"durum": "hata", "mesaj": f"ID {takim_id} için uçuş kaydı bulunamadı."}), 404
        
    cevap = {
        "durum": "basarili",
        "nokta_sayisi": len(rota_noktalari),
        "baslangic": rota_noktalari[0],
        "bitis": rota_noktalari[-1],
        "rota": rota_noktalari
    }
    
    return jsonify(cevap)

if __name__ == '__main__':
    print(f" Uçuş Sunucusu Başlatılıyor... Dosya: {DATA_FILE}")
    app.run(debug=True, port=5000)