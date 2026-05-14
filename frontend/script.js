let dark = false;

// LOGIN FUNCTION
function login() {

    const username =
    document.getElementById("username").value;

    const password =
    document.getElementById("password").value;

    if(username === "admin" &&
       password === "admin123") {

        document.getElementById("login-page")
        .style.display = "none";

        document.getElementById("main-page")
        .classList.remove("hidden");
    }

    else {

        alert("Invalid Username or Password");
    }
}


// ANALYZE FUNCTION
async function analyze() {

    try {

        document.getElementById("loading")
        .style.display = "block";

        const file =
        document.getElementById("resume").files[0];

        const jd =
        document.getElementById("jd").value;

        if(!file || !jd){

            alert("Please upload resume and enter job description");

            return;
        }

        const formData = new FormData();

        formData.append("resume", file);

        formData.append("job_desc", jd);

        const res = await fetch(
            "https://ai-resume-screening-chatbot.onrender.com/analyze",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await res.json();

        document.getElementById("loading")
        .style.display = "none";

        if(data.error){

            alert(data.error);

            return;
        }

        document.getElementById("result").innerHTML = `

        <div class="result-card">

            <h2>📊 ATS Score:
            ${data.ats_score}%</h2>

            <div class="progress">

                <div class="progress-bar"
                style="width:${data.ats_score}%">
                </div>

            </div>

            <h3>📈 Similarity Score:
            ${data.similarity_score}%</h3>

            <h3>🧠 Skill Match:
            ${data.skill_score}%</h3>

            <h3>🏆 Rank:
            ${data.rank}</h3>

            <h3>🚀 Improvement Needed:
            ${data.improvement}%</h3>

            <h3>✅ Matched Skills</h3>

            <p>
            ${data.matched_skills.join(", ") || "None"}
            </p>

            <h3>❌ Missing Skills</h3>

            <p>
            ${data.missing_skills.join(", ") || "None"}
            </p>

            <h3>⚠ Missing Sections</h3>

            <p>
            ${data.missing_sections.join(", ") || "None"}
            </p>

            <h3>🤖 AI Feedback</h3>

            <pre>
${data.ai_feedback}
            </pre>

            <h3>🎯 Interview Questions</h3>

            <pre>
${data.interview_questions}
            </pre>

        </div>
        `;

    }

    catch(err) {

        console.log(err);

        alert("Backend Error");
    }
}


// DARK MODE
function toggleTheme() {

    dark = !dark;

    if(dark){

        document.body.classList.add("dark");
    }

    else{

        document.body.classList.remove("dark");
    }
}


// DRAG & DROP
function allowDrop(ev) {

    ev.preventDefault();
}

function dropHandler(ev) {

    ev.preventDefault();

    document.getElementById("resume").files =
    ev.dataTransfer.files;
}