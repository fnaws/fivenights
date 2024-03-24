function addRippleEffect(button) {
  button.addEventListener("mouseover", function (e) {
    // Create a new span for the ripple effect every time there is a mouseover event
    let rippleSpan = document.createElement("span");
    rippleSpan.classList.add("ripple");
    this.appendChild(rippleSpan);

    // Position the span element
    let x = e.clientX - e.target.offsetLeft;
    let y = e.clientY - e.target.offsetTop;
    rippleSpan.style.left = x + 'px';
    rippleSpan.style.top = y + 'px';

    // Remove the span after it animates
    setTimeout(() => {
      rippleSpan.remove();
    }, 600); // Ensure this matches the duration of your ripple effect
  });
}

// Add the ripple effect to all buttons with the 'btn' class
document.querySelectorAll('.btn').forEach(button => {
  addRippleEffect(button);
});
