/**
 * Google Analytics 4 con Consent Mode v2.
 *
 * Este fichero tiene que ejecutarse ANTES de que cargue gtag.js, porque
 * declara el estado de consentimiento por defecto. Sin esa declaracion GA4
 * arranca asumiendo consentimiento y escribe las cookies analiticas antes
 * de que el visitante haya aceptado nada, que es justo lo que el RGPD y la
 * LSSI no permiten.
 *
 * cookies.js se encarga despues del gtag('consent','update') cuando el
 * usuario acepta o rechaza en el banner.
 *
 * Vive en un fichero aparte (y no en un <script> inline) para que la
 * Content-Security-Policy pueda prohibir el script inline por completo.
 */
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }

// Todo denegado mientras no haya consentimiento explicito.
gtag('consent', 'default', {
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'functionality_storage': 'granted',
    'security_storage': 'granted',
    // margen para que el banner resuelva antes de enviar nada
    'wait_for_update': 500
});

gtag('js', new Date());
gtag('config', 'G-MG3Y3TKP8M', {
    'anonymize_ip': true,
    'cookie_flags': 'SameSite=None;Secure'
});
