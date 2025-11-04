"""
Rezervasyon endpoint testleri
"""

import json
from datetime import datetime, timedelta


def test_create_booking_success(client):
    """POST /api/v1/bookings - Geçerli veri ile başarılı rezervasyon"""
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    payload = {
        "service_ids": [1, 3],
        "event_date": future_date,
        "notes": "Yılbaşı kutlaması için."
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    
    assert 'message' in data
    assert 'booking_id' in data
    assert data['message'] == "Rezervasyon talebiniz alındı."
    assert isinstance(data['booking_id'], int)
    assert 1000 <= data['booking_id'] <= 9999


def test_create_booking_without_notes(client):
    """POST /api/v1/bookings - notes alanı olmadan da çalışmalı"""
    future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    
    payload = {
        "service_ids": [2],
        "event_date": future_date
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 201


def test_create_booking_empty_service_ids(client):
    """POST /api/v1/bookings - Boş service_ids listesi kabul edilmeli"""
    future_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    
    payload = {
        "service_ids": [],
        "event_date": future_date
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 201


def test_create_booking_missing_service_ids(client):
    """POST /api/v1/bookings - service_ids eksikse 400 hatası"""
    future_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    
    payload = {
        "event_date": future_date
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert 'error' in data
    assert 'details' in data
    assert 'service_ids' in data['details']


def test_create_booking_invalid_service_ids_type(client):
    """POST /api/v1/bookings - service_ids string ise hata"""
    future_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    
    payload = {
        "service_ids": "1,2,3",  # String (yanlış)
        "event_date": future_date
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'service_ids' in data['details']


def test_create_booking_invalid_service_id(client):
    """POST /api/v1/bookings - Geçersiz hizmet ID'si ile hata"""
    future_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    
    payload = {
        "service_ids": [1, 999],  # 999 geçersiz
        "event_date": future_date
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'service_ids' in data['details']


def test_create_booking_missing_event_date(client):
    """POST /api/v1/bookings - event_date eksikse 400 hatası"""
    payload = {
        "service_ids": [1, 2]
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    
    assert 'error' in data
    assert 'details' in data
    assert 'event_date' in data['details']


def test_create_booking_invalid_date_format(client):
    """POST /api/v1/bookings - Yanlış tarih formatında hata"""
    payload = {
        "service_ids": [1],
        "event_date": "24-12-2025"  # DD-MM-YYYY formatı (yanlış)
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'event_date' in data['details']


def test_create_booking_past_date(client):
    """POST /api/v1/bookings - Geçmiş tarih ile hata"""
    past_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    
    payload = {
        "service_ids": [1],
        "event_date": past_date
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'event_date' in data['details']
    assert 'gelecek bir tarih' in data['details']['event_date']


def test_create_booking_today(client):
    """POST /api/v1/bookings - Bugünün tarihi geçmiş sayılmalı"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    payload = {
        "service_ids": [1],
        "event_date": today
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    # Bugün geçmiş sayılır
    assert response.status_code == 400


def test_create_booking_no_json_body(client):
    """POST /api/v1/bookings - JSON body yoksa hata"""
    response = client.post('/api/v1/bookings')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_create_booking_invalid_json(client):
    """POST /api/v1/bookings - Geçersiz JSON ile hata"""
    response = client.post(
        '/api/v1/bookings',
        data='{"service_ids": [1, 2]',  # Kapanmayan JSON
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_create_booking_tomorrow(client):
    """POST /api/v1/bookings - Yarının tarihi geçerli olmalı"""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    payload = {
        "service_ids": [1, 2, 3],
        "event_date": tomorrow,
        "notes": "Acil organizasyon"
    }
    
    response = client.post(
        '/api/v1/bookings',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 201

