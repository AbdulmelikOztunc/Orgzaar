"""
Hizmetler endpoint testleri
"""

import json


def test_get_services_success(client):
    """GET /api/v1/services - Başarılı hizmet listesi dönmeli"""
    response = client.get('/api/v1/services')
    
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    
    # En az 3 hizmet olmalı
    assert len(data) >= 3
    
    # İlk hizmetin yapısını kontrol et
    first_service = data[0]
    assert 'id' in first_service
    assert 'name' in first_service
    assert 'category' in first_service
    assert 'price' in first_service
    
    # Beklenen ilk hizmet
    assert first_service['id'] == 1
    assert first_service['name'] == "DJ Hizmeti (2 Saat)"
    assert first_service['category'] == "Müzik & Sanatçı"
    assert first_service['price'] == 5000


def test_get_services_all_fields(client):
    """Tüm hizmetlerin gerekli alanları olmalı"""
    response = client.get('/api/v1/services')
    data = json.loads(response.data)
    
    for service in data:
        assert isinstance(service['id'], int)
        assert isinstance(service['name'], str)
        assert isinstance(service['category'], str)
        assert isinstance(service['price'], (int, float))
        assert len(service['name']) > 0
        assert service['price'] > 0

