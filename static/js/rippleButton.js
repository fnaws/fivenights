// Function to create ripple effect
function createRipple(button) {
  button.addEventListener("mouseover", function (e) {
    let x = e.clientX - e.target.offsetLeft;
    let y = e.clientY - e.target.offsetTop;
    let ripples = document.createElement("span");
    ripples.style.left = x + "px";
    ripples.style.top = y + "px";
    this.appendChild(ripples);

    setTimeout(() => {
      ripples.remove();
    }, 1000);
  });

  button.addEventListener("mouseout", function (e) {
    this.querySelectorAll('span').forEach(span => span.remove());
  });
}

// Apply ripple effect to each button
createRipple(document.getElementById("increase"));
createRipple(document.getElementById("decrease"));
createRipple(document.getElementById("increase2"));
createRipple(document.getElementById("decrease2"));
createRipple(document.getElementById("increase3"));
// Add more buttons if necessary
