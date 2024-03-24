window.onload = function() {
    // Show the modal on page load
    const modal2 = document.getElementById('gameOverModal');
    // modal.classList.replace('hidden', 'show');

    // Get the <span> element that closes the modal
    const span2 = document.getElementsByClassName("close")[0];

    // When the user clicks on <span> (x), close the modal
    span2.onclick = function() {
        modal2.classList.replace('show', 'hidden');
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal2)
            modal2.classList.replace('show', 'hidden');
    }
}
