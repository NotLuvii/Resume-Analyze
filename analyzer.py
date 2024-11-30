import re
import spacy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import matplotlib.pyplot as plt
import language_tool_python
# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Predefined skill categories
TECHNICAL_KEYWORDS = [
    # Programming Languages
    "python", "java", "c#", "c++", "javascript", "typescript", "swift", "kotlin", 
    "ruby", "php", "go", "rust", "r", "scala", "perl", "sql", "nosql", "bash", 
    "powershell", "vhdl", "matlab", "assembly", "html", "css", "sass", "less",
    "apex", "objective-c", "fortran", "cobol", "julia",

    # Frameworks and Libraries
    "react", "angular", "vue", "svelte", "django", "flask", "fastapi", "spring", 
    "laravel", "rails", "express", "nestjs", "nextjs", "nuxtjs", "asp.net", 
    "flutter", "react native", "ionic", "electron", "bootstrap", "material-ui", 
    "tailwindcss", "three.js", "chart.js", "d3.js", "ant design", "qt", "tkinter",

    # Cloud Platforms
    "aws", "azure", "google cloud platform", "gcp", "oracle cloud", "ibm cloud", 
    "salesforce", "digitalocean", "heroku", "cloudflare", "alibaba cloud", 
    "sap hana", "openstack", "red hat openshift",

    # Databases
    "mysql", "postgresql", "mongodb", "cassandra", "couchdb", "firebase", "sqlite", 
    "oracle", "dynamodb", "mariadb", "redis", "elasticsearch", "neo4j", "snowflake", 
    "redshift", "cosmos db", "clickhouse", "hbase", "arangodb", "timescaledb",

    # DevOps and CI/CD Tools
    "docker", "kubernetes", "jenkins", "terraform", "ansible", "puppet", "chef", 
    "circleci", "travisci", "gitlab ci", "github actions", "bitbucket pipelines", 
    "artifactory", "vagrant", "helm", "openshift", "bamboo", "spinnaker", 
    "azure devops",

    # Machine Learning and Data Science
    "tensorflow", "pytorch", "scikit-learn", "keras", "numpy", "pandas", "matplotlib", 
    "seaborn", "plotly", "jupyter", "hadoop", "spark", "hive", "pig", "airflow", 
    "data wrangling", "data pipelines", "etl", "mlflow", "opencv", "deep learning", 
    "nlp", "huggingface", "caffe", "xgboost", "lightgbm", "catboost", "databricks",

    # Game Development
    "unity", "unreal engine", "godot", "cryengine", "phaser", "game maker studio", 
    "cocos2d", "blender", "maya", "zbrush", "autodesk", "asset management", 
    "shader programming", "directx", "opengl", "vulkan", "havok", "crytek",

    # Mobile Development
    "android", "ios", "xcode", "android studio", "swiftui", "jetpack compose", "flutter", 
    "react native", "cordova", "xamarin", "kotlin multiplatform mobile",

    # Web Development
    "seo", "wcag", "web accessibility", "graphql", "rest", "soap", "websockets", 
    "swagger", "openapi", "json", "xml", "html", "css", "javascript",

    # Networking and Cybersecurity
    "wireshark", "nmap", "metasploit", "burpsuite", "tcpdump", "tls", "ssl", "vpn", 
    "firewalls", "osint", "penetration testing", "ethical hacking", "iso 27001", "soc2", 
    "pci dss", "gdpr", "hipaa", "siem", "zero trust", "splunk", "snort", "owasp", 
    "cyberark", "fortigate", "zscaler", "carbon black", "cisco", "ngfw", "palo alto",

    # Internet of Things (IoT)
    "mqtt", "coap", "zigbee", "z-wave", "ble", "lorawan", "aws iot", "google iot", 
    "azure iot", "raspberry pi", "arduino", "esp8266", "esp32", "iot edge computing",

    # Blockchain and Cryptography
    "ethereum", "bitcoin", "solidity", "web3", "hyperledger", "corda", "truffle", 
    "ganache", "ipfs", "cryptography", "rsa", "elliptic curve", "sha-256", "smart contracts",

    # Robotics and Embedded Systems
    "ros", "gazebo", "robotics", "arduino", "raspberry pi", "pid control", "px4", 
    "autonomous navigation", "embedded c", "vhdl", "fpga", "rtos", "micropython",

    # Big Data and Analytics
    "hadoop", "spark", "kafka", "hive", "pig", "mapreduce", "flink", "storm", 
    "druid", "superset", "tableau", "power bi", "qlikview", "splunk analytics",

    # Project Management and Agile Tools
    "jira", "trello", "asana", "monday.com", "clickup", "confluence", "scrum", 
    "kanban", "agile", "xp", "lean", "waterfall", "version control", "ci/cd",

    # General Tools
    "git", "github", "gitlab", "bitbucket", "svn", "powershell", "bash scripting", 
    "vscode", "intellij", "pycharm", "eclipse"
]


