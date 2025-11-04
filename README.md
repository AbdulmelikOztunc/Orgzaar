# Mini Orgzaar API

Basit bir etkinlik hizmeti listeleme ve rezervasyon talebi alma REST API'si.

## Kurulum

```bash
# Sanal ortam oluştur
python -m venv venv

# Aktif et (Windows)
venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

## API Endpoints

### GET /api/v1/services
Tüm hizmetleri listeler.

### POST /api/v1/bookings
Yeni rezervasyon talebi oluşturur.

**Request Body:**
```json
{
  "service_ids": [1, 3],
  "event_date": "2025-12-24",
  "notes": "Opsiyonel notlar"
}
```

## Testler

```bash
pytest
```

## Teknolojiler

- Python 3.8+
- Flask 3.0.0
- Pytest 7.4.3
