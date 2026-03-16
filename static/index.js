var timer = 0;
var timerRunning = false;

timeCounter = document.getElementById("timer");
startTimer = document.getElementById("startTimer");
stopTimer = document.getElementById("stopTimer");
seshTime = document.getElementById("seshTime");
form = document.querySelector("form");

startTimer.addEventListener("pointerdown", () => {
  if (!startTimer.disabled) {
    timerRunning = true;
    startTimer.disabled = true;
    stopTimer.disabled = false;
  }
});

stopTimer.addEventListener("pointerdown", () => {
  if (!stopTimer.disabled) {
    timerRunning = false;
    timeCounter.textContent = 0;
    startTimer.disabled = false;
    stopTimer.disabled = true;
    let m = Math.ceil(timer / 60);
    seshTime.value = m;
    form.submit();
    timer = 0;
    seshTime.value = 0;
  }
});

form.addEventListener("submit", () => {
  seshTime.value = timer;
});

setInterval(() => {
  if (timerRunning) {
    timer++;
    timeCounter.textContent = parseInt(timer);
    seshTime.value = timer;
  }
}, 1000);
