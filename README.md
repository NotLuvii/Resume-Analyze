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
   pip install -r requirements.txt
   ```
If a requirements.txt file is not present, you can install these dependencies manually:

```
pip install matplotlib pandas tkinterdnd2 language-tool-python pdfplumber
```

# **Usage**

## **Running the Application**

1. Clone the repository or download the project files.
2. Navigate to the project directory.

## **Functionality**

### **1. Job Keywords Tab**

- Enter the job description in the provided text box.
- Click **Extract Job Keywords** to extract technical and soft skills.

### **2. Resume Analysis Tab**

- Drag and drop resumes into the designated area.
- The app will analyze resumes for:
  - Relevance scores.
  - Matched technical and soft skills.
  - Overall performance against the job description.

### **3. Graphical Reports Tab**

- View visualizations for:
  - Skills frequency across resumes.
  - Distribution of relevance scores.

### **4. Interview Preparation Insights Tab**

- Review interview questions generated from the job description.
- Questions are categorized into technical, soft skills, and general scenarios.

# **Known Issues**

1. **Drag-and-Drop Limitations**:
   - Dragging unsupported file types or corrupted files may cause errors.
   - Ensure resumes are in PDF or text format for accurate analysis.

2. **Keyword Extraction Challenges**:
   - Certain job descriptions with complex phrasing or unconventional formatting may lead to incomplete keyword extraction.

3. **Graphical Reports Overlap**:
   - If too many skills are displayed in the frequency chart, labels may overlap or be hard to read.

4. **Large Resumes Processing Time**:
   - Analyzing long resumes may take noticeable time, especially if they contain extensive content.

5. **Resolution Dependence**:
   - The app may not scale well on very small screens or non-standard resolutions.

6. **Customization Limitations**:
   - Job relevance weights for keywords are static and do not dynamically adjust based on user preferences.

7. **Resume Scoring Inconsistencies**:
   - Scores may vary significantly for resumes with creative formatting or unconventional layouts.

8. **Scrollbars in Graphical Reports**:
   - Scrollbars may not function smoothly on some systems when the graphical reports exceed the frame size.
