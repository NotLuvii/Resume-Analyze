document.addEventListener("DOMContentLoaded", () => {
    const analyzeBtn = document.getElementById("analyze-btn");
    const jobDescriptionField = document.getElementById("job-description");
    const resumeField = document.getElementById("resume");
    const analysisOutput = document.getElementById("analysis-output");
    const questionsList = document.getElementById("questions");

    analyzeBtn.addEventListener("click", async () => {
        const jobDescription = jobDescriptionField.value.trim();
        const resumeFile = resumeField.files[0];
    
        // Validate inputs
        if (!jobDescription) {
            alert("Please enter a job description.");
            return;
        }
    
        if (!resumeFile) {
            alert("Please upload a resume file.");
            return;
        }
    
        const formData = new FormData();
        formData.append("job_description", jobDescription);
        formData.append("resume", resumeFile);
    
        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData,
            });
    
            const result = await response.json();
            if (result.error) {
                alert(result.error);
            } else {
                // Clear previous results
                document.getElementById("missing-soft").innerHTML = "";
                document.getElementById("missing-technical").innerHTML = "";
                document.getElementById("matched-soft").innerHTML = "";
                document.getElementById("matched-technical").innerHTML = "";
                questionsList.innerHTML = "";
    
                // Display Gap Analysis
                result.analysis.gap_analysis.missing_soft.forEach((skill) => {
                    const li = document.createElement("li");
                    li.textContent = skill;
                    document.getElementById("missing-soft").appendChild(li);
                });
    
                result.analysis.gap_analysis.missing_technical.forEach((skill) => {
                    const li = document.createElement("li");
                    li.textContent = skill;
                    document.getElementById("missing-technical").appendChild(li);
                });
    
                // Display Matched Keywords
                result.analysis.matched_soft.forEach((skill) => {
                    const li = document.createElement("li");
                    li.textContent = skill;
                    document.getElementById("matched-soft").appendChild(li);
                });
    
                result.analysis.matched_technical.forEach((skill) => {
                    const li = document.createElement("li");
                    li.textContent = skill;
                    document.getElementById("matched-technical").appendChild(li);
                });
    
                // Display Interview Questions
                result.questions.forEach((question) => {
                    const li = document.createElement("li");
                    li.textContent = question;
                    questionsList.appendChild(li);
                });
            }
        } catch (error) {
            console.error("Error analyzing resume:", error);
        }
    });
});
