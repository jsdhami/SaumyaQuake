 // Get references to the button and popup container
 const togglePopupButton = document.getElementById('toggle-popup');
 const popup = document.getElementById('popup');

 // Function to toggle the popup visibility
 function togglePopup() {
     if (popup.style.display === 'none' || popup.style.display === '') {
         popup.style.display = 'block';
     } else {
         popup.style.display = 'none';
     }
 }

 // Event listener for the toggle button
 togglePopupButton.addEventListener('click', togglePopup);