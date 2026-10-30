/* ASB Photography — site behavior
   1. Click a gallery photo to enlarge it. The X, Esc, or clicking
      outside the photo closes it; arrow keys or swiping move
      between photos.
   2. Inquiry/contact forms send an email titled "Photo Shoot Inquiry".
*/

/* ---------- 1. Enlarged photo (lightbox) ---------- */
(function () {
  var photos = Array.prototype.slice.call(document.querySelectorAll('.gallery .photo'));
  if (!photos.length) return;

  var box = document.createElement('div');
  box.className = 'lightbox';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.setAttribute('aria-label', 'Enlarged photo');
  box.innerHTML =
    '<p class="lightbox-count" aria-live="polite"></p>' +
    '<button class="lightbox-close" type="button" aria-label="Close photo">' +
    '<svg viewBox="0 0 32 32" fill="none" stroke="#111" stroke-width="1.5">' +
    '<path d="M3 3 L29 29 M29 3 L3 29"/></svg></button>' +
    '<img alt="">';
  document.body.appendChild(box);

  var img = box.querySelector('img');
  var count = box.querySelector('.lightbox-count');
  var closeBtn = box.querySelector('.lightbox-close');
  var current = -1;
  var lastFocus = null;

  function show(i) {
    current = (i + photos.length) % photos.length;
    var link = photos[current];
    var thumb = link.querySelector('img');
    img.src = link.getAttribute('href');
    img.alt = thumb ? thumb.alt : '';
    count.textContent = (current + 1) + ' / ' + photos.length;
  }

  function open(i) {
    lastFocus = document.activeElement;
    show(i);
    box.classList.add('open');
    document.body.classList.add('no-scroll');
    closeBtn.focus({ preventScroll: true });
  }

  function close() {
    box.classList.remove('open');
    document.body.classList.remove('no-scroll');
    img.removeAttribute('src');
    if (lastFocus) lastFocus.focus({ preventScroll: true });
  }

  photos.forEach(function (link, i) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      open(i);
    });
  });

  closeBtn.addEventListener('click', close);
  box.addEventListener('click', function (e) {
    if (e.target === box) close();
  });
  document.addEventListener('keydown', function (e) {
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowRight') show(current + 1);
    else if (e.key === 'ArrowLeft') show(current - 1);
    else if (e.key === 'Tab') { e.preventDefault(); closeBtn.focus(); }
  });

  // Swipe left/right on phones to move between photos
  var startX = null, startY = null;
  box.addEventListener('touchstart', function (e) {
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
  }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (startX === null) return;
    var dx = e.changedTouches[0].clientX - startX;
    var dy = e.changedTouches[0].clientY - startY;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(current + (dx < 0 ? 1 : -1));
    startX = null;
  });
})();

/* ---------- 2. Inquiry / contact forms ---------- */
(function () {
  var forms = document.querySelectorAll('form.inquiry');

  Array.prototype.forEach.call(forms, function (form) {
    var status = form.querySelector('.form-status');
    var button = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;

      // The form's action is https://formsubmit.co/<email>; the AJAX
      // version of the same address is https://formsubmit.co/ajax/<email>
      var endpoint = form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/');
      var data = {};
      new FormData(form).forEach(function (value, key) { data[key] = value; });

      button.disabled = true;
      status.className = 'form-status';
      status.textContent = 'Sending…';

      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (res) { return res.json().then(function (body) { return { ok: res.ok, body: body }; }); })
        .then(function (r) {
          if (!r.ok || String(r.body.success) === 'false') throw new Error(r.body.message || 'Send failed');
          form.reset();
          status.textContent = 'Thank you! Your inquiry has been sent.';
        })
        .catch(function () {
          status.className = 'form-status error';
          status.textContent = 'Sorry, something went wrong. Please try again in a moment.';
        })
        .then(function () { button.disabled = false; });
    });
  });
})();
