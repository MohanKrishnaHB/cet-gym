let duration;
timeComponent = {};
let interval;

const getPrintableTimeFormat = (duration) => {
  let time = duration.hr < 10 ? "0" : "";
  time += duration.hr + ":";
  time += duration.min < 10 ? "0" : "";
  time += duration.min + ":";
  time += duration.sec < 10 ? "0" : "";
  time += duration.sec;
  return time;
};

const updateDuration = () => {
  timeComponent.innerHTML = getPrintableTimeFormat(duration);
  let sec = duration.sec - 1;
  let min = duration.min;
  let hr = duration.hr;
  if (sec <= -1) {
    sec = 59;
    min = min - 1;
    if (min <= -1) {
      min = 59;
      hr = hr - 1;
      if (hr <= 0) {
        clearInterval(interval);
      }
    }
  }
  duration = { hr, min, sec };
};

function onLoad(duration) {
  duration = duration;
  interval = setInterval(updateDuration, 1000);
  timeComponent = document.getElementById("timer");
}
