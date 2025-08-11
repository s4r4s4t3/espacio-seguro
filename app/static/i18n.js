/* i18n.js — persist language choice and call /set_language/<lang> */
document.addEventListener('DOMContentLoaded', () => {
  const sel = document.getElementById('language-select');
  if (!sel) return;
  sel.addEventListener('change', () => {
    const lang = sel.value.replace('-', '_');
    try { localStorage.setItem('ui_lang', lang); } catch(e){}
    window.location.href = `/set_language/${lang}`;
  });
  // Preselect from localStorage if available
  try {
    const saved = localStorage.getItem('ui_lang');
    if (saved && sel.value !== saved) sel.value = saved;
  } catch(e){}
});
