from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
# CORS: Frontend'in (8080) Backend'e (8000) erişmesine izin ver
CORS(app)

# --- MONGODB BAĞLANTISI ---
# Docker-compose'daki servis adı 'mongodb' olduğu için host olarak onu kullanıyoruz.
client = MongoClient('mongodb://mongodb:27017/')
db = client.ymg_veritabani  # Veritabanı adı
users_col = db.users        # Kullanıcılar tablosu

# Başlangıçta admin kullanıcısı yoksa ekle (Test kolaylığı için)
if users_col.count_documents({"kullanici_adi": "admin"}) == 0:
    users_col.insert_one({"kullanici_adi": "admin", "sifre": "12345"})
    print("Admin kullanıcısı otomatik oluşturuldu.")

# Sabit Token (Önceki ödevden kalan güvenlik önlemi)
API_TOKEN = "SUPER_SECRET_TOKEN_12345"

# --- 1. KAYIT OL (REGISTER) ENDPOINT ---
@app.route('/register', methods=['POST'])
def handle_register():
    if not request.is_json:
        return jsonify({"durum": "hata", "mesaj": "JSON formatı gerekli."}), 400

    data = request.get_json()
    kullanici_adi = data.get('kullanici_adi')
    sifre = data.get('sifre')

    if not kullanici_adi or not sifre:
        return jsonify({"durum": "hata", "mesaj": "Kullanıcı adı ve şifre zorunlu!"}), 400

    # Kullanıcı zaten var mı?
    if users_col.find_one({"kullanici_adi": kullanici_adi}):
        return jsonify({"durum": "hata", "mesaj": "Bu kullanıcı adı zaten alınmış."}), 409

    # Yeni kullanıcıyı kaydet
    users_col.insert_one({"kullanici_adi": kullanici_adi, "sifre": sifre})
    
    return jsonify({"durum": "basarili", "mesaj": "Kayıt başarılı! Giriş yapabilirsiniz."}), 201

# --- 2. GİRİŞ YAP (LOGIN) ENDPOINT ---
@app.route('/login', methods=['POST'])
def handle_login():
    data = request.get_json()
    kullanici_adi = data.get('kullanici_adi')
    sifre = data.get('sifre')

    # Veritabanında ara
    user = users_col.find_one({"kullanici_adi": kullanici_adi, "sifre": sifre})

    if user:
        return jsonify({"durum": "basarili", "mesaj": "Giriş Başarılı"}), 200
    else:
        return jsonify({"durum": "hata", "mesaj": "Kullanıcı adı veya şifre hatalı."}), 401

# --- 3. GÜVENLİ VERİ (TOKEN TESTİ) ---
@app.route('/secure_data', methods=['GET'])
def get_secure_data():
    auth_header = request.headers.get('Authorization')
    if auth_header and API_TOKEN in auth_header:
        return jsonify({
            "durum": "basarili", 
            "mesaj": "Gizli verilere erişim sağlandı.",
            "data": {"user_level": "premium", "record_count": 42}
        }), 200
    return jsonify({"durum": "hata", "mesaj": "Yetkisiz Erişim"}), 401

# --- 4. SİSTEM DURUMU ---
@app.route('/status', methods=['GET'])
def health_check():
    return jsonify({"durum": "basarili", "mesaj": "API ve Veritabanı Aktif"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)