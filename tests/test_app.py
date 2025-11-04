"""
Ana uygulama testleri
"""

import json


def test_index_route(client):
    """Ana sayfa (/) bilgi döndürmeli"""
    response = client.get('/')
    
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

