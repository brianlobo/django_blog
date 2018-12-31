(function(){
    var menu = document.querySelector('ul');
    var menulink = document.querySelector('#menubar');

    menulink.addEventListener('click', function(e) {
        menu.classList.toggle('navactive');
        e.preventDefault();
    });
})();