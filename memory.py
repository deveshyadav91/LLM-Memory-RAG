import os

MEMORY_DIR = "memories"

os.makedirs(MEMORY_DIR, exist_ok=True)


TECH_KEYWORDS = [
    "python",
    "c++",
    "java",
    "fastapi",
    "machine learning",
    "deep learning",
    "opencv",
    "pytorch",
    "tensorflow",
    "sql",
    "faiss",
    "streamlit",
    "rag",
    "llm",
    "sentence transformers",
    "gemini",
    "computer vision",
    "yolo",
    "lightfm"
]


def clean_user_line(line):
    line = line.strip()

    if not line.lower().startswith("user:"):
        return None

    return line[5:].strip()


def extract_memory(conversation: str):

    profile = []
    skills = []
    projects = []
    preferences = []
    goals = []

    lines = conversation.splitlines()

    for line in lines:

        clean_line = clean_user_line(line)

        if not clean_line:
            continue

        text = clean_line.lower()

        # ---------------- PROFILE ----------------

        if any(keyword in text for keyword in [
            "my name is",
            "i am a student",
            "i'm a student",
            "b.tech",
            "btech",
            "m.tech",
            "mtech",
            "college",
            "university",
            "iit"
        ]):
            profile.append(clean_line)

        # ---------------- SKILLS ----------------

        if any(tech in text for tech in TECH_KEYWORDS):
            skills.append(clean_line)

        # ---------------- PROJECTS ----------------

        project_keywords = [
            "my project",
            "my projects",
            "working on",
            "building",
            "developing",
            "creating",
            "project is",
            "project called",
            "project named"
        ]

        if any(keyword in text for keyword in project_keywords):

            projects.append(clean_line)

        # ---------------- PREFERENCES ----------------

        if any(keyword in text for keyword in [
            "i like",
            "i prefer",
            "i love",
            "favorite",
            "favourite",
            "i don't like",
            "i dislike"
        ]):
            preferences.append(clean_line)

        # ---------------- GOALS ----------------

        if any(keyword in text for keyword in [
            "i want",
            "my goal",
            "my aim",
            "i plan to",
            "i am planning to",
            "i hope to"
        ]):
            goals.append(clean_line)

    profile = unique(profile)
    skills = sorted(set(skills))
    projects = unique(projects)
    preferences = unique(preferences)
    goals = unique(goals)

    save_md("profile.md", profile)
    save_md("skills.md", skills)
    save_md("projects.md", projects)
    save_md("preferences.md", preferences)
    save_md("goals.md", goals)

    return {
        "profile": profile,
        "skills": skills,
        "projects": projects,
        "preferences": preferences,
        "goals": goals
    }


def unique(items):

    seen = set()
    result = []

    for item in items:

        key = item.lower().strip()

        if key not in seen:
            seen.add(key)
            result.append(item.strip())

    return result


def save_md(filename, data):

    path = os.path.join(MEMORY_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Memory\n\n")

        if not data:
            f.write("No memory found.\n")
            return

        for item in data:
            f.write(f"- {item}\n")