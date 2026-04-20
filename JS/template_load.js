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
const sheetURL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQQdn_JLKJ-U1JR7087gB2bF26NsusVoqRsaqZTZQnsVADfYk4Au_CkDT8qHmYFN8I9I4gvwRo4CEdP/pub?gid=0&single=true&output=csv';

async function displayCSV() {
    try {
        const response = await fetch(sheetURL);
        const data = await response.text();
        
        // Split the CSV into rows
        const rows = data.split('\n');
        let html = '<table class="andgo-table">';

        rows.forEach((row, index) => {
            html += '<tr>';
            const columns = row.split(',').slice(0, 4); 
            columns.forEach(col => {
                const tag = (index === 0) ? 'th' : 'td';
                html += `<${tag}>${col}</${tag}>`;
            });
            html += '</tr>';
        });

        html += '</table>';
        document.getElementById('csv-table-display').innerHTML = html;
    } catch (error) {
        console.error('Error loading Sheet:', error);
        document.getElementById('csv-table-display').innerHTML = 'Failed to load data.';
    }
}

async function getDocsValue(x, y) {
    const response = await fetch(sheetURL);
    const data = await response.text();
    const rows = data.split('\n');

    if (rows[y]) {
        const columns = rows[y].split(',');
        
        return columns[x] ? columns[x].trim() : "Empty cell";
    }
    return "Row not found";
}

// Usage:
getDocsValue(4, 1).then(value => {
  document.getElementById("total-time").innerHTML = value
});

displayCSV();

loadElement('header-placeholder', '/templates/header.html');
loadElement('footer-placeholder', '/templates/footer.html');