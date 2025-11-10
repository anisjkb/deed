// Add this to your main.js or a separate script file
document.addEventListener('DOMContentLoaded', () => {
  const scroller = document.querySelector('.industry-scroller');
  const track = scroller.querySelector('.industry-track');
  let isDown = false;
  let startX;
  let scrollLeft;

  scroller.addEventListener('mousedown', (e) => {
    isDown = true;
    scroller.classList.add('active');
    startX = e.pageX - track.offsetLeft;
    scrollLeft = track.scrollLeft;
  });

  scroller.addEventListener('mouseleave', () => {
    isDown = false;
    scroller.classList.remove('active');
  });

  scroller.addEventListener('mouseup', () => {
    isDown = false;
    scroller.classList.remove('active');
  });

  scroller.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - track.offsetLeft;
    const walk = (x - startX) * 2; //scroll-fast
    track.scrollLeft = scrollLeft - walk;
  });
});