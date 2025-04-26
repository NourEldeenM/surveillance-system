document.addEventListener("DOMContentLoaded", () => {
    const videoEl = document.getElementById("annotatedVideo");
    const tableBody = document.querySelector("#resultsTable tbody");
    const backBtn = document.getElementById("backBtn");
  
    // Retrieve from sessionStorage
    const annotatedVideo = sessionStorage.getItem("annotatedVideo");
    const resultsData    = JSON.parse(sessionStorage.getItem("resultsData") || "[]");
  
    if (annotatedVideo) {
      videoEl.src = annotatedVideo;
    }
  
    if (resultsData.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">No detections found.</td></tr>`;
    } else {
      // Flatten results: one row per face detection
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
      sessionStorage.clear();
      window.location.href = "/";
    });
  });
  