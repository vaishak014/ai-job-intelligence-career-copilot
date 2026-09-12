from skill_extractor import extract_skills


test_cases = [
    "Python 3 programming with SQL",
    "Experience with PostgreSQL and Fast API",
    "Machine learning using sklearn",
    "Build applications using ReactJS and JavaScript",
    "Docker containers and Git version control"
]


for text in test_cases:
    skills = extract_skills(text)

    print()
    print("Text:", text)
    print("Normalized Skills:", skills)
