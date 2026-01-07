# Basic Login API (Docker + PostgreSQL)

Bu proje Flask tabanlı bir REST API uygulamasıdır.  
Docker Compose kullanılarak backend, frontend ve PostgreSQL servisleri birlikte çalıştırılmaktadır.

---

## 🔄 Login Akışı (Mermaid Sequence Diagram)

```mermaid
sequenceDiagram
    participant User as Kullanıcı
    participant Frontend
    participant API as Flask API
    participant DB as PostgreSQL

    User->>Frontend: Kullanıcı adı ve şifre girer
    Frontend->>API: POST /login isteği gönderilir
    API->>DB: Kullanıcı bilgileri sorgulanır
    DB-->>API: Kullanıcı bulundu / bulunamadı
    API-->>Frontend: Token veya hata mesajı döner
    Frontend-->>User: Giriş sonucu gösterilir