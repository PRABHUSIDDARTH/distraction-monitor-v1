let threshold = 0;
if (Notification.permission !== "granted") {
  Notification.requestPermission().then((perm) => {
    if (perm === "granted") {
      console.log("✅ Notification permission granted.");
    }
  });
}


document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("thresholdForm");
  const startBtn = document.getElementById("startBtn");
  const stopBtn = document.getElementById("stopBtn");
  const resetBtn = document.getElementById("resetBtn");
  const shortsCounter = document.getElementById("shortsCount"); // FIXED
  const statusText = document.getElementById("statusText");
  const intervalSlider = document.getElementById("intervalSlider");
  const intervalValue = document.getElementById("intervalValue");

  let monitorInterval = null;

  // 🧮 Set threshold
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const rangeValue = parseInt(document.getElementById("range").value, 10);

    if (isNaN(rangeValue) || rangeValue < 25 || rangeValue > 50) {
      alert("🚫 Enter a number between 25 and 50.");
      return;
    }

    threshold = rangeValue;

    try {
      const response = await fetch("/set_threshold", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `threshold=${threshold}`
      });

      const result = await response.json();
      if (result.message) {
        alert(`✅ ${result.message}`);
        statusText.textContent = "✅ Threshold Set. Ready to Monitor.";
        shortsCounter.textContent = "0";
      } else {
        throw new Error("Unexpected response");
      }
    } catch (err) {
      alert("❌ Error setting threshold.");
      console.error(err);
    }
  });

  // 🔍 Start monitoring loop
  startBtn.addEventListener("click", () => {
    if (threshold === 0) {
      alert("⚠️ Set the threshold first.");
      return;
    }

    if (monitorInterval) clearInterval(monitorInterval);

    statusText.textContent = "🔍 Monitoring for Shorts...";

    monitorInterval = setInterval(async () => {
      try {
        const res = await fetch("/start_monitoring");
        const data = await res.json();

        shortsCounter.textContent = data.shorts_viewed;

       if (data.shorts_viewed >= threshold) {
  statusText.textContent = "⚠️ Limit Reached!";

  // 🔔 Send notification
  if (Notification.permission === "granted") {
    new Notification("🚨 Distraction Alert", {
      body: `You have watched ${data.shorts_viewed} shorts!`,
    });
  }

  // 🔊 Play alert sound
  const audio = new Audio("alert.mp3");
  audio.play().catch(e => console.log("Audio failed:", e));

  alert(`🚫 You viewed ${data.shorts_viewed} shorts!`);
}

      } catch (err) {
        console.error("❌ Error in monitoring loop:", err);
      }
    }, parseInt(intervalSlider.value) * 1000); // interval in ms
  });

  // ⛔ Stop monitoring
  stopBtn.addEventListener("click", async () => {
    clearInterval(monitorInterval);
    monitorInterval = null;

    try {
      const res = await fetch("/stop_monitoring", { method: "POST" });
      const data = await res.json();
      statusText.textContent = "⛔ Monitoring Stopped.";
    } catch (err) {
      alert("❌ Failed to stop monitoring.");
      console.error(err);
    }
  });

  // ♻️ Reset everything
  resetBtn.addEventListener("click", async () => {
    clearInterval(monitorInterval);
    monitorInterval = null;

    try {
      const res = await fetch("/reset", { method: "POST" });
      const data = await res.json();
      if (data.message) {
        shortsCounter.textContent = "0";
        statusText.textContent = "🔁 Reset Complete. Idle.";
      }
    } catch (err) {
      alert("❌ Reset failed.");
      console.error(err);
    }
  });

  // 🔁 Update shorts counter every second from backend
  setInterval(() => {
    fetch('/shorts_count')
      .then(res => res.json())
      .then(data => {
        shortsCounter.textContent = data.shorts_viewed;
      })
      .catch(err => console.error("Counter update failed:", err));
  }, 1000);

  // 🎚️ Slider value display
  intervalSlider.oninput = () => {
    intervalValue.innerText = `${intervalSlider.value}s`;
  };

  // ⏱️ Update interval button
  document.getElementById("setIntervalBtn").addEventListener("click", () => {
    fetch('/set_interval', {
      method: 'POST',
      body: new URLSearchParams({ interval: intervalSlider.value }),
    })
      .then(res => res.json())
      .then(data => alert(data.message || data.error))
      .catch(err => console.error("Interval set failed:", err));
  });
});
