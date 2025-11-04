/**
 * Mini Orgzaar - Main JavaScript v2
 * Horizontal scroll services with search
 */

// ============================================
// Global State
// ============================================
let services = [];
let selectedServices = new Set();
let filteredServices = [];

// ============================================
// API Functions
// ============================================

/**
 * Fetch all services from the API
 */
async function fetchServices() {
    try {
        const response = await fetch('/api/v1/services');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        services = data;
        filteredServices = [...services];
        renderServices(filteredServices);
        
        // Update service count in hero
        const serviceCountEl = document.getElementById('serviceCount');
        if (serviceCountEl) {
            serviceCountEl.textContent = services.length;
        }
        
        return data;
    } catch (error) {
        console.error('Error fetching services:', error);
        showToast('Hizmetler yüklenirken bir hata oluştu.', 'error');
        
        // Show error in UI
        const container = document.getElementById('servicesHorizontal');
        if (container) {
            container.innerHTML = `
                <div class="loading-inline" style="color: #ef4444;">
                    <p>⚠️ Hizmetler yüklenemedi</p>
                </div>
            `;
        }
        
        return [];
    }
}

/**
 * Create a booking via the API
 */
async function createBooking(bookingData) {
    try {
        const response = await fetch('/api/v1/bookings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bookingData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw {
                status: response.status,
                data: data
            };
        }
        
        return { success: true, data };
    } catch (error) {
        console.error('Error creating booking:', error);
        return { 
            success: false, 
            error: error.data || { message: 'Bilinmeyen bir hata oluştu.' }
        };
    }
}

// ============================================
// UI Rendering Functions
// ============================================

/**
 * Get icon emoji for service category
 */
function getCategoryIcon(category) {
    const icons = {
        'Müzik & Sanatçı': '🎵',
        'Dekorasyon & Süsleme': '🎨',
        'Yemek & İkram': '🍽️',
        'Fotoğraf & Video': '📸',
        'Teknik Ekipman': '🎬'
    };
    return icons[category] || '⭐';
}

/**
 * Format price with Turkish Lira
 */
function formatPrice(price) {
    return new Intl.NumberFormat('tr-TR', {
        style: 'currency',
        currency: 'TRY',
        minimumFractionDigits: 0
    }).format(price);
}

/**
 * Render services horizontally
 */
