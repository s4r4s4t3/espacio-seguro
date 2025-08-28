/* likes.js — double-tap like with optimistic UI */
(function(){
  function dblTap(el, fn){
    let last=0;
    el.addEventListener('click', e=>{
      const now = Date.now();
      if (now - last < 350) fn(e);
      last = now;
    });
  }
  document.querySelectorAll('.post-card [data-post-id]').forEach(img=>{
    dblTap(img, async ()=>{
      const postId = img.getAttribute('data-post-id');
      img.classList.add('liked-pulse');
      try{
        const res = await fetch(`/posts/${postId}/like`, {method:'POST', headers:{'X-Requested-With':'XMLHttpRequest'}});
        // ignore response for now; backend may or may not be wired fully
      }catch(_e){}
      setTimeout(()=>img.classList.remove('liked-pulse'), 450);
    });
  });
})();
