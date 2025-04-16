// Function to toggle the dropdown
function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    if (!dropdown) return; // Prevent if the dropdown doesn't exist

    // Close all dropdowns except the clicked one
    document.querySelectorAll('.dropdown-content').forEach(d => {
        if (d !== dropdown) {
            d.classList.remove('show-dropdown');
        }
    });

    // Toggle clicked dropdown visibility
    dropdown.classList.toggle('show-dropdown');
    console.log('Toggled dropdown:', id);
}

// Click event listener to close dropdowns when clicking outside
window.addEventListener('click', function (event) {
    // Get all the dropdowns and dropdown triggers
    const dropdowns = document.querySelectorAll('.dropdown-content');
    const triggers = document.querySelectorAll('h5');

    // Ensure the dropdowns and triggers exist
    if (dropdowns.length === 0 || triggers.length === 0) return;

    const target = event.target;

    // If the clicked target is inside a dropdown or is a trigger, do nothing
    if (Array.from(dropdowns).some(dropdown => dropdown.contains(target)) || Array.from(triggers).some(trigger => trigger.contains(target))) {
        return; // Do nothing if the click is inside a dropdown or a trigger
    }

    // If clicked outside of dropdowns and triggers, close all dropdowns
    dropdowns.forEach(dropdown => {
        dropdown.classList.remove('show-dropdown');
    });
    console.log('Closed all dropdowns');
});