function renderServices(servicesData) {
    const container = document.getElementById('servicesHorizontal');
    
    if (!container) return;
    
    if (servicesData.length === 0) {
        container.innerHTML = `
            <div class="loading-inline">
                <p>Hizmet bulunamadı.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = servicesData.map(service => `
        <div class="service-card-horizontal ${selectedServices.has(service.id) ? 'selected' : ''}" 
             data-service-id="${service.id}"
             onclick="toggleService(${service.id})">
            <div class="service-header">
                <span class="service-icon">${getCategoryIcon(service.category)}</span>
                <input type="checkbox" 
                       class="service-checkbox" 
                       ${selectedServices.has(service.id) ? 'checked' : ''}
                       onchange="toggleService(${service.id})"
                       onclick="event.stopPropagation()">
            </div>
            <h4 class="service-name">${service.name}</h4>
            <span class="service-category">${service.category}</span>
            <div class="service-price">${formatPrice(service.price)}</div>
        </div>
    `).join('');
    
    updateScrollButtons();
}

/**
 * Update selected services summary and list
 */
function updateSelectedSummary() {
    const countElement = document.getElementById('selectedCount');
    const totalElement = document.getElementById('totalPrice');
    const listElement = document.getElementById('selectedServicesList');
    
    if (!countElement || !totalElement || !listElement) return;
    
    const selectedServicesData = services.filter(s => selectedServices.has(s.id));
    const totalPrice = selectedServicesData.reduce((sum, s) => sum + s.price, 0);
    
    // Update count and total
    countElement.textContent = selectedServices.size;
    totalElement.textContent = formatPrice(totalPrice);
    
    // Update list
    if (selectedServicesData.length === 0) {
        listElement.innerHTML = `
            <p class="empty-message">Henüz hizmet seçmediniz. Yukarıdaki hizmetlerden seçim yapın.</p>
        `;
    } else {
        listElement.innerHTML = selectedServicesData.map(service => `
            <div class="selected-service-item">
                <div class="selected-service-info">
                    <span class="selected-service-icon">${getCategoryIcon(service.category)}</span>
                    <span class="selected-service-name">${service.name}</span>
                </div>
                <span class="selected-service-price">${formatPrice(service.price)}</span>
            </div>
        `).join('');
    }
}

// ============================================
// Event Handlers
// ============================================

/**
 * Toggle service selection
 */
function toggleService(serviceId) {
    if (selectedServices.has(serviceId)) {
        selectedServices.delete(serviceId);
    } else {
        selectedServices.add(serviceId);
    }
    
    renderServices(filteredServices);
    updateSelectedSummary();
}

/**
 * Search services
 */
function searchServices(query) {
    const searchTerm = query.toLowerCase().trim();
    
    if (!searchTerm) {
        filteredServices = [...services];
    } else {
        filteredServices = services.filter(service => 
            service.name.toLowerCase().includes(searchTerm) ||
            service.category.toLowerCase().includes(searchTerm)
        );
    }
    
    renderServices(filteredServices);
}

/**
 * Scroll services container
 */
function scrollServices(direction) {
    const container = document.getElementById('servicesHorizontal');
    if (!container) return;
    
    const scrollAmount = 300;
    const targetScroll = direction === 'left' 
        ? container.scrollLeft - scrollAmount 
        : container.scrollLeft + scrollAmount;
    
    container.scrollTo({
        left: targetScroll,
        behavior: 'smooth'
    });
    
    setTimeout(updateScrollButtons, 300);
}

/**
 * Update scroll button visibility
 */
function updateScrollButtons() {
    const container = document.getElementById('servicesHorizontal');
    const leftBtn = document.getElementById('scrollLeft');
    const rightBtn = document.getElementById('scrollRight');
    
    if (!container || !leftBtn || !rightBtn) return;
    
    const isScrollable = container.scrollWidth > container.clientWidth;
    const isAtStart = container.scrollLeft <= 0;
    const isAtEnd = container.scrollLeft + container.clientWidth >= container.scrollWidth - 1;
    
    leftBtn.style.display = isScrollable ? 'flex' : 'none';
    rightBtn.style.display = isScrollable ? 'flex' : 'none';
    
    leftBtn.disabled = isAtStart;
    rightBtn.disabled = isAtEnd;
}

/**
 * Handle booking form submission
 */
async function handleBookingSubmit(event) {
    event.preventDefault();
    
    // Get form data
    const eventDate = document.getElementById('eventDate').value;
    const notes = document.getElementById('notes').value;
    
    // Validate that at least one service is selected
    if (selectedServices.size === 0) {
        showToast('Lütfen en az bir hizmet seçin.', 'error');
        return;
    }
    
    // Validate date
    if (!eventDate) {
        showToast('Lütfen etkinlik tarihini girin.', 'error');
        return;
    }
    
    // Validate date format (YYYY-MM-DD)
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(eventDate)) {
        showToast('Tarih formatı YYYY-MM-DD olmalıdır.', 'error');
        return;
    }
    
    // Validate future date
    const selectedDate = new Date(eventDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (selectedDate < today) {
        showToast('Lütfen gelecek bir tarih seçin.', 'error');
        return;
    }
    
    // Prepare booking data (API formatına uygun)
    const bookingData = {
        service_ids: Array.from(selectedServices),
        event_date: eventDate  // YYYY-MM-DD formatında
    };
    
    // Add notes if provided
    if (notes.trim()) {
        bookingData.notes = notes.trim();
    }
    
    // Disable submit button
    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
        <div class="spinner-small"></div>
        Gönderiliyor...
    `;
    
    // Create booking
    const result = await createBooking(bookingData);
    
    // Re-enable submit button
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalText;
    
    // Show result
    const resultElement = document.getElementById('bookingResult');
    if (!resultElement) return;
    
    resultElement.style.display = 'block';
    
    if (result.success) {
        resultElement.className = 'booking-result success';
        resultElement.innerHTML = `
            <h4>✅ Rezervasyon Başarılı!</h4>
            <p>Rezervasyon talebiniz alındı.</p>
            <p><strong>Rezervasyon ID:</strong> ${result.data.booking_id}</p>
            <p style="margin-top: 1rem; font-size: 0.9rem;">
                ${result.data.message}
            </p>
        `;
        
        showToast('Rezervasyon başarıyla oluşturuldu!', 'success');
        
        // Reset form and selections
        setTimeout(() => {
            document.getElementById('bookingForm').reset();
            selectedServices.clear();
            renderServices(filteredServices);
            updateSelectedSummary();
            resultElement.style.display = 'none';
        }, 5000);
    } else {
        resultElement.className = 'booking-result error';
        
        let errorMessage = result.error.error || 'Bilinmeyen bir hata oluştu.';
        let errorDetails = '';
        
        if (result.error.details) {
            errorDetails = '<ul style="margin-top: 0.5rem; padding-left: 1.5rem;">';
            for (const [field, message] of Object.entries(result.error.details)) {
                errorDetails += `<li><strong>${field}:</strong> ${message}</li>`;
            }
            errorDetails += '</ul>';
        }
        
        resultElement.innerHTML = `
            <h4>❌ Rezervasyon Başarısız</h4>
            <p>${errorMessage}</p>
            ${errorDetails}
        `;
        
        showToast('Rezervasyon oluşturulamadı. Lütfen bilgilerinizi kontrol edin.', 'error');
    }
    
    // Scroll to result
    resultElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

/**
 * Copy code to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text)
            .then(() => {
                showToast('Kod panoya kopyalandı!', 'success');
            })
            .catch(err => {
                console.error('Error copying to clipboard:', err);
                showToast('Kopyalama başarısız.', 'error');
            });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast('Kod panoya kopyalandı!', 'success');
        } catch (err) {
            console.error('Error copying to clipboard:', err);
            showToast('Kopyalama başarısız.', 'error');
        }
        document.body.removeChild(textArea);
    }
}

/**
 * Set minimum date for event date input
 */
function setMinimumDate() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const dateInput = document.getElementById('eventDate');
    if (dateInput) {
        // YYYY-MM-DD formatında minimum tarih
        const minDate = tomorrow.toISOString().split('T')[0];
        dateInput.min = minDate;
        
        // Set default to tomorrow
        dateInput.value = minDate;
    }
}

// ============================================
// Initialization
// ============================================

/**
 * Initialize the application
 */
function init() {
    // Set minimum date
    setMinimumDate();
    
    // Fetch services
    fetchServices();
    
    // Setup form event listener
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', handleBookingSubmit);
    }
    
    // Setup search input
    const searchInput = document.getElementById('serviceSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchServices(e.target.value);
        });
    }
    
    // Setup scroll buttons
    const leftBtn = document.getElementById('scrollLeft');
    const rightBtn = document.getElementById('scrollRight');
    
    if (leftBtn) {
        leftBtn.addEventListener('click', () => scrollServices('left'));
    }
    
    if (rightBtn) {
        rightBtn.addEventListener('click', () => scrollServices('right'));
    }
    
    // Update scroll buttons on scroll
    const container = document.getElementById('servicesHorizontal');
    if (container) {
        container.addEventListener('scroll', updateScrollButtons);
    }
    
    // Update scroll buttons on window resize
    window.addEventListener('resize', updateScrollButtons);
    
    // Setup copy button event listeners
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-copy');
            const codeElement = document.getElementById(targetId);
            if (codeElement) {
                const code = codeElement.textContent;
                copyToClipboard(code);
            }
        });
    });
    
    console.log('Mini Orgzaar initialized successfully! 🎉');
}

// ============================================
// Start Application
// ============================================

// Wait for DOM to be fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchServices,
        createBooking,
        formatPrice,
        getCategoryIcon,
        searchServices
    };
}
