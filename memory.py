import os
import re

MEMORY_DIR = "memories"

os.makedirs(MEMORY_DIR, exist_ok=True)


def extract_memory(conversation: str):

    profile = []
    skills = []
    projects = []
    preferences = []
    goals = []

    lines = conversation.split("\n")

    for line in lines:

        text = line.lower()

        # ---------- Name ----------
        if "my name is" in text:
            profile.append(line.replace("User:", "").strip())

        # ---------- Education ----------
        if any(x in text for x in [
            "student",
            "m.tech",
            "b.tech",
            "college",
            "university"
        ]):
            profile.append(line.replace("User:", "").strip())

        # ---------- Skills ----------
        tech = [
            "python",
            "c++",
            "java",
            "fastapi",
            "machine learning",
            "deep learning",
            "opencv",
            "pytorch",
            "tensorflow",
            "sql"
        ]

        for t in tech:
            if t in text:
                skills.append(t)

        # ---------- Projects ----------
        if any(x in text for x in [
            "building",
            "project",
            "developing",
            "creating"
        ]):
            projects.append(line.replace("User:", "").strip())

        # ---------- Preferences ----------
        if any(x in text for x in [
            "i like",
            "i prefer",
            "favorite"
        ]):
            preferences.append(line.replace("User:", "").strip())

        # ---------- Goals ----------
        if any(x in text for x in [
            "i want",
            "my goal",
            "aim"
        ]):
            goals.append(line.replace("User:", "").strip())

    save_md("profile.md", profile)
    save_md("skills.md", sorted(set(skills)))
    save_md("projects.md", projects)
    save_md("preferences.md", preferences)
    save_md("goals.md", goals)


def save_md(filename, data):

    path = os.path.join(MEMORY_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Memory\n\n")

        if not data:
            f.write("No memory found.\n")
            return

        for item in data:
            f.write(f"- {item}\n")