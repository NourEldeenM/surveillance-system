const form      = document.getElementById("uploadForm");
const response  = document.getElementById("response");
const btn       = document.getElementById("uploadBtn");
const input     = document.getElementById("fileInput");
const label     = document.querySelector(".file-input-label[for='fileInput']");

// Highlight when file chosen
input.addEventListener("change", () => {
  if (input.files.length) {
    label.classList.add("selected");
    label.querySelector("span").textContent = input.files[0].name;
  }
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  response.innerHTML = "";
  btn.disabled = true;
  btn.querySelector("span").textContent = "Processing…";

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

    // store for results page
    sessionStorage.setItem("integration_annotated", payload.annotated_video);
    sessionStorage.setItem("integration_results", JSON.stringify(payload.results));
    window.location.href = "/results";

  } catch (err) {
    response.innerHTML = `<p class="error">⚠️ ${err.message}</p>`;
  } finally {
    btn.disabled = false;
    btn.querySelector("span").textContent = "Upload & Process";
  }
});
