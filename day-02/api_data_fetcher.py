import requests
import sys
import json


def fetch_github_user(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    data = response.json()

    user_info = {
        "username": data.get("login"),
        "name": data.get("name"),
        "public_repos": data.get("public_repos"),
        "followers": data.get("followers"),
        "following": data.get("following")
    }

    return user_info


def display_user_info(user_info):
    print("\nGitHub User Information:")
    for key, value in user_info.items():
        print(f"{key}: {value}")


def save_to_file(data):
    with open("github_user.json", "w") as file:
        json.dump(data, file, indent=4)


def main():
    # Bonus: CLI argument
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = "KhushiKachhawaha14"

    user_info = fetch_github_user(username)

    display_user_info(user_info)
    save_to_file(user_info)

    print("\n✅ Data saved to github_user.json")


if __name__ == "__main__":
    main()
