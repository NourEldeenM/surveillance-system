const form = document.getElementById("trackingForm");
const responseDiv = document.getElementById("trackingResponse");
const trackBtn   = document.getElementById("trackingBtn");
const fileLabel  = document.querySelector(".file-input-label[for='trackingInput']");
const fileInput  = document.getElementById("trackingInput");

// Visual feedback on file selection
fileInput.addEventListener("change", () => {
  if (fileInput.files.length) {
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

    responseDiv.innerHTML = `
      <a href="${data.annotated_video}" download class="btn">
        <span>Download Annotated Video</span>
        <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path fill="currentColor" d="M5 20h14v-2H5v2zm7-18L5.33 9h3.84v6h4.66V9h3.84L12 2z"/>
        </svg>
      </a>
    `;

    // Show annotated video
    // responseDiv.innerHTML = "";
    // const videoEl = document.createElement("video");
    // videoEl.controls = true;
    // videoEl.src = data.annotated_video;   // must start with "/static/outputs/..."
    // videoEl.className = "video-player";
    // videoEl.style = "width:100%; max-width:600px; display:block; margin:1rem auto;";
    // console.log("Appending videoEl:", videoEl);
    // responseDiv.appendChild(videoEl);
  } catch (err) {
    responseDiv.innerHTML = `<p class="error">⚠️ ${err.message}</p>`;
  } finally {
    trackBtn.disabled = false;
    trackBtn.querySelector("span").textContent = "Track Objects";
  }
});