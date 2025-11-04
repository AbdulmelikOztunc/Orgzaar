"""
Hizmetler Blueprint
GET /api/v1/services endpoint'i
"""

from flask import Blueprint, jsonify
import logging

logger = logging.getLogger(__name__)

services_bp = Blueprint('services', __name__, url_prefix='/api/v1')

# Hardcoded hizmet verileri
SERVICES = [
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


@services_bp.route('/services', methods=['GET'])
def get_services():
    """
    Tüm hizmetleri listeler.
    
    Returns:
        200: Hizmet listesi (JSON)
        
    Örnek Yanıt:
        [
            {
                "id": 1,
                "name": "DJ Hizmeti (2 Saat)",
                "category": "Müzik & Sanatçı",
                "price": 5000
            },
            ...
        ]
    """
    logger.info(f"GET /api/v1/services - Toplam {len(SERVICES)} hizmet döndürüldü")
    
    return jsonify(SERVICES), 200

