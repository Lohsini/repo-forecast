import pandas as pd
import requests
from datetime import datetime, timedelta, timezone
import time
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()
save_dir = "data/charts"


def fetch_issues(headers, repo, since, label):
    print(f"Fetching {label} issues from: {repo}")
    all_issues = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo}/issues"
        params = {
            "state": "all",
            "since": since,
            "per_page": 100,
            "page": page
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error fetching {repo} page {page}: {response.status_code}")
            break

        data = response.json()
        if not data:
            break
        for issue in data:
            if "pull_request" not in issue:
                all_issues.append({
                    "repo": repo,
                    "id": issue["id"],
                    "number": issue["number"],
                    "title": issue["title"],
                    "state": issue["state"],
                    "created_at": issue["created_at"],
                    "closed_at": issue["closed_at"]
                })
        page += 1
        time.sleep(1)  # avoid rate limit
    return all_issues


def filter_recent_issues(df: pd.DataFrame, days: int = 60, mode: str = "created_only") -> pd.DataFrame:
    # Format
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    df["closed_at"] = pd.to_datetime(df["closed_at"], utc=True)

    # Strict filter
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    if mode == "created_only":
        df = df[df["created_at"] >= cutoff_date].copy()
    elif mode == "created_or_closed":
        df = df[
            (df["created_at"] >= cutoff_date) |
            (df["closed_at"] >= cutoff_date)
        ]
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    # remove timezone and warning
    df["created_at"] = df["created_at"].dt.tz_localize(None)
    df["closed_at"] = df["closed_at"].dt.tz_localize(None)

    return df


def main():
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}

    repos = [
        "meta-llama/llama3",
        "ollama/ollama",
        "langchain-ai/langchain",
        "langchain-ai/langgraph",
        "microsoft/autogen",
        "openai/openai-cookbook",
        "elastic/elasticsearch",
        "milvus-io/pymilvus"
    ]

    os.makedirs(save_dir, exist_ok=True)

    # Fetch GitHub Issues
    print("=== Fetching GitHub issues ===")
    now = datetime.today()
    since_2_months = (now - timedelta(days=60)).isoformat() + "Z"

    issues_2_months = []
    for repo in repos:
        issues_2_months += fetch_issues(headers,
                                        repo, since_2_months, "2-month")

    df = pd.DataFrame(issues_2_months)
    print("==== Fetching repo Done ====")
    print(f"Total: {len(df)}")

    # Format and strict filter
    df = filter_recent_issues(df, days=60, mode="created_only")

    df["repo"] = df["repo"].astype(str)

    # 2. A Line Chart to plot the issues for every Repo
    print("=== 2. Issues Per Day (Line Chart) ===")
    df["day"] = df["created_at"].dt.date
    daily_df = df.groupby(["repo", "day"]).size(
    ).reset_index(name="issue_count")
    pivot_df = daily_df.pivot(
        index="day", columns="repo", values="issue_count").fillna(0)

    plt.figure()
    pivot_df.plot(kind="line", marker="o", figsize=(14, 6))
    plt.title("Issues per Day per Repository")
    plt.xlabel("Date")
    plt.ylabel("Issue Count")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/2.daily_issues.png")
    plt.close()

    # 3. A Bar Chart to plot the issues created for every month for every Repo
    print("=== 3. Monthly Issues (Bar Chart) ===")
    df["month"] = df["created_at"].dt.to_period("M").astype(str)
    monthly_df = df.groupby(["repo", "month"]).size(
    ).reset_index(name="issue_count")
    pivot_df = monthly_df.pivot(
        index="month", columns="repo", values="issue_count").fillna(0)

    pivot_df.plot(kind="bar", figsize=(16, 7), width=0.85)
    plt.title("Monthly Created Issues per Repository")
    plt.xlabel("Month")
    plt.ylabel("Number of Issues")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(f"{save_dir}/3.monthly_issues.png")
    plt.close()

    # Fetch Repo Metadata (for stars/forks)
    print("=== Fetching repo metadata ===")
    repo_meta = {}
    for repo in repos:
        url = f"https://api.github.com/repos/{repo}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            repo_meta[repo] = {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0)
            }
        else:
            print(f"Error fetching {repo}: {response.status_code}")
            repo_meta[repo] = {"stars": None, "forks": None}

    # 4. A Bar Chart to plot the stars for every Repo
    print("=== 4. Stars Chart ===")
    stars_data = {repo: meta["stars"] for repo, meta in repo_meta.items()}
    sorted_stars = dict(sorted(stars_data.items(
    ), key=lambda item: item[1] if item[1] is not None else -1, reverse=True))

    plt.figure(figsize=(12, 6))
    plt.bar(sorted_stars.keys(), sorted_stars.values(), color="orange")
    plt.title("GitHub Stars per Repository")
    plt.ylabel("Stars Count")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(f"{save_dir}/4.repo_stars.png")
    plt.close()

    # 5. A Bar Chart to plot the forks for every Repo
    print("=== 5. Forks Chart ===")
    forks_data = {repo: meta["forks"] for repo, meta in repo_meta.items()}
    sorted_forks = dict(sorted(forks_data.items(
    ), key=lambda item: item[1] if item[1] is not None else -1, reverse=True))

    plt.figure(figsize=(12, 6))
    plt.bar(sorted_forks.keys(), sorted_forks.values(), color="skyblue")
    plt.title("GitHub Forks per Repository")
    plt.ylabel("Forks Count")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(f"{save_dir}/5.repo_forks.png")
    plt.close()

    # 6. A Bar Chart to plot the issues closed for every week for every Repo
    print("=== 6. Weekly Closed Issues ===")
    closed_df = df.dropna(subset=["closed_at"]).copy()
    closed_df["week"] = closed_df["closed_at"].dt.to_period(
        "W").apply(lambda r: r.start_time)
    weekly_closed_df = closed_df.groupby(
        ["week", "repo"]).size().reset_index(name="closed_count")
    pivot_df = weekly_closed_df.pivot(
        index="week", columns="repo", values="closed_count").fillna(0)

    pivot_df.plot(kind="bar", stacked=False, figsize=(18, 7), width=0.9)
    plt.title("Weekly Closed Issues per Repository")
    plt.xlabel("Week")
    plt.ylabel("Closed Issues Count")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.legend(title="Repository", bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"{save_dir}/6.weekly_closed_issues.png")
    plt.close()

    # 7. A Stack-Bar Chart to plot the created and closed issues for every Repo
    print("=== 7. Created vs Closed (Stacked Bar) ===")
    created_counts = df.groupby("repo")["created_at"].count()
    closed_counts = df["closed_at"].notna().groupby(df["repo"]).sum()
    summary_df = pd.DataFrame(
        {"Created": created_counts, "Closed": closed_counts})

    summary_df.plot(kind="bar", stacked=True, figsize=(
        12, 6), color=["#66c2a5", "#fc8d62"])
    plt.title("Issues Created vs Closed per Repository")
    plt.xlabel("Repository")
    plt.ylabel("Number of Issues")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Issue Type")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(f"{save_dir}/7.created_vs_closed_stacked.png")
    plt.close()

    print("PartI 1-7 All done!")


if __name__ == "__main__":
    main()
