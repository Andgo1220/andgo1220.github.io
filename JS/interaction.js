// 1. Select all dropdown buttons
const dropBtns = document.querySelectorAll('.dropbtn');

dropBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        
        const currentMenu = this.nextElementSibling;
        
        document.querySelectorAll('.dropdown-content').forEach(menu => {
            if (menu !== currentMenu) {
                menu.classList.remove('show');
            }
        });

        currentMenu.classList.toggle('show');
    });
});


window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        document.querySelectorAll('.dropdown-content').forEach(menu => {
            menu.classList.remove('show');
        });
    }
}