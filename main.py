import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from backend.parser import extract_text
from backend.analyzer import *
import spacy
print(spacy.util.get_package_path("en_core_web_sm"))

class ResumeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Analyzer")
        self.root.geometry("1920x1080")  # Adjust resolution
        self.root.minsize(1000, 600)

        # Data storage
        self.results = []
        self.job_keywords = {"technical_skills": [], "soft_skills": []}

        # Style
        self.style = ttk.Style()
        self.style.configure("TNotebook", tabposition="n")
        self.style.configure("TNotebook.Tab", font=("Arial", 12))

        # Main Layout
        self.create_widgets()

    def create_widgets(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Job Keywords Tab
        self.job_keywords_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.job_keywords_frame, text="Job Keywords")

        # Resume Analysis Tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Resume Analysis")

        # Graph Reports Tab
        self.graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_frame, text="Graphical Reports")

        # Interview Insights Tab
        self.interview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.interview_frame, text="Interview Insights")

        # Setup tabs
        self.setup_job_keywords_tab()
        self.setup_resume_analysis_tab()
        self.setup_interview_tab()


    def setup_job_keywords_tab(self):
        # Job Description Input
        job_desc_label = ttk.Label(self.job_keywords_frame, text="Enter Job Description:", font=("Arial", 12))
        job_desc_label.pack(pady=5, anchor="w")

        self.job_desc_text = tk.Text(self.job_keywords_frame, height=8, font=("Arial", 10), wrap=tk.WORD)
        self.job_desc_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        # Extract Keywords Button
        keyword_button = ttk.Button(self.job_keywords_frame, text="Extract Job Keywords", command=self.extract_job_keywords)
        keyword_button.pack(pady=10)

        # Keywords Display Area
        self.keywords_display = ttk.LabelFrame(self.job_keywords_frame, text="Extracted Keywords", padding=(10, 5))
        self.keywords_display.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

    def setup_resume_analysis_tab(self):
        # Drag-and-Drop Area
        drop_label = ttk.Label(self.results_frame, text="Drag and Drop Resumes Here", font=("Arial", 14), anchor="center")
        drop_label.pack(pady=20, fill=tk.X)

        # Bind Drag-and-Drop functionality
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

        # Results Display Area
        self.analysis_display = ttk.LabelFrame(self.results_frame, text="Resume Analysis Results", padding=(10, 5))
        self.analysis_display.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

    def extract_job_keywords(self):
        # Clear previous keyword display
        for widget in self.keywords_display.winfo_children():
            widget.destroy()

        job_description = self.job_desc_text.get("1.0", tk.END).strip()
        if not job_description:
            tk.Label(self.keywords_display, text="No job description provided.", font=("Arial", 12)).pack()
            return

        # Extract keywords
        self.job_keywords = extract_keywords_pipeline(job_description)
        self.job_keywords["text"] = job_description

        # Display categorized keywords
        if self.job_keywords["technical_skills"]:
            ttk.Label(self.keywords_display, text="Technical Skills:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
            ttk.Label(
                self.keywords_display,
                text=", ".join(self.job_keywords["technical_skills"]),
                font=("Arial", 10), wraplength=900, justify="left"
            ).pack(anchor="w")

        if self.job_keywords["soft_skills"]:
            ttk.Label(self.keywords_display, text="Soft Skills:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
            ttk.Label(
                self.keywords_display,
                text=", ".join(self.job_keywords["soft_skills"]),
                font=("Arial", 10), wraplength=900, justify="left"
            ).pack(anchor="w")

        # Update interview preparation insights
        self.display_interview_questions(job_description)

        # Re-analyze resumes
        self.reanalyze_resumes()
    
    def handle_drop(self, event):
        file_paths = event.data.split()
        for file_path in file_paths:
            try:
                text = extract_text(file_path)  # Extract text from the resume
                analysis = analyze_resume(text, self.job_keywords)
  
                
                self.results.append({
                    "File Name": os.path.basename(file_path),
                    "File Path": file_path,
                    **analysis,
                })
            except Exception as e:
                self.results.append({"File Name": os.path.basename(file_path), "Error": str(e)})

        self.display_resume_results()

    def display_resume_results(self):
        # Clear previous analysis results
        for widget in self.analysis_display.winfo_children():
            widget.destroy()

        # Resume Table
        columns = ["File Name", "Relevance Score", "Matched Technical Skills", "Matched Soft Skills"]
        table = ttk.Treeview(self.analysis_display, columns=columns, show="headings", height=15)
        table.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=200, anchor=tk.CENTER)

        for result in self.results:
            table.insert("", tk.END, values=[
                result.get("File Name", "N/A"),
                f"{result.get('Relevance Score', 0):.2f}%",
                ", ".join(result["Matched Keywords"].get("technical_skills", [])),
                ", ".join(result["Matched Keywords"].get("soft_skills", []))
            ])

        # Update graphical reports
        self.generate_graphical_reports()

    def generate_graphical_reports(self):
        # Clear previous graphs
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Graph 1: Skills Frequency
        fig1 = plt.Figure(figsize=(8, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        skills_count = {}
        relevance_scores = []

        for result in self.results:
            for skill in result["Matched Keywords"]["technical_skills"]:
                skills_count[skill] = skills_count.get(skill, 0) + 1
            relevance_scores.append(result.get("Relevance Score", 0))

        ax1.bar(skills_count.keys(), skills_count.values(), color="blue")
        ax1.set_title("Percentage of Resumes Matching Specific Skills")
        ax1.set_xticks(range(len(skills_count.keys())))
        ax1.set_xticklabels(skills_count.keys(), rotation=45, ha="right")

        canvas1 = FigureCanvasTkAgg(fig1, self.graph_frame)
        canvas1.get_tk_widget().pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        # Graph 2: Relevance Score Distribution
        fig2 = plt.Figure(figsize=(8, 4), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.hist(relevance_scores, bins=10, color="skyblue", edgecolor="black")
        ax2.set_title("Relevance Scores Distribution")
        ax2.set_xlabel("Relevance Score")
        ax2.set_ylabel("Number of Resumes")

        canvas2 = FigureCanvasTkAgg(fig2, self.graph_frame)
        canvas2.get_tk_widget().pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

    def reanalyze_resumes(self):
        """
        Reanalyzes all uploaded resumes with the updated job keywords.
        """
        self.results = []  # Clear current results

        for result in self.results:
            file_path = result.get("File Path", "")
            if os.path.exists(file_path):
                try:
                    text = extract_text(file_path)
                    analysis = analyze_resume(text, self.job_keywords)
                    self.results.append({
                        "File Name": os.path.basename(file_path),
                        "File Path": file_path,
                        **analysis
                    })
                except Exception as e:
                    self.results.append({"File Name": os.path.basename(file_path), "Error": str(e)})

        self.display_resume_results()
        


    def setup_interview_tab(self):
    # Create a canvas to allow scrolling
        self.interview_canvas = tk.Canvas(self.interview_frame)
        self.scrollbar = ttk.Scrollbar(self.interview_frame, orient="vertical", command=self.interview_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.interview_canvas)

        # Configure the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.interview_canvas.configure(scrollregion=self.interview_canvas.bbox("all"))
        )
        self.interview_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.interview_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack widgets
        self.scrollbar.pack(side="right", fill="y")
        self.interview_canvas.pack(side="left", fill="both", expand=True)

    def display_interview_questions(self, job_description):
        # Generate interview questions
        questions = generate_interview_questions(job_description)

        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if questions:
            ttk.Label(self.scrollable_frame, text="Suggested Questions:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
            for question in questions:
                ttk.Label(self.scrollable_frame, text=f"- {question}", font=("Arial", 10), wraplength=1000, justify="left").pack(anchor="w", pady=2)
        else:
            ttk.Label(self.scrollable_frame, text="No relevant topics or questions found.", font=("Arial", 12)).pack()




if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ResumeAnalyzerApp(root)
    root.mainloop()
