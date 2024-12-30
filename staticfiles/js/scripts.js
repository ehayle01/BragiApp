// static/js/scripts.js

document.querySelectorAll('li').forEach(item => {
    item.addEventListener('mouseenter', function() {
        const submenu = item.querySelector('.submenu');
        if (submenu) {
            submenu.style.display = 'block';
            submenu.style.transform = 'translateX(0)';
        }
    });

    item.addEventListener('mouseleave', function() {
        const submenu = item.querySelector('.submenu');
        if (submenu) {
            submenu.style.display = 'none';
            submenu.style.transform = 'translateX(-100%)';
        }
    });
});
