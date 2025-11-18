# 1. TEMEL İMAJ: Python uygulaması olduğu için resmi Python imajını kullan
FROM python:3.11-slim

# 2. ÇALIŞMA DİZİNİ: Container içinde /app adında bir klasör oluştur ve oraya geç
WORKDIR /app

# 3. BAĞIMLILIKLAR: Flask kurmak için requirements.txt dosyasına ihtiyacımız var.
# Flask kütüphanesini requirements.txt dosyasına eklemeliyiz.
# Bu projede requirements.txt olmadığı için, kurulumu doğrudan RUN komutu ile yapıyoruz.
# Ancak profesyonel bir yaklaşım için requirements.txt kullanmak daha doğrudur.

# Projeniz sadece Flask kullandığı için, bağımlılığı doğrudan kuruyoruz:
RUN pip install Flask gunicorn

# 4. KODU KOPYALA: app.py dosyasını container'daki /app dizinine kopyala
COPY app.py .
COPY swagger.yaml . 

# 5. PORTU AÇ: Uygulamanın dinlediği portu (5000) Docker'a bildir
EXPOSE 5000

# 6. ÇEVRE AYARLARI: Flask'ın dışarıdan erişilebilmesi için host'u ayarla
# (Not: app.py'niz zaten 5000 portunda çalışıyor)
ENV FLASK_RUN_HOST=0.0.0.0

# 7. ÇALIŞTIRMA KOMUTU: Container başlatıldığında Gunicorn ile uygulamayı çalıştır
# Gunicorn, Flask'ın standart geliştirme sunucusundan daha güvenli ve sağlamdır.
# app:app komutu, 'app.py' dosyasındaki 'app' objesini çalıştır demektir.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]