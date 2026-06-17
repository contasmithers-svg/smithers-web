/**
 * Cookie Consent Banner - Smithers Restaurant
 * GDPR compliant cookie consent manager
 * Categories: necessary, analytics, marketing
 */

(function() {
    'use strict';

    const COOKIE_NAME = 'smithers_cookies_consent';
    const COOKIE_EXPIRY_DAYS = 365;

    // ====== STYLES ======
    const styles = document.createElement('style');
    styles.textContent = `
        #smithers-cookie-banner {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 999999;
            background: #1a1a1a;
            color: #f5f5f5;
            padding: 20px 24px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            line-height: 1.5;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
            transform: translateY(100%);
            transition: transform 0.4s ease;
            max-height: 90vh;
            overflow-y: auto;
        }
        #smithers-cookie-banner.visible {
            transform: translateY(0);
        }
        #smithers-cookie-banner p {
            margin: 0 0 14px 0;
            max-width: 800px;
            color: #ccc;
        }
        #smithers-cookie-banner a {
            color: #c8a45c;
            text-decoration: underline;
        }
        #smithers-cookie-banner .cookie-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }
        #smithers-cookie-banner .cookie-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: opacity 0.2s;
        }
        #smithers-cookie-banner .cookie-btn:hover {
            opacity: 0.85;
        }
        #smithers-cookie-banner .btn-accept-all {
            background: #c8a45c;
            color: #1a1a1a;
        }
        #smithers-cookie-banner .btn-reject-all {
            background: #444;
            color: #f5f5f5;
        }
        #smithers-cookie-banner .btn-configure {
            background: transparent;
            color: #c8a45c;
            border: 1px solid #c8a45c;
        }
        #smithers-cookie-modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.7);
            z-index: 9999999;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        #smithers-cookie-modal-overlay.active {
            display: flex;
        }
        #smithers-cookie-modal {
            background: #1a1a1a;
            color: #f5f5f5;
            max-width: 500px;
            width: 100%;
            padding: 28px;
            border-radius: 8px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            max-height: 80vh;
            overflow-y: auto;
            border: 1px solid #333;
        }
        #smithers-cookie-modal h3 {
            margin: 0 0 20px 0;
            font-size: 20px;
            color: #c8a45c;
        }
        #smithers-cookie-modal .cookie-category {
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid #333;
        }
        #smithers-cookie-modal .cookie-category:last-child {
            border-bottom: none;
        }
        #smithers-cookie-modal .cookie-category label {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            font-weight: 600;
            font-size: 15px;
        }
        #smithers-cookie-modal .cookie-category label input[type="checkbox"] {
            width: 18px;
            height: 18px;
            accent-color: #c8a45c;
        }
        #smithers-cookie-modal .cookie-category p {
            margin: 6px 0 0 28px;
            color: #999;
            font-size: 13px;
        }
        #smithers-cookie-modal .cookie-category .always-on {
            color: #bbb;
            font-size: 12px;
            font-weight: normal;
        }
        #smithers-cookie-modal .modal-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        #smithers-cookie-modal .modal-buttons .cookie-btn {
            flex: 1;
        }
        #cookie-manage-link {
            color: #c8a45c;
            cursor: pointer;
            text-decoration: underline;
            font-size: 13px;
        }
        #cookie-manage-link:hover {
            opacity: 0.8;
        }
    `;
    document.head.appendChild(styles);

    // ====== BANNER HTML ======
    const banner = document.createElement('div');
    banner.id = 'smithers-cookie-banner';
    banner.innerHTML = `
        <p>Usamos cookies propias y de terceros para mejorar tu experiencia, analizar tráfico y mostrarte contenido relevante. Puedes aceptar todas, rechazar las no necesarias o configurar tus preferencias.</p>
        <div class="cookie-buttons">
            <button class="cookie-btn btn-accept-all" data-action="accept-all">Aceptar todas</button>
            <button class="cookie-btn btn-reject-all" data-action="reject-all">Solo necesarias</button>
            <button class="cookie-btn btn-configure" data-action="configure">Configurar</button>
        </div>
    `;

    // ====== MODAL HTML ======
    const modalOverlay = document.createElement('div');
    modalOverlay.id = 'smithers-cookie-modal-overlay';
    modalOverlay.innerHTML = `
        <div id="smithers-cookie-modal">
            <h3>Configuración de cookies</h3>
            <div class="cookie-category">
                <label>
                    <input type="checkbox" checked disabled>
                    <span>Necesarias <span class="always-on">(siempre activas)</span></span>
                </label>
                <p>Cookies técnicas necesarias para el funcionamiento del sitio web.</p>
            </div>
            <div class="cookie-category">
                <label>
                    <input type="checkbox" id="cookie-analytics" checked>
                    <span>Analíticas</span>
                </label>
                <p>Nos ayudan a entender cómo usas el sitio para mejorarlo (Google Analytics).</p>
            </div>
            <div class="cookie-category">
                <label>
                    <input type="checkbox" id="cookie-marketing">
                    <span>Marketing</span>
                </label>
                <p>Permiten mostrarte publicidad relevante en otros sitios.</p>
            </div>
            <div class="modal-buttons">
                <button class="cookie-btn btn-accept-all" data-action="accept-all">Aceptar todas</button>
                <button class="cookie-btn btn-reject-all" data-action="reject-all">Solo necesarias</button>
            </div>
            <div class="modal-buttons" style="margin-top: 10px;">
                <button class="cookie-btn btn-configure" data-action="save-modal" style="flex:1;background:#c8a45c;color:#1a1a1a;border:none;">Guardar preferencias</button>
            </div>
        </div>
    `;

    // ====== COOKIE UTILITIES ======
    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? decodeURIComponent(match[2]) : null;
    }

    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = name + '=' + encodeURIComponent(value) +
            '; expires=' + date.toUTCString() +
            '; path=/; SameSite=Lax';
    }

    function getConsent() {
        const saved = getCookie(COOKIE_NAME);
        if (saved) {
            try { return JSON.parse(saved); } catch(e) { return null; }
        }
        return null;
    }

    function saveConsent(analytics, marketing) {
        const consent = {
            necessary: true,
            analytics: analytics,
            marketing: marketing,
            timestamp: new Date().toISOString()
        };
        setCookie(COOKIE_NAME, JSON.stringify(consent), COOKIE_EXPIRY_DAYS);
        return consent;
    }

    // ====== GA4 HELPER ======
    function applyConsent(consent) {
        // Check for GA4 script tag and gtag
        if (typeof gtag === 'function') {
            gtag('consent', 'update', {
                'analytics_storage': consent.analytics ? 'granted' : 'denied',
                'ad_storage': consent.marketing ? 'granted' : 'denied',
                'ad_user_data': consent.marketing ? 'granted' : 'denied',
                'ad_personalization': consent.marketing ? 'granted' : 'denied'
            });
        }
        // Fire GA4 page_view if analytics accepted and not fired yet
        if (consent.analytics && typeof gtag === 'function') {
            gtag('event', 'page_view', {
                page_title: document.title,
                page_location: window.location.href
            });
        }
    }

    // ====== BANNER LOGIC ======
    function showBanner() {
        banner.classList.add('visible');
        document.body.appendChild(banner);
    }

    function hideBanner() {
        banner.classList.remove('visible');
        setTimeout(() => { if (banner.parentNode) banner.parentNode.removeChild(banner); }, 400);
    }

    function showModal() {
        document.body.appendChild(modalOverlay);
        setTimeout(() => modalOverlay.classList.add('active'), 10);
        // Set checkboxes from current consent
        const existing = getConsent();
        if (existing) {
            document.getElementById('cookie-analytics').checked = existing.analytics;
            document.getElementById('cookie-marketing').checked = existing.marketing;
        }
    }

    function hideModal() {
        modalOverlay.classList.remove('active');
        setTimeout(() => { if (modalOverlay.parentNode) modalOverlay.parentNode.removeChild(modalOverlay); }, 300);
    }

    function acceptAll() {
        const consent = saveConsent(true, true);
        applyConsent(consent);
        hideBanner();
        hideModal();
    }

    function rejectAll() {
        const consent = saveConsent(false, false);
        applyConsent(consent);
        hideBanner();
        hideModal();
    }

    function saveModalPreferences() {
        const analytics = document.getElementById('cookie-analytics').checked;
        const marketing = document.getElementById('cookie-marketing').checked;
        const consent = saveConsent(analytics, marketing);
        applyConsent(consent);
        hideBanner();
        hideModal();
    }

    // ====== EVENT DELEGATION ======
    banner.addEventListener('click', function(e) {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        const action = btn.dataset.action;
        if (action === 'accept-all') acceptAll();
        else if (action === 'reject-all') rejectAll();
        else if (action === 'configure') { hideBanner(); showModal(); }
    });

    modalOverlay.addEventListener('click', function(e) {
        if (e.target === modalOverlay) hideModal();
    });

    modalOverlay.addEventListener('click', function(e) {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        const action = btn.dataset.action;
        if (action === 'accept-all') acceptAll();
        else if (action === 'reject-all') rejectAll();
        else if (action === 'save-modal') saveModalPreferences();
    });

    // ====== INIT ======
    const existingConsent = getConsent();
    if (!existingConsent) {
        // First visit - show banner
        document.addEventListener('DOMContentLoaded', function() {
            document.body.appendChild(banner);
            setTimeout(() => banner.classList.add('visible'), 100);
        });
    } else {
        // Returning visitor - apply saved preferences silently
        applyConsent(existingConsent);
    }

    // ====== PUBLIC API (for "Gestionar cookies" link in footer) ======
    window.SmithersCookies = {
        openPreferences: function() {
            if (banner.parentNode) {
                banner.classList.remove('visible');
                banner.parentNode.removeChild(banner);
            }
            showModal();
        }
    };

})();