SOFT_SKILLS_KEYWORDS = [
    # Communication and Collaboration
    "communication", "collaboration", "teamwork", "public speaking", 
    "presentation skills", "negotiation", "active listening", 
    "cross-functional collaboration",

    # Problem-Solving and Critical Thinking
    "problem-solving", "critical thinking", "decision making", 
    "analytical skills", "troubleshooting", "logical reasoning", 
    "creative thinking",

    # Leadership and Management
    "leadership", "people management", "delegation", "mentoring", 
    "coaching", "conflict resolution", "team management", "influence", 
    "stakeholder management",

    # Time Management and Organization
    "time management", "organization", "multitasking", 
    "prioritization", "planning", "deadline management", 
    "scheduling",

    # Adaptability and Resilience
    "adaptability", "flexibility", "resilience", "stress management", 
    "change management", "growth mindset", "emotional intelligence",

    # Innovation and Creativity
    "creativity", "innovation", "brainstorming", "ideation", 
    "design thinking", "strategic thinking", "visionary thinking",

    # Attention to Detail
    "attention to detail", "accuracy", "thoroughness", "quality assurance"
]

CUSTOM_STOPWORDS = set([
    "a", "all", "its", "and", "of", "the", "for", "to", "an", "in", "with", "on", "at", 
    "job", "description", "role", "responsibilities", "requirements", "about", 
    "benefits", "skills", "employees", "company", "this", "as", "we"
])

def remove_stopwords(text):
    """
    Removes stopwords and custom noise words from the text.
    """
    words = text.lower().split()
    return [word for word in words if word not in ENGLISH_STOP_WORDS and word not in CUSTOM_STOPWORDS]

def extract_noun_phrases(text):
    """
    Extracts meaningful noun phrases using spaCy (e.g., "cloud applications").
    """
    doc = nlp(text)
    return [chunk.text.lower() for chunk in doc.noun_chunks]

def match_predefined_keywords(words, predefined_keywords):
    """
    Matches words or phrases against a predefined list of technical and soft skills keywords.
    """
    return [word for word in words if word in predefined_keywords]


def extract_keywords_pipeline(text):
    """
    Extracts and categorizes keywords into technical and soft skills.
    """
    # Step 1: Clean and preprocess text
    text = re.sub(r"[^\w\s]", "", text.lower())  # Remove special characters, normalize to lowercase
    filtered_words = remove_stopwords(text)  # Remove stopwords
    noun_phrases = extract_noun_phrases(text)  # Extract meaningful multi-word terms

    # Step 2: Combine keywords
    combined_keywords = set(filtered_words + noun_phrases)

    # Step 3: Match and categorize
    technical_skills = [
        keyword for keyword in combined_keywords if keyword in TECHNICAL_KEYWORDS
    ]
    soft_skills = [
        keyword for keyword in combined_keywords if keyword in SOFT_SKILLS_KEYWORDS
    ]

    return {
        "technical_skills": sorted(technical_skills),
        "soft_skills": sorted(soft_skills)
    }


def calculate_keyword_weights(job_keywords):
    """
    Dynamically calculate weights for each keyword based on frequency in the job description.
    """
    keyword_weights = {}
    all_keywords = job_keywords["technical_skills"] + job_keywords["soft_skills"]
    
    # Count frequency of each keyword in the job description
    for keyword in all_keywords:
        count = job_keywords["text"].lower().count(keyword.lower())
        keyword_weights[keyword] = count

    # Normalize weights to ensure they sum up to 1
    total_count = sum(keyword_weights.values())
    if total_count > 0:
        for keyword in keyword_weights:
            keyword_weights[keyword] /= total_count

    return keyword_weights

