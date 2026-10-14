"""The Tkinter desktop version: needs Tk and a display, so it's skipped where neither exists."""
import os
import types

import pytest

pytest.importorskip("tkinter")
pytest.importorskip("tkinterdnd2")
if os.name != "nt" and not os.environ.get("DISPLAY"):
    pytest.skip("needs a display (run under xvfb-run on Linux)", allow_module_level=True)

from tkinter import ttk  # noqa: E402

from tkinterdnd2 import TkinterDnD  # noqa: E402

import main  # noqa: E402


@pytest.fixture
def app():
    root = TkinterDnD.Tk()
    yield main.ResumeAnalyzerApp(root)
    root.destroy()


def set_job(app, text):
    app.job_desc_text.delete("1.0", "end")
    app.job_desc_text.insert("1.0", text)
    app.extract_job_keywords()


def result_rows(app):
    (table,) = [w for w in app.analysis_display.winfo_children() if isinstance(w, ttk.Treeview)]
    return [table.item(row)["values"] for row in table.get_children()]


def test_dropping_a_resume_shows_its_score_and_draws_the_charts(app, tmp_path, docx_bytes):
    path = tmp_path / "resume.docx"
    path.write_bytes(docx_bytes("Python and SQL"))
    set_job(app, "Python, Python, SQL and Docker")
    app.handle_drop(types.SimpleNamespace(data=str(path)))
    name, score, technical, soft = result_rows(app)[0]
    assert (name, score) == ("resume.docx", "75.0%")
    assert len(app.graph_frame.winfo_children()) == 2


def test_changing_the_job_description_rescores_the_resumes_already_dropped(app, tmp_path, docx_bytes):
    path = tmp_path / "resume.docx"
    path.write_bytes(docx_bytes("Python and SQL"))
    set_job(app, "Python, SQL")
    app.handle_drop(types.SimpleNamespace(data=str(path)))
    set_job(app, "Docker and Kubernetes")
    assert [row[:2] for row in result_rows(app)] == [["resume.docx", "0.0%"]]
