# Basit Giriş API Projesi

Bu proje, bir kullanıcı doğrulama servisini simüle eden basit bir Flask REST API'sidir.
Proje, Docker ve Docker Compose kullanılarak paketlenmiştir.

## Kurulum ve Çalıştırma

Projenin çalışması için bilgisayarınızda **Docker Desktop**'ın kurulu ve çalışır durumda olması gerekmektedir.

### 1. Docker İmajını Oluşturma

Projeyi kullanmaya başlamadan önce imajı derlemelisiniz. **Proje ana dizinindeyken** terminalde bu komutu çalıştırın:

```bash
docker build -t basit-login-api:v1 .