def weighted_relevance_score(matched_keywords, keyword_weights):
    """
    Calculates a weighted relevance score based on dynamically calculated weights.
    """
    total_weight = sum(keyword_weights.values())
    achieved_weight = sum(keyword_weights.get(kw, 0) for kw in matched_keywords)

    return (achieved_weight / total_weight * 100) if total_weight > 0 else 0

def gap_analysis(resume_keywords, job_keywords):
    """
    Performs gap analysis to identify missing keywords in resumes.
    Args:
        resume_keywords (dict): Extracted keywords from the resume.
        job_keywords (dict): Keywords extracted from the job description.

    Returns:
        dict: Missing technical and soft skills.
    """
    missing_technical = set(job_keywords["technical_skills"]) - set(resume_keywords["technical_skills"])
    missing_soft = set(job_keywords["soft_skills"]) - set(resume_keywords["soft_skills"])
    
    return {
        "Missing Technical Skills": sorted(missing_technical),
        "Missing Soft Skills": sorted(missing_soft)
    }
    

def analyze_resume(text, job_keywords):
    """
    Analyzes a resume by comparing its content with job description keywords.
    Includes weighted scoring and gap analysis.
    """
    extracted_keywords = extract_keywords_pipeline(text)
    technical_matched = set(extracted_keywords["technical_skills"]) & set(job_keywords["technical_skills"])
    soft_matched = set(extracted_keywords["soft_skills"]) & set(job_keywords["soft_skills"])

    gap = gap_analysis(extracted_keywords, job_keywords)
    keyword_weights = calculate_keyword_weights(job_keywords)
    total_matched = list(technical_matched) + list(soft_matched)
    weighted_score = weighted_relevance_score(total_matched, keyword_weights)

    return {
        "Extracted Keywords": extracted_keywords,
        "Matched Keywords": {
            "technical_skills": sorted(technical_matched),
            "soft_skills": sorted(soft_matched)
        },
        "Missing Keywords": gap,
        "Relevance Score": weighted_score
    }
    
def parse_certifications(resume_text):
    # Use regex to find certifications (e.g., AWS Certified, Google Cloud Certified)
    certification_patterns = [
        r"(AWS Certified.*)",
        r"(Google Cloud Certified.*)",
        r"(Certified.*Professional.*)",
    ]
    certifications = []
    for pattern in certification_patterns:
        certifications += re.findall(pattern, resume_text, flags=re.IGNORECASE)
    return list(set(certifications))


def parse_education(resume_text):
    # Extract degrees, institutions, and graduation years
    degree_patterns = [
        r"(Bachelor's|Master's|PhD|Diploma|Associate Degree).*",
        r"(B\.Sc\.|M\.Sc\.|MBA|B\.Tech|M\.Tech).*",
    ]
    institution_patterns = [
        r"([A-Z][a-z]+\sUniversity)",
        r"([A-Z][a-z]+ Institute of Technology)",
    ]
    year_pattern = r"(19|20)\d{2}"

    degrees = []
    institutions = []
    years = []

    for pattern in degree_patterns:
        degrees += re.findall(pattern, resume_text, flags=re.IGNORECASE)

    for pattern in institution_patterns:
        institutions += re.findall(pattern, resume_text, flags=re.IGNORECASE)

    years += re.findall(year_pattern, resume_text)

    return {"Degrees": list(set(degrees)), "Institutions": list(set(institutions)), "Years": list(set(years))}


def parse_work_experience(resume_text):
    # Extract job titles, companies, and durations
    sentences = sent_tokenize(resume_text)
    job_title_patterns = [
        r"(Software Engineer|Data Scientist|Project Manager|Developer|Analyst).*",
    ]
    company_patterns = [
        r"(at [A-Z][a-z]+.*)",
    ]
    duration_pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}\s(to|-\s)\s(?:Present|\d{4})"

    job_titles = []
    companies = []
    durations = []

    for sentence in sentences:
        for pattern in job_title_patterns:
            job_titles += re.findall(pattern, sentence, flags=re.IGNORECASE)

        for pattern in company_patterns:
            companies += re.findall(pattern, sentence, flags=re.IGNORECASE)

        durations += re.findall(duration_pattern, sentence, flags=re.IGNORECASE)

    return {"Job Titles": list(set(job_titles)), "Companies": list(set(companies)), "Durations": list(set(durations))}


