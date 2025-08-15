/ Momentum-style horizontal drag for .scroll-row
document.querySelectorAll('.scroll-row').forEach(row => {
  let isDown=false,startX,scrollLeft;
  row.addEventListener('mousedown', e => {isDown=true; startX=e.pageX-row.offsetLeft; scrollLeft=row.scrollLeft;});
  row.addEventListener('mouseleave', ()=> isDown=false);
  row.addEventListener('mouseup', ()=> isDown=false);
  row.addEventListener('mousemove', e => {
    if(!isDown) return;
    e.preventDefault();
    const x=e.pageX-row.offsetLeft, walk=(x-startX)*1.2;
    row.scrollLeft = scrollLeft - walk;
  });
});
