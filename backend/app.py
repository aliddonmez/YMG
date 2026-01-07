from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from flasgger import Swagger
import requests
import os
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

# ----------------------------
# Swagger (OpenAPI) UI
# ----------------------------
# swagger.yaml dosyasını kullanarak /apidocs/ altında Swagger UI sağlar
Swagger(app, template_file="swagger.yaml")

# ----------------------------
# MongoDB Bağlantısı
# ----------------------------
client = MongoClient('mongodb://mongodb:27017/')
db = client.ymg_veritabani
users_col = db.users

# İlk kullanıcı
if users_col.count_documents({"kullanici_adi": "admin"}) == 0:
    users_col.insert_one({"kullanici_adi": "admin", "sifre": "12345"})

# ----------------------------
# JWT Ayarları
# ----------------------------
JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
JWT_ALG = "HS256"
JWT_EXPIRE_MIN = int(os.getenv("JWT_EXPIRE_MIN", "30"))

def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRE_MIN),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"durum": "hata", "mesaj": "Bearer token gerekli"}), 401

        token = auth.split(" ", 1)[1].strip()
        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        except jwt.ExpiredSignatureError:
            return jsonify({"durum": "hata", "mesaj": "Token süresi doldu"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"durum": "hata", "mesaj": "Geçersiz token"}), 401

        request.user = decoded.get("sub")
        return f(*args, **kwargs)
    return decorated


# ----------------------------
# Public endpoint (TOKEN GEREKMEZ)
# ----------------------------
@app.route('/public-data', methods=['GET'])
def get_external_api():
    """Dış dünyadaki ücretsiz bir API'ye istek atar."""
    try:
        url = "https://jsonplaceholder.typicode.com/todos/1"
        response = requests.get(url, timeout=5)
        return jsonify({
            "durum": "basarili",
            "kaynak": "jsonplaceholder",
            "veri": response.json()
        }), 200
    except Exception as e:
        return jsonify({"durum": "hata", "mesaj": str(e)}), 500


@app.route('/register', methods=['POST'])
def handle_register():
    data = request.get_json() or {}
    if not data.get("kullanici_adi") or not data.get("sifre"):
        return jsonify({"durum": "hata", "mesaj": "kullanici_adi ve sifre zorunlu"}), 400

    if users_col.find_one({"kullanici_adi": data.get('kullanici_adi')}):
        return jsonify({"durum": "hata", "mesaj": "Kullanıcı zaten var"}), 409

    users_col.insert_one({"kullanici_adi": data["kullanici_adi"], "sifre": data["sifre"]})
    return jsonify({"durum": "basarili", "mesaj": "Kayıt başarılı"}), 201


# ----------------------------
# Login -> JWT üretir (TOKEN GEREKMEZ)
# ----------------------------
@app.route('/login', methods=['POST'])
def handle_login():
    data = request.get_json() or {}
    user = users_col.find_one({
        "kullanici_adi": data.get('kullanici_adi'),
        "sifre": data.get('sifre')
    })
    if user:
        token = create_token(user["kullanici_adi"])
        return jsonify({"durum": "basarili", "mesaj": "Giriş Başarılı", "token": token}), 200
    return jsonify({"durum": "hata", "mesaj": "Hatalı Bilgi"}), 401


@app.route('/status', methods=['GET'])
def health_check():
    return jsonify({"durum": "aktif"}), 200


# ----------------------------
# Protected endpoint (JWT/Bearer GEREKİR)
# ----------------------------
@app.route('/profile', methods=['GET'])
@token_required
def profile():
    return jsonify({"durum": "basarili", "kullanici": getattr(request, "user", None)}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
