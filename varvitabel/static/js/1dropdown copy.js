// Function to toggle the dropdown menu
function toggleDropdown(id) {
    var dropdown = document.getElementById(id);
    dropdown.classList.toggle('show-dropdown'); // Toggle the visibility of the dropdown
}

// Close the dropdown if the user clicks outside of it, but NOT inside the input field or the dropdown
window.onclick = function(event) {
    var dropdown = document.getElementById("dropdown-nimi"); // Get the dropdown
    var inputField = document.querySelector('input[name="desc"]'); // Get the input field

    // Check if the click is outside the dropdown and input field
    if (!dropdown.contains(event.target) && !inputField.contains(event.target) && !event.target.matches('.tootekood-tabeliheaderkast h5', '.tabeliheaderkast h5')) {
        dropdown.classList.remove('show-dropdown'); // Close the dropdown
    }
}

// Stop the event from propagating when the user clicks inside the dropdown content or the input field
document.querySelector('.dropdown-content').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent the click from propagating to the window.onclick
});

document.querySelector('input[name="desc"]').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent the click from propagating to the window.onclick
});
