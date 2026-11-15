import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
import pandas as pd


FEATURE_COLUMNS = [
    "stars",
    "forks",
    "repo_age_days",
    "days_since_last_push",
    "Ant",
    "Buildr",
    "Gradle",
    "Make",
    "Maven",
    "SBT",
    "Ivy",
    "Eclipse",
    "IntelliJ IDEA",
    "NetBeans",
    "Travis CI",
    "Git submodules",
    "tool"
]


def parse_github_url(repo_url):
    parsed = urlparse(repo_url)

    if parsed.hostname not in ("github.com", "www.github.com"):
        raise ValueError("Please provide a valid GitHub repository URL.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("GitHub URL must contain owner and repository.")

    return parts[0], parts[1].removesuffix(".git")


def get_repository_features(repo_url):
    owner, repo = parse_github_url(repo_url)

    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(
        api_url,
        headers={"Accept": "application/vnd.github+json"},
        timeout=20
    )
    response.raise_for_status()

    metadata = response.json()

    now = datetime.now(timezone.utc)

    created = datetime.fromisoformat(
        metadata["created_at"].replace("Z", "+00:00")
    )

    pushed = datetime.fromisoformat(
        metadata["pushed_at"].replace("Z", "+00:00")
    )

    repo_age_days = max(0, (now - created).total_seconds() / 86400)
    days_since_last_push = max(0, (now - pushed).total_seconds() / 86400)

    tree_url = (
        f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD"
        "?recursive=1"
    )

    tree_response = requests.get(
        tree_url,
        headers={"Accept": "application/vnd.github+json"},
        timeout=30
    )
    tree_response.raise_for_status()

    tree = tree_response.json().get("tree", [])

    file_paths = [
        item["path"].lower()
        for item in tree
        if item["type"] == "blob"
    ]

    def contains_file(filename):
        return any(
            Path(path).name.lower() == filename.lower()
            for path in file_paths
        )

    def contains_folder(folder):
        return any(
            f"/{folder.lower()}/" in f"/{path}/"
            for path in file_paths
        )

    maven = contains_file("pom.xml")
    gradle = (
        contains_file("build.gradle")
        or contains_file("build.gradle.kts")
    )
    ant = contains_file("build.xml")

    if maven:
        tool = "Maven"
    elif gradle:
        tool = "Gradle"
    elif ant:
        tool = "Ant"
    else:
        tool = "Unknown"

    features = {
        "stars": metadata.get("stargazers_count", 0),
        "forks": metadata.get("forks_count", 0),
        "repo_age_days": repo_age_days,
        "days_since_last_push": days_since_last_push,
        "Ant": int(ant),
        "Buildr": int(contains_file("buildfile")),
        "Gradle": int(gradle),
        "Make": int(contains_file("makefile")),
        "Maven": int(maven),
        "SBT": int(
            contains_file("build.sbt")
        ),
        "Ivy": int(
            any("ivy.xml" in path for path in file_paths)
        ),
        "Eclipse": int(contains_folder(".settings")),
        "IntelliJ IDEA": int(
            contains_folder(".idea")
        ),
        "NetBeans": int(
            contains_folder("nbproject")
        ),
        "Travis CI": int(
            contains_file(".travis.yml")
        ),
        "Git submodules": int(
            contains_file(".gitmodules")
        ),
        "tool": tool
    }

    return pd.DataFrame(
        [features],
        columns=FEATURE_COLUMNS
    )


if __name__ == "__main__":
    url = input("Enter public GitHub repository URL: ").strip()

    try:
        data = get_repository_features(url)
        print("\nRepository features:")
        print(data.T.to_string())
    except Exception as error:
        print(f"Feature extraction failed: {error}")
