function loadElement(id, file) {
    fetch(file)
        .then(response => response.text())
        .then(data => {
            const placeholder = document.getElementById(id);
            if (placeholder) {
                placeholder.insertAdjacentHTML('afterend', data);
                placeholder.remove();
                
                // --- ADD THIS PART ---
                // If this was the header, run the dropdown setup
                if (id === 'header-placeholder') {
                    setupDropdowns(); 
                }
            }
        });
}

function setupDropdowns() {
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
}

loadElement('header-placeholder', '/templates/header.html');
loadElement('footer-placeholder', '/templates/footer.html');