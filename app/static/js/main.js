const form = document.getElementById("uploadForm");
const responseDiv = document.getElementById("response");
const uploadBtn   = document.getElementById("uploadBtn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  responseDiv.textContent = "";   
  uploadBtn.disabled = true;     
  uploadBtn.querySelector("span").textContent = "Processing…";

  try {
    const res = await fetch("/models/integration/video", {
      method: "POST",
      body: new FormData(form)
    });
    const text = await res.text();
    let payload;
    try { payload = JSON.parse(text); }
    catch { throw new Error(text); }
    if (!res.ok) throw new Error(payload.detail || "Processing failed");
    responseDiv.innerHTML = `
    <div class="video-wrapper">
      <video controls src="${payload.annotated_video}" class="video-player"></video>
    </div>
  `;

    // Store for results page
    sessionStorage.setItem("annotatedVideo", payload.annotated_video);
    sessionStorage.setItem("resultsData", JSON.stringify(payload.results));

    // Redirect to results
    window.location.href = "/results";
  } catch (err) {
    responseDiv.innerHTML = `<p class="error">⚠️ ${err.message}</p>`;
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.querySelector("span").textContent = "Upload & Process";
  }
});
