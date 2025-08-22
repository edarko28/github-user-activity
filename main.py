import json
import sys
import requests

def load_api(nickname: str) -> requests.Response | str | None:
    "Function to load a github api for a user."
    response = requests.get(f"https://api.github.com/users/{nickname}/events")
    match response.status_code:
        case 200:
            return response
        case 404:
            return f"User {nickname} has not been found."
        case int():
            return f"API error appeared: code {response.status_code}"
    return None


def detect_activity(activity: list) -> list:
    'Function to detect activity based on  the API data for a specified user.'
    github_activity = []
    if len(activity) <= 0:
        return github_activity
    for i in range(len(activity)):
        event_type = activity[i]['type']
        repo_name = activity[i]['repo']['name']
        events = {"WatchEvent": {"message": f"Starred {repo_name}."},
                  "CommitCommentEvent": {"message": f"Commented on a commit in {repo_name}."}, "CreateEvent": {
                "message": f"Created a new {activity[i]['payload']['ref_type'] if event_type == 'CreateEvent' else None} in {repo_name}."},
                  "DeleteEvent": {
                      "message": f"Deleted a {activity[i]['payload']['ref_type'] if event_type == 'DeleteEvent' else None} in {repo_name}."},
                  "ForkEvent": {"message": f"Forked {repo_name}."}, "IssueCommentEvent": {
                "message": f"{activity[i]['payload']['action'].capitalize() if event_type == 'IssueCommentEvent' else None} a comment on issue #{activity[i]['payload']['issue']['number'] if event_type == 'IssueCommentEvent' else None} at {repo_name}."},
                  "IssuesEvent": {
                      "message": f"{activity[i]['payload']['action'].capitalize() if event_type == 'IssuesEvent' else None} an issue in {repo_name}."},
                  "PushEvent": {
                      "message": f"Pushed {activity[i]['payload']['size'] if event_type == 'PushEvent' else None} commits to {repo_name}."},
                  "PullRequestEvent": {
                      "message": f"{activity[i]['payload']['action'].capitalize() if event_type == 'PullRequestEvent' else None} a pull request #{activity[i]['payload']['number'] if event_type == 'PullRequestEvent' else None} in {repo_name}."},
                  "PullRequestReviewEvent": {
                      "message": f"{activity[i]['payload']['action'].capitalize() if event_type == 'PullRequestReviewEvent' else None} a review on pull request #{activity[i]['payload']['pull_request']['number'] if event_type == 'PullRequestReviewEvent' else None} in {repo_name}."},
                  "PullRequestReviewCommentEvent": {
                      "message": f"Commented on a review for pull request #{activity[i]['payload']['pull_request']['number'] if event_type == 'PullRequestReviewCommentEvent' else None} in {repo_name}."},
                  "MemberEvent": {
                      "message": f"{activity[i]['payload']['action'].capitalize() if event_type == 'MemberEvent' else None} member {activity[i]['payload']['member']['login'] if event_type == 'MemberEvent' else None} in {repo_name}."}}
        if event_type in events:
            github_activity.append(events[event_type]["message"])
    return github_activity

def save_to_file(activity_list: list, username: str) -> str:
    "Function to save user's activity data to a txt file."
    with open(f"{username}_activity.txt", "w", encoding="utf-8") as file:
        for element in activity_list:
            file.write(str(element) + "\n")
    return "Activity saved to file successfully."


def main() -> None:
    """
    Main function of the program.
    """
    username = sys.argv[1]
    api_result = load_api(username)
    if isinstance(api_result, requests.Response):
        data = json.loads(load_api(username).text)
        print(save_to_file(detect_activity(data), username))
    else:
        print(api_result if api_result is not None else "Unknown error occurred while loading API.")
        sys.exit(-1)


if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print("Error: Invalid usage. Proper command format: github-activity <username>")
        sys.exit(-1)