import requests
import subprocess
from statistics import median


def get_github_data(username, repo):
    url = f'https://api.github.com/repos/{username}/{repo}'
    response = requests.get(url)
    return response.json(), response.headers.get('stargazers-count')


def get_commits_count(username, repo):
    url = f'https://api.github.com/repos/{username}/{repo}/commits'
    response = requests.get(url)
    return len(response.json())


def get_stars_count(username, repo):
    url = f'https://api.github.com/repos/{username}/{repo}/stars'
    response = requests.get(url)
    return len(response.json())


def get_contributors_count(username, repo):
    contributors_url = f'https://api.github.com/repos/{username}/{repo}/contributors'
    response = requests.get(contributors_url)
    return len(response.json())


def get_branches_count(username, repo):
    branches_url = f'https://api.github.com/repos/{username}/{repo}/branches'
    response = requests.get(branches_url)
    return len(response.json())


def get_tags_count(username, repo):
    tags_url = f'https://api.github.com/repos/{username}/{repo}/tags'
    response = requests.get(tags_url)
    return len(response.json())


def get_forks_count(username, repo):
    forks_url = f'https://api.github.com/repos/{username}/{repo}/forks'
    response = requests.get(forks_url)
    return len(response.json())


def get_releases_count(username, repo):
    releases_url = f'https://api.github.com/repos/{username}/{repo}/releases'
    response = requests.get(releases_url)
    return len(response.json())


def get_closed_issues_count(username, repo):
    closed_issues_url = f'https://api.github.com/repos/{username}/{repo}/issues?state=closed'
    response = requests.get(closed_issues_url)
    return len(response.json())


def get_environments_count(username, repo):
    environments_url = f'https://api.github.com/repos/{username}/{repo}/environments'
    response = requests.get(environments_url)
    return len(response.json())


def get_lines_of_code(repo):
    command = r'F:\Code --json --quiet {repo}'
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    lines_of_code = result.stdout
    return lines_of_code


def main():
    username = 'Kaggle'
    repos = ['docker-python', 'docker-rstats', 'kagglehub', 'docker-rcran', 'kaggle-environments',
             'kaggle-api', 'learntools', '.allstar', '.github', 'jupyterlab', 'docker-julia',
             'pipelinehelpers']  # Add all Kaggle repositories

    total_commits = []
    total_stars = []
    total_contributors = []
    total_branches = []
    total_tags = []
    total_forks = []
    total_releases = []
    total_closed_issues = []
    total_environments = []
    total_lines_of_code = []

    for repo in repos:
        data, star_count = get_github_data(username, repo)

        total_commits.append(get_commits_count(username, repo))
        if star_count is not None:
            total_stars.append(int(star_count))
        else:
            total_stars.append(0)
        total_contributors.append(get_contributors_count(username, repo))
        total_branches.append(get_branches_count(username, repo))
        total_tags.append(get_tags_count(username, repo))
        total_forks.append(get_forks_count(username, repo))
        total_releases.append(get_releases_count(username, repo))
        total_closed_issues.append(get_closed_issues_count(username, repo))
        total_environments.append(get_environments_count(username, repo))

        lines_of_code = get_lines_of_code(repo)
        total_lines_of_code.append(lines_of_code)

    median_commits = median(total_commits)
    median_stars = median(total_stars)
    median_contributors = median(total_contributors)
    median_branches = median(total_branches)
    median_tags = median(total_tags)
    median_forks = median(total_forks)
    median_releases = median(total_releases)
    median_closed_issues = median(total_closed_issues)
    median_environments = median(total_environments)

    print(f'Total Commits: {sum(total_commits)}, Median Commits: {median_commits}')
    print(f'Total Stars: {sum(total_stars)}, Median Stars: {median_stars}')
    print(f'Total Contributors: {sum(total_contributors)}, Median Contributors: {median_contributors}')
    print(f'Total Branches: {sum(total_branches)}, Median Branches: {median_branches}')
    print(f'Total Tags: {sum(total_tags)}, Median Tags: {median_tags}')
    print(f'Total Forks: {sum(total_forks)}, Median Forks: {median_forks}')
    print(f'Total Releases: {sum(total_releases)}, Median Releases: {median_releases}')
    print(f'Total Closed Issues: {sum(total_closed_issues)}, Median Closed Issues: {median_closed_issues}')
    print(f'Total Environments: {sum(total_environments)}, Median Environments: {median_environments}')

    # Print lines of code per language
    print('\nLines of Code per Language:')
    for language, lines_count in sum(total_lines_of_code).items():
        print(f'{language}: {lines_count}')


if __name__ == "__main__":
    main()
