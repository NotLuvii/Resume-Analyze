"""Relevance scoring: how much of what a job description asks for a résumé covers."""
import io

import pytest

from app import app
from backend import analyzer
from backend.analyzer import analyze_resume, calculate_keyword_weights, extract_keywords_pipeline


def analyze(resume, job):
    return analyze_resume(resume, extract_keywords_pipeline(job))


def test_weights_follow_how_often_each_skill_appears_in_the_posting():
    weights = calculate_keyword_weights("Python, Python and more Python. Some SQL.")
    assert weights == pytest.approx({"python": 0.75, "sql": 0.25})


def test_short_skill_names_are_counted_as_whole_words():
    # "R" appears once as a word; the letter r inside "Rust" or "reporting" must not count towards it.
    assert calculate_keyword_weights("We use R and Rust for reporting.") == {"r": 0.5, "rust": 0.5}


def test_score_is_the_weighted_share_of_posting_skills_found_in_the_resume():
    result = analyze("I write Python every day.", "Python, Python and more Python. Some SQL.")
    assert result["relevance_score"] == 75.0


def test_a_resume_with_every_skill_scores_100():
    assert analyze("Python and SQL", "Python, SQL")["relevance_score"] == 100.0


def test_a_resume_with_none_of_the_skills_scores_0():
    assert analyze("Gardening and cooking", "Python, SQL")["relevance_score"] == 0.0


def test_a_posting_without_listed_skills_scores_0_without_dividing_by_zero():
    assert analyze("Python", "We are a friendly company.")["relevance_score"] == 0.0


def test_matches_and_gaps_are_still_reported():
    result = analyze("Python and teamwork", "Python, SQL, teamwork, leadership")
    assert sorted(result["matched_technical"]) == ["python"]
    assert sorted(result["matched_soft"]) == ["teamwork"]
    assert sorted(result["gap_analysis"]["missing_technical"]) == ["sql"]
    assert sorted(result["gap_analysis"]["missing_soft"]) == ["leadership"]


def test_a_resume_file_on_disk_can_be_analyzed(tmp_path, docx_bytes):
    # The desktop version works from file paths dropped onto the window.
    path = tmp_path / "resume.docx"
    path.write_bytes(docx_bytes("Python and SQL"))
    result = analyzer.analyze_resume_file(str(path), extract_keywords_pipeline("Python, SQL"))
    assert result["File Name"] == "resume.docx"
    assert result["relevance_score"] == 100.0


def test_the_web_endpoint_returns_the_score(docx_bytes):
    client = app.test_client()
    response = client.post(
        "/upload",
        data={"job_description": "Python, SQL", "resume": (io.BytesIO(docx_bytes("Python")), "resume.docx")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert response.get_json()["analysis"]["relevance_score"] == 50.0


def test_the_web_page_has_a_place_for_the_score():
    page = app.test_client().get("/").get_data(as_text=True)
    assert 'id="relevance-score"' in page
    assert 'id="score-bar"' in page
    script = app.test_client().get("/scripts.js").get_data(as_text=True)
    assert "relevance_score" in script
