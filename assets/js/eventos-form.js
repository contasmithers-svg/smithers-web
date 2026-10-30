/* Formulario de eventos Smithers: envia por WhatsApp o email, sin backend. */
(function () {
  var f = document.getElementById('ev-form');
  if (!f) return;
  var PHONE = '34624868537';
  var EMAIL = 'info@smithersrestaurant.com';
  function v(id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; }
  function build() {
    var lines = [
      'Solicitud de evento - Smithers',
      'Nombre: ' + v('ev_nombre'),
      'Telefono: ' + v('ev_tel'),
      (v('ev_email') ? 'Email: ' + v('ev_email') : ''),
      (v('ev_fecha') ? 'Fecha: ' + v('ev_fecha') : ''),
      (v('ev_personas') ? 'Personas: ' + v('ev_personas') : ''),
      (v('ev_tipo') ? 'Tipo: ' + v('ev_tipo') : ''),
      (v('ev_detalles') ? 'Detalles: ' + v('ev_detalles') : '')
    ];
    var out = [];
    for (var i = 0; i < lines.length; i++) { if (lines[i]) out.push(lines[i]); }
    return out.join('\n');
  }
  function valid() { return f.reportValidity(); }
  var wa = document.getElementById('ev_wa');
  if (wa) wa.addEventListener('click', function () {
    if (!valid()) return;
    window.open('https://wa.me/' + PHONE + '?text=' + encodeURIComponent(build()), '_blank', 'noopener');
  });
  var ml = document.getElementById('ev_mail');
  if (ml) ml.addEventListener('click', function () {
    if (!valid()) return;
    var subject = 'Solicitud de evento - ' + (v('ev_nombre') || 'Smithers');
    window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(build());
  });
})();
