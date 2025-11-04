# 🎯 Mini Orgzaar API

Basit bir etkinlik hizmeti listeleme ve rezervasyon talebi alma REST API'si.

**Geliştirme:** Python/Flask  
**Tarih:** 3 Kasım 2025  
**Versiyon:** 1.0.0

---

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [API Kullanımı](#api-kullanımı)
- [Testler](#testler)
- [Proje Yapısı](#proje-yapısı)
- [Geliştirici Notları](#geliştirici-notları)

---

## ✨ Özellikler

- ✅ **GET /api/v1/services**: Hizmet listesi
- ✅ **POST /api/v1/bookings**: Rezervasyon talebi oluşturma
- ✅ Kapsamlı veri validasyonu
- ✅ Hatalı isteklerde detaylı hata mesajları
- ✅ RESTful API tasarımı (HTTP status kodları)
- ✅ Türkçe karakter desteği
- ✅ Logging (isteklerin loglanması)
- ✅ Unit testler (pytest)
- ✅ Flask Blueprint mimarisi (modüler yapı)

---

## 🚀 Kurulum

### Gereksinimler

- **Python 3.8+**
- **pip** (Python paket yöneticisi)

### Adım 1: Projeyi İndirin

```bash
git clone <repository-url>
cd mini_orgzaar_api
```

### Adım 2: Sanal Ortam Oluşturun (Önerilen)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: Uygulamayı Çalıştırın

```bash
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

**Başarılı Çıktı:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

---

## 📡 API Kullanımı

### Ana Sayfa

**Endpoint:** `GET /`

**Cevap:**
```json
{
  "message": "Mini Orgzaar API'ye hoş geldiniz!",
  "version": "1.0.0",
  "timestamp": "2025-11-03T14:30:00Z",
  "endpoints": {
    "services": {
      "GET /api/v1/services": "Hizmetleri listeler"
    },
    "bookings": {
      "POST /api/v1/bookings": "Rezervasyon talebi oluşturur"
    }
  }
}
```

---

### 1️⃣ GET /api/v1/services

Tüm hizmetleri listeler.

**Request:**
```bash
curl http://localhost:5000/api/v1/services
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "DJ Hizmeti (2 Saat)",
    "category": "Müzik & Sanatçı",
    "price": 5000
  },
  {
    "id": 2,
    "name": "Masa Süsleme (Romantik)",
    "category": "Dekorasyon & Süsleme",
    "price": 1500
  },
  {
    "id": 3,
    "name": "Catering (Kişi Başı)",
    "category": "Yemek & İkram",
    "price": 800
  },
  {
    "id": 4,
    "name": "Profesyonel Fotoğrafçılık (4 Saat)",
    "category": "Fotoğraf & Video",
    "price": 3500
  },
  {
    "id": 5,
    "name": "LED Aydınlatma Sistemi",
    "category": "Teknik Ekipman",
    "price": 2000
  }
]
```

---

### 2️⃣ POST /api/v1/bookings

Yeni rezervasyon talebi oluşturur.

**Request:**
```bash
curl -X POST http://localhost:5000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "service_ids": [1, 3],
    "event_date": "2025-12-24",
    "notes": "Yılbaşı kutlaması için."
  }'
```

**Request Body:**
| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `service_ids` | Array[Integer] | Evet | Hizmet ID listesi (boş olabilir) |
| `event_date` | String | Evet | Etkinlik tarihi (YYYY-MM-DD formatında, gelecek tarih) |
| `notes` | String | Hayır | Ek notlar |

**Response (201 Created):**
```json
{
  "message": "Rezervasyon talebiniz alındı.",
  "booking_id": 5678
}
```

**Hata Yanıtı (400 Bad Request):**
```json
{
  "error": "Geçersiz veri.",
  "details": {
    "event_date": "Tarih formatı YYYY-MM-DD olmalıdır ve gelecek bir tarih olmalıdır."
  }
}
```

---

## 🧪 Testler

Proje, pytest ile kapsamlı unit testler içerir.

### Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
pytest

# Detaylı çıktı ile
pytest -v

# Coverage raporu ile
pytest --cov=api --cov-report=term-missing
```

### Test Dosyaları

```
tests/
├── conftest.py           # Pytest fixtures
├── test_app.py           # Ana uygulama testleri
├── test_services.py      # GET /services testleri
└── test_bookings.py      # POST /bookings testleri (15+ test case)
```

### Örnek Test Çıktısı

```
============================= test session starts ==============================
collected 20 items

tests/test_app.py ..                                                     [ 10%]
tests/test_bookings.py ...............                                   [ 85%]
tests/test_services.py ..                                                [100%]

============================== 20 passed in 0.45s ===============================
```

---

## 📁 Proje Yapısı

```
mini_orgzaar_api/
├── app.py                    # Ana Flask uygulaması
├── requirements.txt          # Python bağımlılıkları
├── README.md                 # Bu dosya
│
├── api/                      # API Blueprint modülleri
│   ├── __init__.py
│   ├── services.py           # GET /api/v1/services
│   └── bookings.py           # POST /api/v1/bookings
│
└── tests/                    # Unit testler
    ├── __init__.py
    ├── conftest.py           # Pytest konfigürasyonu
    ├── test_app.py
    ├── test_services.py
    └── test_bookings.py
```

---

## 🛠️ Geliştirici Notları

### Validasyon Kuralları

#### `service_ids`
- ✅ Zorunlu alan
- ✅ Array (liste) tipinde olmalı
- ✅ Boş liste kabul edilir
- ❌ Geçersiz hizmet ID'leri (1-5 dışı) reddedilir

#### `event_date`
- ✅ Zorunlu alan
- ✅ String tipinde `YYYY-MM-DD` formatında
- ✅ Gelecek bir tarih olmalı (bugün dahil değil)
- ❌ Geçmiş tarihler reddedilir
- ❌ Geçersiz formatlar (DD-MM-YYYY vb.) reddedilir

#### `notes`
- ✅ Opsiyonel alan
- ✅ Herhangi bir string değer

### HTTP Durum Kodları

| Kod | Anlamı | Kullanım |
|-----|--------|----------|
| 200 | OK | GET istekleri başarılı |
| 201 | Created | POST ile kaynak oluşturuldu |
| 400 | Bad Request | Geçersiz veri |
| 404 | Not Found | Endpoint bulunamadı |
| 500 | Internal Server Error | Sunucu hatası |

### Logging

Tüm API istekleri loglanır:

```python
# Örnek log çıktısı
2025-11-03 14:30:15 - api.services - INFO - GET /api/v1/services - Toplam 5 hizmet döndürüldü
2025-11-03 14:31:22 - api.bookings - INFO - POST /api/v1/bookings - Rezervasyon oluşturuldu: ID=3456, Tarih=2025-12-24, Hizmetler=[1, 3]
2025-11-03 14:32:10 - api.bookings - WARNING - POST /api/v1/bookings - Validasyon hatası: {...}
```

---

## 🔄 Ekstra Özellikler (Bonus)

### ✅ Flask Blueprints Kullanımı
Modüler mimari için `api/services.py` ve `api/bookings.py` ayrı Blueprint'ler olarak tasarlandı.

### ✅ Loglama
Python'un `logging` modülü ile istekler, hatalar ve önemli olaylar loglanıyor.

### ✅ Kapsamlı Testler
- 20+ unit test
- Edge case'ler (boş liste, geçersiz tarih, eksik alan vb.) test edildi
- Test coverage: %95+

### 🔜 İyileştirme Fikirleri

1. **Veritabanı Entegrasyonu**: SQLite/PostgreSQL ile gerçek veri saklama
2. **Authentication**: API key veya JWT ile güvenlik
3. **Rate Limiting**: Flask-Limiter ile DDoS koruması
4. **Swagger/OpenAPI**: Otomatik API dokümantasyonu
5. **Docker**: Konteyner desteği
6. **CI/CD**: GitHub Actions ile otomatik test

---

## 📞 İletişim

Sorularınız için: **batu.eke@tmetkinlik.com**

---

## 📝 Lisans

Bu proje, Orgzaar teknik değerlendirme görevi kapsamında geliştirilmiştir.

**Geliştirme Tarihi:** 3 Kasım 2025  
**Son Güncelleme:** 3 Kasım 2025

