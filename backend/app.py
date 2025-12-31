from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import requests  # <-- Ödev için eklenen kütüphane

app = Flask(__name__)
CORS(app)

# MongoDB Bağlantısı
client = MongoClient('mongodb://mongodb:27017/')
db = client.ymg_veritabani
users_col = db.users

if users_col.count_documents({"kullanici_adi": "admin"}) == 0:
    users_col.insert_one({"kullanici_adi": "admin", "sifre": "12345"})

# --- ÖDEV ŞARTI: PUBLIC API SORGUSU ---
@app.route('/public-data', methods=['GET'])
def get_external_api():
    """Dış dünyadaki ücretsiz bir API'ye istek atar."""
    try:
        # Örnek: JSONPlaceholder'dan veri çekiyoruz
        url = "https://jsonplaceholder.typicode.com/todos/1"
        response = requests.get(url, timeout=5)
        return jsonify({
            "durum": "basarili",
            "kaynak": "jsonplaceholder",
            "veri": response.json()
        }), 200
    except Exception as e:
        return jsonify({"durum": "hata", "mesaj": str(e)}), 500

# --- DİĞER ENDPOINTLER ---
@app.route('/register', methods=['POST'])
def handle_register():
    data = request.get_json()
    if users_col.find_one({"kullanici_adi": data.get('kullanici_adi')}):
        return jsonify({"durum": "hata", "mesaj": "Kullanıcı zaten var"}), 409
    users_col.insert_one(data)
    return jsonify({"durum": "basarili", "mesaj": "Kayıt başarılı"}), 201

@app.route('/login', methods=['POST'])
def handle_login():
    data = request.get_json()
    user = users_col.find_one({"kullanici_adi": data.get('kullanici_adi'), "sifre": data.get('sifre')})
    if user:
        return jsonify({"durum": "basarili", "mesaj": "Giriş Başarılı"}), 200
    return jsonify({"durum": "hata", "mesaj": "Hatalı Bilgi"}), 401

@app.route('/status', methods=['GET'])
def health_check():
    return jsonify({"durum": "aktif"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)