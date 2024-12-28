# **Resume Analyzer**

## **Overview**
The Resume Analyzer is a Python-based application designed to analyze resumes against job descriptions. It provides insights such as matched skills, relevance scores, and potential interview questions. The application is built using `Tkinter` for the graphical user interface (GUI) and integrates advanced text processing for keyword extraction, graphical reports, and interview preparation.

---

## **Features**
- **Drag-and-Drop Resumes**: Easily upload resumes using drag-and-drop functionality.
- **Keyword Extraction**: Extract technical and soft skills from job descriptions.
- **Resume Analysis**:
  - Match technical and soft skills from resumes against job descriptions.
  - Generate relevance scores based on keyword matches.
- **Interview Preparation**:
  - Suggest interview questions based on job description keywords.
  - Categorized questions for technical skills, soft skills, and situational scenarios.
- **Graphical Reports**:
  - View skills frequency charts.
  - Relevance score distribution graphs.
- **Responsive Design**:
  - Scalable window resolution.
  - Vertical scrolling for long content (e.g., interview questions).
 
## **Installation**

### **Prerequisites**
1. Install Python (version 3.8 or higher).
2. Install required Python libraries using `pip`:
```
pip install matplotlib pandas tkinterdnd2 language-tool-python pdfplumber
```
3. Run the Flask server:
```
python app.py
```
4. Open your browser and navigate to:
```
http://127.0.0.1:5000
```
# **Usage**

## **Running the Application**

1. Clone the repository or download the project files.
2. Navigate to the project directory.

## **Functionality**

### **1. Job Description Entry**

- Enter the job description in the provided text box.
- Click Analyze to start the analysis.

### **2. Resume Analysis Tab**

- Upload a resume in PDF or DOCX format using the file upload field.
- The app will analyze resumes for:
  - Relevance scores.
  - Matched technical and soft skills.

### **3. Results Display**

- Analysis Results:
  - Shows matched and missing skills.
  - Provides a breakdown of skills into technical and soft categories.
- Interview Questions:
  - Displays suggested interview questions based on the job description.


# **Known Issues**

1. **Resume Formatting**:
   - Unconventional resume layouts or excessive formatting may impact keyword extraction accuracy.

2. **Processing Time**:
   - Analyzing very large resumes can take longer than usual.

3. **Static Keyword Matching**:
   - The application uses static keyword lists and does not handle synonyms or alternative phrases dynamically.

## **Future Enhancements**
- Add synonym matching using NLP techniques.
- Improve UI with modern design frameworks like Tailwind CSS or Material UI.
- Export results to PDF or CSV.
- Integrate visualization features for graphical representation of results.
