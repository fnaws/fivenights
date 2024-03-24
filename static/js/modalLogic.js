window.onload = function() {
    // Show the modal on page load
    const modal = document.getElementById('instructionsModal');
    modal.classList.replace('hidden', 'show');

    // Get the <span> element that closes the modal
    const span = document.getElementsByClassName("close")[0];

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.classList.replace('show', 'hidden');
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal)
            modal.classList.replace('show', 'hidden');
    }
}
