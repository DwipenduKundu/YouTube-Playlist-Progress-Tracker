
const profileButton = document.getElementById('profileButton');
const profileDropdown = document.getElementById('profileDropdown');

// Open and close profile dropdown
profileButton.addEventListener('click', function () {
    profileDropdown.classList.toggle('show');
});

// Close dropdown when clicking outside
document.addEventListener('click', function (event) {
    if (
        !profileButton.contains(event.target) &&
        !profileDropdown.contains(event.target)
    ) {
        profileDropdown.classList.remove('show');
    }
});
