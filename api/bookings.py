"""
Rezervasyonlar Blueprint
POST /api/v1/bookings endpoint'i
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/v1')

# Hardcoded hizmet ID'leri (validasyon için)
VALID_SERVICE_IDS = [1, 2, 3, 4, 5]


@bookings_bp.route('/bookings', methods=['POST'])
def create_booking():
    """
    Yeni rezervasyon talebi oluşturur.
    
    Request Body (JSON):
        {
            "service_ids": [1, 3],
            "event_date": "2025-12-24",
            "notes": "Yılbaşı kutlaması için." (opsiyonel)
        }
    
    Returns:
        201: Rezervasyon başarıyla oluşturuldu
        400: Geçersiz veri
        
    Örnek Başarılı Yanıt:
        {
            "message": "Rezervasyon talebiniz alındı.",
            "booking_id": 5678
        }
    
    Örnek Hata Yanıtı:
        {
            "error": "Geçersiz veri.",
            "details": {
                "event_date": "Tarih formatı YYYY-MM-DD olmalıdır ve gelecek bir tarih olmalıdır."
            }
        }
    """
    # JSON verisini al
    data = request.get_json()
    
    if not data:
        logger.warning("POST /api/v1/bookings - Request body boş")
        return jsonify({
            "error": "Geçersiz veri.",
            "details": {
                "request_body": "JSON formatında veri gönderilmelidir."
            }
        }), 400
    
    # Validasyon
    validation_error = validate_booking_data(data)
    if validation_error:
        logger.warning(f"POST /api/v1/bookings - Validasyon hatası: {validation_error}")
        return jsonify(validation_error), 400
    
    # Rezervasyon ID'si oluştur (1000-9999 arası rastgele)
    booking_id = random.randint(1000, 9999)
    
    logger.info(
        f"POST /api/v1/bookings - Rezervasyon oluşturuldu: "
        f"ID={booking_id}, Tarih={data['event_date']}, "
        f"Hizmetler={data['service_ids']}"
    )
    
    return jsonify({
        "message": "Rezervasyon talebiniz alındı.",
        "booking_id": booking_id
    }), 201


def validate_booking_data(data):
    """
    Rezervasyon verisini doğrular.
    
    Args:
        data (dict): Request body
    
    Returns:
        dict veya None: Hata varsa hata detayları, yoksa None
    """
    # 1. service_ids kontrolü
    if 'service_ids' not in data:
        return {
            "error": "Geçersiz veri.",
            "details": {
                "service_ids": "Bu alan zorunludur."
            }
        }
    
    service_ids = data['service_ids']
    
    if not isinstance(service_ids, list):
        return {
            "error": "Geçersiz veri.",
            "details": {
                "service_ids": "Bu alan bir liste (array) olmalıdır."
            }
        }
    
    # Boş liste kabul edilebilir (göreve göre), ancak geçersiz ID'ler kontrol edilmeli
    if service_ids:
        invalid_ids = [sid for sid in service_ids if sid not in VALID_SERVICE_IDS]
        if invalid_ids:
            return {
                "error": "Geçersiz veri.",
                "details": {
                    "service_ids": f"Geçersiz hizmet ID'leri: {invalid_ids}. Geçerli ID'ler: {VALID_SERVICE_IDS}"
                }
            }
    
    # 2. event_date kontrolü
    if 'event_date' not in data:
        return {
            "error": "Geçersiz veri.",
            "details": {
                "event_date": "Bu alan zorunludur."
            }
        }
    
    event_date = data['event_date']
    
    if not isinstance(event_date, str):
        return {
            "error": "Geçersiz veri.",
            "details": {
                "event_date": "Bu alan string (metin) formatında olmalıdır."
            }
        }
    
    # Tarih formatı kontrolü (YYYY-MM-DD)
    try:
        date_obj = datetime.strptime(event_date, '%Y-%m-%d')
    except ValueError:
        return {
            "error": "Geçersiz veri.",
            "details": {
                "event_date": "Tarih formatı YYYY-MM-DD olmalıdır (örn: 2025-12-24)."
            }
        }
    
    # Gelecek tarih kontrolü
    today = datetime.now().date()
    if date_obj.date() < today:
        return {
            "error": "Geçersiz veri.",
            "details": {
                "event_date": "Tarih formatı YYYY-MM-DD olmalıdır ve gelecek bir tarih olmalıdır."
            }
        }
    
    # 3. notes kontrolü (opsiyonel, validasyon gerekmez)
    # notes alanı eksik olsa da sorun yok
    
    # Tüm kontroller başarılı
    return None

