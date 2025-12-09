# Gerekli Flask modüllerini import ediyoruz.
# Flask: Web uygulamasını oluşturmak için ana sınıf.
# jsonify: Python dictionary'lerini JSON formatında yanıt olarak döndürmek için.
# request: İstemciden (client) gelen verileri (örn: JSON) almak için.
from flask_cors import CORS
from flask import Flask, request, jsonify

# Flask uygulamasını başlatıyoruz.
app = Flask(__name__)
# CORS (Cross-Origin Resource Sharing) etkinleştirme
CORS(app)   

# --- Proje Açıklamanızdaki Sabit Bilgiler ---
# Normalde bu bilgiler bir veritabanında şifrelenmiş olarak tutulur.
# Sizin verdiğiniz örneğe göre ("admin" ve "12345") sabit olarak tanımlıyoruz.
DOGRULANMIS_KULLANICI_ADI = "admin"
DOGRULANMIS_SIFRE = "12345"
# Yeni güvenlikli API endpoint'i için sabit Bearer Token
API_TOKEN = "SUPER_SECRET_TOKEN_12345"
# ---------------------------------------------

@app.route('/login', methods=['POST'])
def handle_login():

    """
    Kullanıcı girişi için REST API endpoint'i.
    POST metodu ile JSON formatında 'kullanici_adi' ve 'sifre' bekler.
    Sequence diagram'daki 4. ve 5. adımları gerçekleştirir.
    """
    
    # 1. Adım & 2. Adım (Kullanıcıdan verinin gelmesi)
    # Gelen isteğin JSON formatında olup olmadığını kontrol et
    if not request.is_json:
        return jsonify({"durum": "hata", "mesaj": "Hatalı istek. JSON formatı bekleniyor."}), 400

    # Gelen JSON verisini bir Python dictionary'sine çevir
    data = request.get_json()

    # 3. Adım (Kullanıcının 'Giriş Yap' butonuna basması bu isteği tetikler)
    # Gerekli alanlar 'kullanici_adi' ve 'sifre' JSON içinde var mı?
    if 'kullanici_adi' not in data or 'sifre' not in data:
        return jsonify({"durum": "hata", "mesaj": "Eksik bilgi. 'kullanici_adi' ve 'sifre' alanları zorunludur."}), 400

    # Kullanıcıdan gelen bilgileri al
    kullanici_adi = data['kullanici_adi']
    sifre = data['sifre']

    # 4. Adım: Uygulama işlemi yapar (Bilgileri kontrol et)
    if kullanici_adi == DOGRULANMIS_KULLANICI_ADI and sifre == DOGRULANMIS_SIFRE:
        # 5. Adım: Başarılı Sonuç
        print(f"Başarılı giriş denemesi: Kullanıcı={kullanici_adi}")
        response_data = {
            "durum": "basarili",
            "mesaj": "Giriş Başarılı"
        }
        return jsonify(response_data), 200
    else:
        # 5. Adım: Hatalı Sonuç
        print(f"Hatalı giriş denemesi: Kullanıcı={kullanici_adi}, Şifre={sifre}")
        response_data = {
            "durum": "hata",
            "mesaj": "Hatalı Bilgi Girdiniz"
        }
        return jsonify(response_data), 401 # 401: Unauthorized (Yetkisiz)
@app.route('/secure_data', methods=['GET'])
def get_secure_data():
    """
    Bu endpoint'e erişim için Bearer Token (API Token) gereklidir.
    """
    # HTTP Başlığından (Header) Authorization alanını al
    auth_header = request.headers.get('Authorization')

    if auth_header:
        try:
            # 'Bearer ' ön ekini ayırıp token'ı al
            token_type, token = auth_header.split()
        except ValueError:
            return jsonify({"durum": "hata", "mesaj": "Hatalı yetkilendirme başlığı formatı."}), 401

        # Token tipi ve değerini kontrol et
        if token_type.lower() == 'bearer' and token == API_TOKEN:
            # Başarılı Yetkilendirme (Token geçerli)
            return jsonify({
                "durum": "basarili",
                "mesaj": "Gizli verilere erişim sağlandı.",
                "data": {"user_level": "premium", "record_count": 42}
            }), 200
        else:
            return jsonify({"durum": "hata", "mesaj": "Geçersiz Bearer Token."}), 401
    else:
        # Authorization başlığı yoksa
        return jsonify({"durum": "hata", "mesaj": "Bu kaynağa erişim için Bearer Token gereklidir."}), 401
    
@app.route('/status', methods=['GET'])
def health_check():
    """
    API'nin çalışır durumda olup olmadığını kontrol eder.
    """
    return jsonify({"durum": "basarili", "mesaj": "API çalışıyor, sistem sağlıklı."}), 200

# Python script'i doğrudan çalıştırıldığında bu blok çalışır
if __name__ == '__main__':
    # Uygulamayı debug modunda 5000 portunda başlatır.
    # Debug modu, kodda değişiklik yaptığınızda sunucunun otomatik yeniden başlamasını sağlar.
    app.run(debug=True, port=5000)