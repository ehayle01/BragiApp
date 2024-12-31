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
        }// Handle submenu hover events
document.querySelectorAll('li').forEach(item => {
    item.addEventListener('mouseover', function() {
        const submenu = item.querySelector('.submenu');
        if (submenu) {
            submenu.style.display = 'block';
            submenu.style.transform = 'translateX(0)';
        }
    });

    item.addEventListener('mouseout', function() {
        const submenu = item.querySelector('.submenu');
        if (submenu) {
            submenu.style.display = 'none';
            submenu.style.transform = 'translateX(-100%)';
        }
    });
});

// Theme toggle logic
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');

    // Check if the theme toggle button and icon exist to avoid errors
    if (themeToggleButton && themeIcon) {
        // Set initial theme based on user's preference stored in localStorage or default to light mode
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark-mode');
            themeIcon.classList.replace('fa-sun', 'fa-moon'); // Change icon to moon
        } else {
            document.body.classList.remove('dark-mode');
            themeIcon.classList.replace('fa-moon', 'fa-sun'); // Change icon to sun
        }

        // Theme toggle button functionality
        themeToggleButton.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');

            // Switch icons
            if (document.body.classList.contains('dark-mode')) {
                themeIcon.classList.replace('fa-sun', 'fa-moon');
                localStorage.setItem('theme', 'dark'); // Save the user's preference
            } else {
                themeIcon.classList.replace('fa-moon', 'fa-sun');
                localStorage.setItem('theme', 'light'); // Save the user's preference
            }
        });
    }
});

    });
});

document.addEventListener('DOMContentLoaded', () => {
    // Set initial theme based on user's preference stored in localStorage or default to light mode
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        document.getElementById('theme-icon').classList.replace('fa-sun', 'fa-moon'); // Change icon to moon
    } else {
        document.body.classList.remove('dark-mode');
        document.getElementById('theme-icon').classList.replace('fa-moon', 'fa-sun'); // Change icon to sun
    }

    // Theme toggle button
    const themeToggleButton = document.getElementById('theme-toggle');
    themeToggleButton.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');

        // Switch icons
        const icon = document.getElementById('theme-icon');
        if (document.body.classList.contains('dark-mode')) {
            icon.classList.replace('fa-sun', 'fa-moon');
            localStorage.setItem('theme', 'dark'); // Save the user's preference
        } else {
            icon.classList.replace('fa-moon', 'fa-sun');
            localStorage.setItem('theme', 'light'); // Save the user's preference
        }
    });
});

