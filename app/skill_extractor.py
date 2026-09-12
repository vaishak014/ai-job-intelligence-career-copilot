import re


SKILL_TAXONOMY = {
    "Python": {
        "category": "Programming",
        "aliases": [
            "python",
            "python 3",
            "python3",
            "python programming"
        ]
    },

    "Java": {
        "category": "Programming",
        "aliases": [
            "java"
        ]
    },

    "JavaScript": {
        "category": "Programming",
        "aliases": [
            "javascript",
            "js"
        ]
    },

    "TypeScript": {
        "category": "Programming",
        "aliases": [
            "typescript",
            "ts"
        ]
    },

    "C": {
        "category": "Programming",
        "aliases": [
            "c programming",
            "c language"
        ]
    },

    "C++": {
        "category": "Programming",
        "aliases": [
            "c++",
            "cpp"
        ]
    },

    "C#": {
        "category": "Programming",
        "aliases": [
            "c#",
            "c sharp"
        ]
    },

    "Go": {
        "category": "Programming",
        "aliases": [
            "golang"
        ]
    },

    "PHP": {
        "category": "Programming",
        "aliases": [
            "php"
        ]
    },

    "Dart": {
        "category": "Programming",
        "aliases": [
            "dart",
            "dart programming"
        ]
    },

    "Kotlin": {
        "category": "Programming",
        "aliases": [
            "kotlin"
        ]
    },

    "SQL": {
        "category": "Data",
        "aliases": [
            "sql",
            "structured query language"
        ]
    },

    "Pandas": {
        "category": "Data",
        "aliases": [
            "pandas",
            "pandas library"
        ]
    },

    "NumPy": {
        "category": "Data",
        "aliases": [
            "numpy",
            "numpy library"
        ]
    },

    "PySpark": {
        "category": "Data",
        "aliases": [
            "pyspark",
            "spark",
            "apache spark"
        ]
    },

    "PostgreSQL": {
        "category": "Data",
        "aliases": [
            "postgresql",
            "postgres",
            "postgres db",
            "postgres database"
        ]
    },

    "MySQL": {
        "category": "Data",
        "aliases": [
            "mysql",
            "mysql database"
        ]
    },

    "MongoDB": {
        "category": "Data",
        "aliases": [
            "mongodb",
            "mongo db",
            "mongo"
        ]
    },

    "Power BI": {
        "category": "Data",
        "aliases": [
            "power bi",
            "powerbi"
        ]
    },

    "Tableau": {
        "category": "Data",
        "aliases": [
            "tableau"
        ]
    },

    "Data Modeling": {
        "category": "Data",
        "aliases": [
            "data modeling",
            "data modelling"
        ]
    },

    "Time-Series Databases": {
        "category": "Data",
        "aliases": [
            "time-series databases",
            "time series databases",
            "time-series database",
            "time series database"
        ]
    },

    "FastAPI": {
        "category": "Backend",
        "aliases": [
            "fastapi",
            "fast api"
        ]
    },

    "Flask": {
        "category": "Backend",
        "aliases": [
            "flask"
        ]
    },

    "Django": {
        "category": "Backend",
        "aliases": [
            "django"
        ]
    },

    "Node.js": {
        "category": "Backend",
        "aliases": [
            "node.js",
            "nodejs",
            "node js"
        ]
    },

    "REST APIs": {
        "category": "Backend",
        "aliases": [
            "rest api",
            "rest apis",
            "restful api",
            "restful apis"
        ]
    },

    "GraphQL": {
        "category": "Backend",
        "aliases": [
            "graphql"
        ]
    },

    "HTML": {
        "category": "Frontend",
        "aliases": [
            "html",
            "html5"
        ]
    },

    "CSS": {
        "category": "Frontend",
        "aliases": [
            "css",
            "css3"
        ]
    },

    "React": {
        "category": "Frontend",
        "aliases": [
            "react",
            "reactjs",
            "react.js"
        ]
    },

    "Angular": {
        "category": "Frontend",
        "aliases": [
            "angular",
            "angularjs"
        ]
    },

    "Vue.js": {
        "category": "Frontend",
        "aliases": [
            "vue",
            "vue.js",
            "vuejs"
        ]
    },

    "Next.js": {
        "category": "Frontend",
        "aliases": [
            "next.js",
            "nextjs",
            "next js"
        ]
    },

    "Responsive Design": {
        "category": "Frontend",
        "aliases": [
            "responsive design",
            "responsive web design"
        ]
    },

    "Machine Learning": {
        "category": "AI / ML",
        "aliases": [
            "machine learning",
            "ml"
        ]
    },

    "scikit-learn": {
        "category": "AI / ML",
        "aliases": [
            "scikit-learn",
            "sklearn",
            "scikit learn"
        ]
    },

    "TensorFlow": {
        "category": "AI / ML",
        "aliases": [
            "tensorflow"
        ]
    },

    "PyTorch": {
        "category": "AI / ML",
        "aliases": [
            "pytorch",
            "torch"
        ]
    },

    "Deep Learning": {
        "category": "AI / ML",
        "aliases": [
            "deep learning"
        ]
    },

    "Natural Language Processing": {
        "category": "AI / ML",
        "aliases": [
            "natural language processing",
            "nlp"
        ]
    },

    "Generative AI": {
        "category": "AI / ML",
        "aliases": [
            "generative ai",
            "gen ai"
        ]
    },

    "Large Language Models": {
        "category": "AI / ML",
        "aliases": [
            "large language models",
            "large language model",
            "llm",
            "llms"
        ]
    },

    "AWS": {
        "category": "Cloud / DevOps",
        "aliases": [
            "aws",
            "amazon web services"
        ]
    },

    "Azure": {
        "category": "Cloud / DevOps",
        "aliases": [
            "azure",
            "microsoft azure"
        ]
    },

    "Google Cloud": {
        "category": "Cloud / DevOps",
        "aliases": [
            "gcp",
            "google cloud",
            "google cloud platform"
        ]
    },

    "Docker": {
        "category": "Cloud / DevOps",
        "aliases": [
            "docker",
            "docker containers"
        ]
    },

    "Kubernetes": {
        "category": "Cloud / DevOps",
        "aliases": [
            "kubernetes",
            "k8s"
        ]
    },

    "Git": {
        "category": "Tools / Platforms",
        "aliases": [
            "git",
            "git version control",
            "version control"
        ]
    },

    "GitHub": {
        "category": "Tools / Platforms",
        "aliases": [
            "github"
        ]
    },

    "Firebase": {
        "category": "Tools / Platforms",
        "aliases": [
            "firebase"
        ]
    },

    "CRM": {
        "category": "Tools / Platforms",
        "aliases": [
            "crm",
            "customer relationship management"
        ]
    },

    "Flutter": {
        "category": "Mobile",
        "aliases": [
            "flutter",
            "flutter framework"
        ]
    },

    "Android": {
        "category": "Mobile",
        "aliases": [
            "android",
            "android development"
        ]
    },

    "MVVM": {
        "category": "Software Architecture",
        "aliases": [
            "mvvm"
        ]
    },

    "MVP": {
        "category": "Software Architecture",
        "aliases": [
            "mvp architecture",
            "model view presenter"
        ]
    },

    "Data Structures and Algorithms": {
        "category": "Computer Science",
        "aliases": [
            "data structures and algorithms",
            "data structures",
            "algorithms",
            "dsa"
        ]
    },

    "Linux": {
        "category": "Operating Systems",
        "aliases": [
            "linux"
        ]
    }
}


SHORT_ALIASES = {
    "ml",
    "js",
    "ts",
    "c",
    "k8s",
    "gcp",
    "nlp",
    "llm",
    "llms",
    "dsa",
    "mvp",
    "crm"
}


def normalize_text(text):
    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^\w\s.+#-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def build_skill_pattern(keyword):
    normalized_keyword = normalize_text(
        keyword
    )

    escaped_keyword = re.escape(
        normalized_keyword
    )

    return (
        r"(?<![a-z0-9])"
        + escaped_keyword
        + r"(?![a-z0-9])"
    )


def extract_skills(text):
    normalized_text = normalize_text(text)

    if not normalized_text:
        return []

    detected_skills = []

    for canonical_skill, skill_data in (
        SKILL_TAXONOMY.items()
    ):
        for keyword in skill_data["aliases"]:

            pattern = build_skill_pattern(
                keyword
            )

            if re.search(
                pattern,
                normalized_text
            ):
                detected_skills.append(
                    canonical_skill
                )
                break

    return detected_skills


def get_skill_category(skill):
    skill_data = SKILL_TAXONOMY.get(skill)

    if skill_data is None:
        return None

    return skill_data["category"]
