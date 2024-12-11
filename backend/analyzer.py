import re
import spacy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import matplotlib.pyplot as plt
import language_tool_python
import spacy
from pathlib import Path
import os
# Load spaCy's English model


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
    words = text.lower().split()
    return [word for word in words if word not in ENGLISH_STOP_WORDS and word not in CUSTOM_STOPWORDS]

def extract_keywords_pipeline(text):
    text = re.sub(r"[^\w\s]", "", text.lower())
    filtered_words = remove_stopwords(text)

    technical_skills = [word for word in filtered_words if word in TECHNICAL_KEYWORDS]
    soft_skills = [word for word in filtered_words if word in SOFT_SKILLS_KEYWORDS]

    return {
        "technical_skills": sorted(set(technical_skills)),
        "soft_skills": sorted(set(soft_skills))
    }

def calculate_keyword_weights(job_keywords):
    keyword_weights = {}
    all_keywords = job_keywords["technical_skills"] + job_keywords["soft_skills"]
    for keyword in all_keywords:
        count = job_keywords["text"].lower().count(keyword.lower())
        keyword_weights[keyword] = count
    total_count = sum(keyword_weights.values())
    if total_count > 0:
        for keyword in keyword_weights:
            keyword_weights[keyword] /= total_count
    return keyword_weights

def analyze_resume(resume_text, job_keywords):
    extracted_keywords = extract_keywords_pipeline(resume_text)
    technical_matched = set(extracted_keywords["technical_skills"]) & set(job_keywords["technical_skills"])
    soft_matched = set(extracted_keywords["soft_skills"]) & set(job_keywords["soft_skills"])
    gap = {
        "missing_technical": list(set(job_keywords["technical_skills"]) - technical_matched),
        "missing_soft": list(set(job_keywords["soft_skills"]) - soft_matched)
    }
    return {
        "matched_technical": list(technical_matched),
        "matched_soft": list(soft_matched),
        "gap_analysis": gap
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
