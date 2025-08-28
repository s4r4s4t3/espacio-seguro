/* stories.js — modal viewer with swipe */
(function(){
  const modal = document.getElementById('story-modal');
  if (!modal) return;
  const stage = modal.querySelector('.story-stage');
  const closeBtn = modal.querySelector('.modal-close');

  let items = [];
  let idx = 0;
  function render(){
    if (!items.length) return;
    const it = items[idx];
    stage.innerHTML = `
      <figure class="story-figure">
        <img src="${it.image}" alt="${it.caption||''}" />
        ${it.caption ? `<figcaption>${it.caption}</figcaption>` : ``}
      </figure>`;
  }

  function openAt(i){
    idx = i;
    modal.setAttribute('aria-hidden','false');
    modal.style.display = 'grid';
    render();
    stage.focus();
  }
  function close(){ modal.style.display='none'; modal.setAttribute('aria-hidden','true'); }
  closeBtn.addEventListener('click', close);
  modal.addEventListener('click', (e)=>{ if(e.target===modal) close(); });

  // Gather story elements
  const storyEls = document.querySelectorAll('.story-item .story-avatar');
  items = Array.from(storyEls).map(el => ({
    image: el.dataset.image,
    caption: el.dataset.caption || '',
  }));
  storyEls.forEach((el, i) => el.addEventListener('click', () => openAt(i)));

  // Swipe
  let sx=0;
  stage.addEventListener('touchstart', e=>{ sx = e.touches[0].clientX; }, {passive:true});
  stage.addEventListener('touchend', e=>{
    const dx = e.changedTouches[0].clientX - sx;
    if (dx < -40) { idx = Math.min(idx+1, items.length-1); render(); }
    if (dx > 40) { idx = Math.max(idx-1, 0); render(); }
  }, {passive:true});
})();
