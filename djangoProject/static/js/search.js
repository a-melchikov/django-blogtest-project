document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.form-control');
    const searchBtn = document.getElementById('searchBtn');

    function toggleSearchBtn() {
        if (searchInput.value.trim() === '') {
            searchBtn.disabled = true;
        } else {
            searchBtn.disabled = false;
        }
    }

    toggleSearchBtn();
    searchInput.addEventListener('input', toggleSearchBtn);
});
