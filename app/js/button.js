 // Get references to the button and popup container
        const togglePopupButton = document.getElementById('toggle-popupjj');
        const popup = document.getElementById('popupforqd');

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
// this is



 // Get references to the button and popup container
 const GraphButton = document.getElementById('graphb');
 const gImg = document.getElementById('graphimg');

 // Function to toggle the popup visibility
 function togglePopupD() {
     if (gImg.style.display === 'none' || gImg.style.display === '') {
        gImg.style.display = 'block';
     } else {
        gImg.style.display = 'none';
     }
 } 

 // Event listener for the toggle button
 GraphButton.addEventListener('click', togglePopupD);
