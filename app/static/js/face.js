const form = document.getElementById("faceForm");
const responseDiv = document.getElementById("faceResponse");
const faceBtn = document.getElementById("faceBtn");
const fileLabel = document.querySelector(".file-input-label[for='faceInput']");
const fileInput = document.getElementById("faceInput");

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
  faceBtn.disabled = true;
  faceBtn.querySelector("span").textContent = "Recognizing…";

  try {
    const res = await fetch("/models/face/recognize", {
      method: "POST",
      body: new FormData(form)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Recognition failed");

    // Display label and preview
    responseDiv.innerHTML = `<p class="success">Identified as: <strong>${data.label}</strong></p>`;
    const reader = new FileReader();
    reader.onload = () => {
      const img = document.createElement("img");
      img.src = reader.result;
      img.className = "preview-img";
      responseDiv.appendChild(img);
    };
    reader.readAsDataURL(fileInput.files[0]);
  } catch (err) {
    responseDiv.innerHTML = `<p class="error">⚠️ ${err.message}</p>`;
  } finally {
    faceBtn.disabled = false;
    faceBtn.querySelector("span").textContent = "Recognize Face";
  }
});