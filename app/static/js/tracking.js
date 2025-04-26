console.log("🎬 tracking.js loaded");
const form = document.getElementById("trackingForm");
const responseDiv = document.getElementById("trackingResponse");
console.log("responseDiv =", responseDiv);
const trackBtn   = document.getElementById("trackingBtn");
const fileLabel  = document.querySelector(".file-input-label[for='trackingInput']");
const fileInput  = document.getElementById("trackingInput");

// Visual feedback on file selection
fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    fileLabel.classList.add("selected");
    fileLabel.querySelector("span").textContent = fileInput.files[0].name;
  }
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  responseDiv.textContent = "";
  trackBtn.disabled = true;
  trackBtn.querySelector("span").textContent = "Tracking…";

  try {
    const res = await fetch("/models/tracking/video", {
      method: "POST",
      body: new FormData(form)
    });

    let data;
    const text = await res.text();
    console.log("Response text:", text);
    try { data = JSON.parse(text); }
    catch {
      throw new Error(text);
    }
    if (!res.ok) throw new Error(data.detail || "Tracking failed");
    console.log("Received data:", data);

    // Show annotated video
    responseDiv.innerHTML = "";
    const videoEl = document.createElement("video");
    videoEl.controls = true;
    videoEl.src = data.annotated_video;   // must start with "/static/outputs/..."
    videoEl.className = "video-player";
    videoEl.style = "width:100%; max-width:600px; display:block; margin:1rem auto;";
    console.log("Appending videoEl:", videoEl);
    responseDiv.appendChild(videoEl);
  } catch (err) {
    responseDiv.innerHTML = `<p class="error">⚠️ ${err.message}</p>`;
  } finally {
    trackBtn.disabled = false;
    trackBtn.querySelector("span").textContent = "Track Objects";
  }
});