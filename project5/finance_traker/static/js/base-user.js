document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.menu-btn');
    const menuShowBtn = document.querySelector('.menu-show-btn');
    const menuBar = document.querySelector('.menu-bar');
    const closeBtn = document.querySelector('.btn-close');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const pageName = this.getAttribute('data-name');
            loadPage(pageName);
        })
    })
    menuShowBtn.addEventListener('click', ()=> {
        closeBtn.classList.remove("hidden");
        menuBar.style.display = "flex";

    });
    document.querySelector('.btn-close').addEventListener('click', ()=> {
        menuBar.style.display = "none"
    })
    loadPage('dashboard');
});


function loadPage(pageName){
    const menuBar = document.querySelector('.menu-bar');
    const pageWidth = window.innerWidth
    if (pageWidth < 600) {
        menuBar.style.display = "none"
    }
    fetch(`/${pageName}/`)
    .then(response => {
        return response.text();
    })
    .then(html => {
        const contentSection = document.querySelector('.page-section');
        contentSection.innerHTML = html;
        contentSection.replaceWith(contentSection.cloneNode(true));
        initPagesJs(pageName);
    })
    .catch(error => {
        console.error('Error loading page:', error);
    });
}
function initPagesJs(pageName) {
    console.log('Initializing page:', pageName);

    if (pageName ===  'dashboard') {
        initDashboardJs();
    } else if (pageName === 'transaction') {
        initTransactionJs();
    }
} 