def parse_social_links(resume_text):
    # Extract LinkedIn, GitHub, and portfolio links
    linkedin_pattern = r"https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9-_/]+"
    github_pattern = r"https?://(www\.)?github\.com/[a-zA-Z0-9-_/]+"
    portfolio_pattern = r"https?://[a-zA-Z0-9-_]+\.(com|net|org)/?[a-zA-Z0-9-_/]*"

    linkedin_links = re.findall(linkedin_pattern, resume_text, flags=re.IGNORECASE)
    github_links = re.findall(github_pattern, resume_text, flags=re.IGNORECASE)
    portfolio_links = re.findall(portfolio_pattern, resume_text, flags=re.IGNORECASE)

    return {
        "LinkedIn": list(set(linkedin_links)),
        "GitHub": list(set(github_links)),
        "Portfolios": list(set(portfolio_links)),
    }


def generate_interview_questions(job_description):
    """
    Analyze job description keywords and suggest potential interview questions.
    """
    keywords = extract_keywords_pipeline(job_description)  # Reuse your existing keyword extraction function
    questions = []

    # Technical Skills-Based Questions
    for skill in keywords["technical_skills"]:
        questions.extend([
            f"Can you explain your experience with {skill}?",
            f"How have you applied {skill} in previous projects?",
            f"What challenges have you faced while using {skill}?",
            f"Can you describe an innovative way you've used {skill} to solve a problem?",
            f"How would you improve your proficiency with {skill}?",
            f""
        ])

    # Soft Skills-Based Questions
    for skill in keywords["soft_skills"]:
        questions.extend([
            f"How do you demonstrate {skill} in a team setting?",
            f"Can you provide an example where {skill} helped you overcome a challenge?",
            f"How would you rate your {skill}, and why?",
            f"How do you ensure consistent {skill} in high-pressure environments?",
            f"Describe a situation where {skill} was crucial to the success of a project.",
            f""
        ])

    # General Career-Related Questions
    questions.extend([
        "Why are you interested in this role?",
        "What do you know about our company?",
        "How do you stay updated with the latest trends in your field?",
        "What motivates you to perform well in a job?",
        "How do you see yourself growing in this position over the next 3–5 years?"
    ])

    # Situational and Behavioral Questions
    questions.extend([
        "Describe a time when you had to lead a team under tight deadlines.",
        "Can you share an example of a challenging problem you solved?",
        "How do you handle conflicts within a team?",
        "What would you do if you disagreed with your manager’s decision?",
        "Can you provide an example of a project where you worked collaboratively with a cross-functional team?"
    ])

    # Questions About Work Experience
    questions.extend([
        "Can you walk us through a key project you worked on?",
        "What was your role in the project, and how did you contribute to its success?",
        "What would you say is your greatest professional achievement?",
        "How do you prioritize tasks when working on multiple projects simultaneously?",
        "What have you learned from a failure in your previous roles?"
    ])

    # Questions for Leadership and Initiative
    questions.extend([
        "Have you ever taken initiative to improve a process or solve a problem?",
        "Can you share an example of how you motivated your team during a tough project?",
        "How do you ensure effective communication as a team leader?",
        "What strategies do you use to delegate tasks effectively?",
        "Describe a time you had to make a difficult decision as a leader."
    ])

    # Technical Problem-Solving
    questions.extend([
        "How would you debug a complex technical issue?",
        "Can you describe your process for reviewing code?",
        "How do you stay updated with new technologies or programming languages?",
        "What steps would you take to optimize system performance?",
        "Describe a time you worked on integrating new technologies into an existing system."
    ])

    # Teamwork and Collaboration
    questions.extend([
        "How do you approach working with team members who have different work styles?",
        "Can you share an example of a successful collaboration?",
        "How do you handle disagreements or conflicting ideas within a team?",
        "What role do you usually take in team projects?",
        "How do you ensure your contributions align with team goals?"
    ])

    # Questions on Learning and Adaptability
    questions.extend([
        "Can you share a time when you had to learn a new skill quickly?",
        "How do you adapt to changes in project requirements?",
        "What steps do you take to improve your professional skills?",
        "Describe a time when you had to pivot from an original plan to achieve a goal.",
        "How do you handle feedback or criticism from peers or managers?"
    ])

    return questions
