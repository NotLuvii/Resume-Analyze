import re
import spacy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import matplotlib.pyplot as plt
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
    

