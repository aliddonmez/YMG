# 1. Temel İmaj
FROM python:3.11-slim

# 2. Çalışma Dizini
WORKDIR /app

# 3. Bağımlılıklar (Flask, CORS, Gunicorn ve MongoDB sürücüsü)
RUN pip install Flask gunicorn flask-cors pymongo

# 4. Önbellek Kırıcı (Kod değişikliklerini anında yansıtmak için)
RUN echo "Build forced on $(date)" >> /tmp/forced_build_timestamp

# 5. Dosyaları Kopyala
COPY app.py .
COPY swagger.yaml . 

# 6. Port ve Çalıştırma
EXPOSE 5000
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]