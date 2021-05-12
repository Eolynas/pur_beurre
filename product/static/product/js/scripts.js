/* Fixed navbar after scroll */

document.addEventListener("DOMContentLoaded", function(){
  window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        document.getElementById('mainNav').classList.add('navbar_scroll');
      }
      else {
        document.getElementById('mainNav').classList.remove('navbar_scroll');
        document.body.style.paddingTop = '0';
      }
  });
});