"""
Mini Orgzaar API
Basit bir etkinlik hizmeti listeleme ve rezervasyon talebi alma API'si.

Author: Teknik Değerlendirme
Date: 3 Kasım 2025
"""

from flask import Flask, jsonify
from api.services import services_bp
from api.bookings import bookings_bp
import logging
from datetime import datetime


def create_app():
    """Flask uygulama factory"""
    app = Flask(__name__)
    
    # Konfigürasyon
    app.config['JSON_AS_ASCII'] = True  # Türkçe karakter desteği
    app.config['JSON_SORT_KEYS'] = False
    
    # Logging ayarları
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Blueprint kayıtları
    app.register_blueprint(services_bp)
    app.register_blueprint(bookings_bp)
    
    # Ana sayfa
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Mini Orgzaar API\'ye hoş geldiniz!',
            'version': '1.0.0',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'endpoints': {
                'services': {
                    'GET /api/v1/services': 'Hizmetleri listeler',
                },
                'bookings': {
                    'POST /api/v1/bookings': 'Rezervasyon talebi oluşturur'
                }
            },
            'documentation': 'https://github.com/yourusername/mini-orgzaar-api'
        })
    
    # 404 handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Endpoint bulunamadı',
            'message': 'İstediğiniz URL mevcut değil. Lütfen /api/v1/services veya /api/v1/bookings endpoint\'lerini kullanın.'
        }), 404
    
    # 500 handler
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal Server Error: {error}')
        return jsonify({
            'error': 'Sunucu hatası',
            'message': 'Bir hata oluştu. Lütfen daha sonra tekrar deneyin.'
        }), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

