//ripple btn for "Increase" button
const increaseBtn = document.getElementById("increase");
let ripplesIncrease = document.createElement("span");
let cleartimeoutIncrease;

// Event listeners for "Increase" button
increaseBtn.addEventListener("mouseover", function (e) {
  let x = e.clientX - e.target.offsetLeft;
  let y = e.clientY - e.target.offsetTop;
  ripplesIncrease.style.left = x + "px";
  ripplesIncrease.style.top = y + "px";
  this.appendChild(ripplesIncrease);

  cleartimeoutIncrease = setTimeout(() => {
    ripplesIncrease.remove();
  }, 1000);
});

increaseBtn.addEventListener("mouseout", function () {
  ripplesIncrease.remove(cleartimeoutIncrease);
});

//ripple btn for all "Decrease" button
//ripple btn for all "Decrease" button
let decreaseBtn = document.getElementById("decrease");
let ripplesDecrease = document.createElement("span");
let cleartimeoutDecrease;

decreaseBtn.addEventListener("mouseover", function (e) {
  let x = e.clientX - e.target.offsetLeft;
  let y = e.clientY - e.target.offsetTop;
  ripplesDecrease.style.left = x + "px";
  ripplesDecrease.style.top = y + "px";
  this.appendChild(ripplesDecrease);

  // Clear the previous timeout, if any
  clearTimeout(cleartimeoutDecrease);

  cleartimeoutDecrease = setTimeout(() => {
    ripplesDecrease.remove();
  }, 4000);
});

decreaseBtn.addEventListener("mouseout", function () {
  // Clear the timeout when the mouse re-enters the button
  clearTimeout(cleartimeoutDecrease);
  ripplesDecrease.remove();
});

