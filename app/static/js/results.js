document.addEventListener("DOMContentLoaded", () => {
  const videoEl = document.getElementById("annotatedVideo");
  const responseDiv = document.getElementById("trackingResponse");
  const tableBody = document.querySelector("#resultsTable tbody");
  const backBtn = document.getElementById("backBtn");

  const videoURL = sessionStorage.getItem("integration_annotated");
  const resultsData = JSON.parse(sessionStorage.getItem("integration_results") || "[]");

  // Preview video
  if (videoURL) {
    responseDiv.innerHTML = `
      <a href="${videoURL}" download class="btn">
        <span>Download Annotated Video</span>
        <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path fill="currentColor" d="M5 20h14v-2H5v2zm7-18L5.33 9h3.84v6h4.66V9h3.84L12 2z"/>
        </svg>
      </a>
    `;
  }

  // Populate table
  if (resultsData.length === 0) {
    tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">No detections found.</td></tr>`;
  } else {
    resultsData.forEach(frameObj => {
      frameObj.faces.forEach(face => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${frameObj.frame}</td>
          <td>${face.tracked_id}</td>
          <td>[${face.bbox.join(", ")}]</td>
          <td>${face.confidence.toFixed(2)}</td>
          <td>${face.face_recognition}</td>
        `;
        tableBody.append(row);
      });
    });
  }

  backBtn.addEventListener("click", () => {
    sessionStorage.removeItem("integration_annotated");
    sessionStorage.removeItem("integration_results");
    window.location.href = "/";
  });
});