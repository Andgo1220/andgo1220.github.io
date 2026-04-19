function loadElement(id, file) {
    fetch(file)
        .then(response => {
            if (response.ok) return response.text();
            throw new Error('Network response was not ok');
        })
        .then(data => {
            const element = document.getElementById(id);
            if (element) {
                element.innerHTML = data;
            }
        })
        .catch(error => console.error('Error loading ' + file, error));
}

// Note: No leading slash before "templates"
loadElement('header-placeholder', '/templates/header.html');
loadElement('footer-placeholder', '/templates/footer.html');