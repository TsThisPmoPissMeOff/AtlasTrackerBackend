let lastResults = null;  // Store last analysis for refinement

// Main analyze function
async function analyzeImage(bbox=null) {
    const fileInput = document.getElementById('imageInput');
    if(fileInput.files.length === 0) {
        alert("Select an image first!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    if(bbox) formData.append("bbox", bbox);

    // Update UI
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = "<p>Analyzing... please wait.</p>";

    try {
        const response = await fetch("https://<YOUR_BACKEND_URL>/analyze", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        lastResults = data;
        displayResults(data);
    } catch (err) {
        resultsDiv.innerHTML = `<p>Error: ${err}</p>`;
    }
}

// Display results with explanations, Google Maps, and refine button
function displayResults(data){
    const div = document.getElementById('results');
    div.innerHTML = "";

    data.candidates.forEach((c, i) => {
        // Candidate header
        const header = document.createElement('p');
        header.innerText = `Candidate ${i+1}: ${c.coords.lat.toFixed(5)}, ${c.coords.lon.toFixed(5)}, Score: ${c.final_score.toFixed(2)}`;
        div.appendChild(header);

        // Google Maps button
        const btnMap = document.createElement('button');
        btnMap.innerText = "Open in Google Maps";
        btnMap.onclick = () => window.open(`https://www.google.com/maps?q=${c.coords.lat},${c.coords.lon}`);
        div.appendChild(btnMap);

        // Explanation dropdown
        const explanationDropdown = document.createElement('details');
        explanationDropdown.innerHTML = `<summary>Explanation</summary><pre>${JSON.stringify(data.explanation, null, 2)}</pre>`;
        div.appendChild(explanationDropdown);

        // Refine button
        const btnRefine = document.createElement('button');
        btnRefine.innerText = "Refine using this candidate";
        btnRefine.onclick = () => refineCandidate(c);
        div.appendChild(btnRefine);

        div.appendChild(document.createElement('hr'));
    });
}

// Iterative refinement function
function refineCandidate(candidate) {
    if(!candidate || !candidate.coords) return;

    // Define bounding box around candidate (+/- small delta)
    const delta = 0.05; // ~5 km box; adjust as needed
    const lat = candidate.coords.lat;
    const lon = candidate.coords.lon;
    const bbox = `${lat-delta},${lon-delta},${lat+delta},${lon+delta}`;

    alert(`Refining search within ~5km of candidate location.`);

    // Re-run analyzeImage with bounding box
    analyzeImage(bbox);
}

// Optional: drag & drop support
document.getElementById('imageInput').addEventListener('dragover', e => e.preventDefault());
document.getElementById('imageInput').addEventListener('drop', e => {
    e.preventDefault();
    document.getElementById('imageInput').files = e.dataTransfer.files;
});
