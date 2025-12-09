# 1. TEMEL İMAJ: Python uygulaması olduğu için resmi Python imajını kullan
FROM python:3.11-slim

# 2. ÇALIŞMA DİZİNİ: Container içinde /app adında bir klasör oluştur ve oraya geç
WORKDIR /app

# 3. BAĞIMLILIKLAR: Flask ve gunicorn'u kur
# 3. BAĞIMLILIKLAR: Flask, gunicorn VE flask-cors'u kur
RUN pip install Flask gunicorn flask-cors
# 4. KODU KOPYALA: Docker'ın önbelleğini geçersiz kılmak için bu satır gereklidir.
# Bu sayede app.py değişmese bile kopyalama işlemi yeniden yapılır.
RUN echo "Build forced on $(date)" >> /tmp/forced_build_timestamp

# 5. KODLARI KOPYALA: app.py dosyasını container'daki /app dizinine kopyala
COPY app.py .
COPY swagger.yaml . 

# 6. PORTU AÇ
EXPOSE 5000

# 7. ÇEVRE AYARLARI
ENV FLASK_RUN_HOST=0.0.0.0

# 8. ÇALIŞTIRMA KOMUTU
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]