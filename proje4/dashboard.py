import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from mpl_toolkits.mplot3d import Axes3D 

class FlightWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("İHA Uçuş Logu Analiz Sistemi")
        self.setGeometry(100, 100, 1200, 800)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # --- ÜST PANEL (Giriş ve Buton) ---
        input_layout = QHBoxLayout()
        
        lbl_id = QLabel("Uçuş ID (Takım No):")
        lbl_id.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Örn: 1, 2, 19...")
        self.input_id.setStyleSheet("font-size: 14px; padding: 5px;")
        
        self.btn_sorgula = QPushButton("Rotayı Çiz")
        self.btn_sorgula.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 8px;")
        self.btn_sorgula.clicked.connect(self.sorgula)
        
        input_layout.addWidget(lbl_id)
        input_layout.addWidget(self.input_id)
        input_layout.addWidget(self.btn_sorgula)
        layout.addLayout(input_layout)

        # --- BİLGİ PANELİ ---
        self.lbl_info = QLabel("Sistem Hazır. Lütfen bir Takım ID girip sorgulayın.")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setStyleSheet("font-size: 12px; color: #333; margin: 10px; padding: 10px; border: 1px solid #ddd; background: #f9f9f9;")
        layout.addWidget(self.lbl_info)

        # --- GRAFİK ALANI (Matplotlib) ---
        self.figure = Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def sorgula(self):
        takim_id_str = self.input_id.text().strip()
        if not takim_id_str.isdigit():
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir sayı giriniz.")
            return

        takim_id = int(takim_id_str)
        self.lbl_info.setText("Veriler sunucudan çekiliyor, lütfen bekleyin...")
        QApplication.processEvents() # Arayüzün donmasını engelle
        
        try:
            # Flask Sunucusuna Bağlan
            url = "http://127.0.0.1:5000/get_flight"
            payload = {"id": takim_id}
            response = requests.post(url, json=payload)
            
            if response.status_code == 404:
                QMessageBox.warning(self, "Bulunamadı", "Bu ID'ye ait uçuş kaydı yok.")
                self.lbl_info.setText("Sonuç bulunamadı.")
                return
            
            if response.status_code != 200:
                QMessageBox.critical(self, "Hata", f"Sunucu hatası: {response.status_code}")
                return

            data = response.json()
            if data["durum"] == "basarili":
                self.grafik_ciz(data, takim_id)
                self.bilgi_guncelle(data)
            else:
                QMessageBox.warning(self, "Hata", data.get("mesaj", "Bilinmeyen hata"))

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Bağlantı Hatası", "Flask sunucusu kapalı olabilir!\n'python app.py' komutunu çalıştırdınız mı?")
            self.lbl_info.setText("Hata: Sunucuya bağlanılamadı.")

    def bilgi_guncelle(self, data):
        count = data["nokta_sayisi"]
        start = data["baslangic"]
        end = data["bitis"]
        
        bilgi_metni = (
            f"✅ SORGULAMA BAŞARILI\n"
            f"Toplam Veri Noktası: {count}\n"
            f"🛫 Başlangıç: Enlem {start['lat']} | Boylam {start['lon']} | İrtifa {start['alt']}m\n"
            f"🛬 Bitiş: Enlem {end['lat']} | Boylam {end['lon']} | İrtifa {end['alt']}m"
        )
        self.lbl_info.setText(bilgi_metni)

    def grafik_ciz(self, data, takim_id):
        rota = data["rota"]
        lats = [p["lat"] for p in rota]
        lons = [p["lon"] for p in rota]
        alts = [p["alt"] for p in rota]

        self.figure.clear()
        
        # Grafik alanını oluştur
        ax = self.figure.add_subplot(111, projection='3d')
        
        # Rotayı Çiz
        ax.plot(lats, lons, alts, label=f'Takım {takim_id}', color='blue', linewidth=2)
        ax.scatter(lats, lons, alts, c='red', s=15, alpha=0.6) # Ara noktalar

        # Başlangıç ve Bitiş
        ax.scatter(lats[0], lons[0], alts[0], color='green', s=100, label='Başlangıç', edgecolors='black')
        ax.scatter(lats[-1], lons[-1], alts[-1], color='black', s=100, marker='s', label='Bitiş')

        # --- EKSEN AYARLARI  ---
        
        
        ax.ticklabel_format(useOffset=False, style='plain')

   
        ax.tick_params(axis='x', labelsize=8, rotation=20)
        ax.tick_params(axis='y', labelsize=8, rotation=20)
        ax.tick_params(axis='z', labelsize=8)

        #  Eksen İsimleri ve Başlık
        ax.set_xlabel('Enlem', labelpad=10)
        ax.set_ylabel('Boylam', labelpad=10)
        ax.set_zlabel('İrtifa (m)', labelpad=10)
        ax.set_title(f"Takım {takim_id} - Uçuş Rotası")
        
        # Efsane (Legend) kutusu
        ax.legend()
        
        # Çizimi güncelle
        self.figure.tight_layout() # Boşlukları otomatik ayarlar
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FlightWindow()
    window.show()
    sys.exit(app.exec_())