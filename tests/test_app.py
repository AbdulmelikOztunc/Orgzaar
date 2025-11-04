"""
Ana uygulama testleri
"""

import json


def test_index_route(client):
    """Ana sayfa (/) HTML arayüzü döndürmeli"""
    response = client.get('/')
    
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert b'Mini Orgzaar' in response.data
    assert b'Etkinlik Hizmetleri' in response.data


def test_api_info_route(client):
    """API bilgi endpoint'i (/api) JSON döndürmeli"""
    response = client.get('/api')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert 'message' in data
    assert 'version' in data
    assert 'endpoints' in data


def test_404_handler(client):
    """Mevcut olmayan route 404 döndürmeli"""
    response = client.get('/api/v1/nonexistent')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    
    assert 'error' in data
    assert 'Endpoint bulunamadı' in data['error']

