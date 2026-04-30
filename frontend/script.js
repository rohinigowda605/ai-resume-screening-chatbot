let lastResult = null;

// LOGIN
function login() {
    const user = document.getElementById("username").value;
    const pass = document.getElementById("password").value;

    if (user === "admin" && pass === "1234") {
        document.getElementById("login-page").classList.add("hidden");
        document.getElementById("main-page").classList.remove("hidden");
    } else {
        alert("Invalid login");
    }
}

// DARK MODE
function toggleTheme() {
    document.body.classList.toggle("dark");
}

// DRAG & DROP
const dropArea = document.getElementById("drop-area");

dropArea.addEventListener("dragover", e => {
    e.preventDefault();
});

dropArea.addEventListener("drop", e => {
    e.preventDefault();
    document.getElementById("resume").files = e.dataTransfer.files;
});

// ANALYZE
async function analyze() {
    const file = document.getElementById("resume").files[0];
    const jd = document.getElementById("jd").value;

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("jd", jd);

    const res = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    lastResult = data;

    function getColor(value) {
        if (value >= 70) return "#28a745";
        if (value >= 40) return "#ffc107";
        return "#dc3545";
    }

    document.getElementById("result").innerHTML = `
        <h3>📊 ATS Score: ${data.scores.ats_score}%</h3>

        <p>Similarity: ${data.scores.similarity_score}%</p>
        <div class="progress-bar">
            <div class="progress-fill" style="width:${data.scores.similarity_score}%; background:${getColor(data.scores.similarity_score)};"></div>
        </div>

        <p>Skill Match: ${data.scores.skill_match}%</p>
        <div class="progress-bar">
            <div class="progress-fill" style="width:${data.scores.skill_match}%; background:${getColor(data.scores.skill_match)};"></div>
        </div>

        <h4>Missing Skills:</h4>
        <p>${data.missing_skills.join(", ") || "None"}</p>

        <h4>Suggestions:</h4>
        <p>${data.ai_feedback}</p>
    `;
}

// DOWNLOAD REPORT
function downloadReport() {
    if (!lastResult) {
        alert("Run analysis first!");
        return;
    }

    const text = `
ATS Score: ${lastResult.scores.ats_score}%
Similarity: ${lastResult.scores.similarity_score}%
Skill Match: ${lastResult.scores.skill_match}%

Missing Skills:
${lastResult.missing_skills.join(", ")}

Suggestions:
${lastResult.ai_feedback}
    `;

    const blob = new Blob([text], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "report.txt";
    a.click();
}