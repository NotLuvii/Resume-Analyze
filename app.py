from flask import Flask, request, jsonify, send_from_directory
from backend.analyzer import *
from backend.parser import extract_text
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/upload", methods=["POST"])
def upload_resume():
    try:
        # Get form inputs
        job_description = request.form.get("job_description")
        resume_file = request.files.get("resume")

        # Validate inputs
        if not job_description or not resume_file:
            return jsonify({"error": "Job description and resume are required."}), 400

        # Extract text from the uploaded resume
        print(f"DEBUG: Extracting text from resume: {resume_file.filename}")
        resume_text = extract_text(resume_file.stream, resume_file.filename)
        print(resume_text, "")
        # Perform analysis
        job_keywords = extract_keywords_pipeline(job_description)
        analysis = analyze_resume(resume_text, job_keywords)

        # Generate interview questions
        questions = generate_interview_questions(job_description)

        return jsonify({"analysis": analysis, "questions": questions})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/questions", methods=["POST"])
def get_questions():
    try:
        data = request.get_json()
        job_description = data.get("job_description")
        if not job_description:
            return jsonify({"error": "Job description is required."}), 400
        questions = generate_interview_questions(job_description)
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
