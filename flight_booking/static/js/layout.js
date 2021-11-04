let mainNav = document.getElementById('js-menu');
let navBarToggle = document.getElementById('js-nav-toggle');

// event click burger

navBarToggle.addEventListener("click",function() {
    mainNav.classList.toggle('active'); //add class from js
});

