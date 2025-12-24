import requests
import sys
import json

def fetch_github_user(username):
    """Fetches user data from GitHub API with error handling."""
    url = f"https://api.github.com/users/{username}"
    
    try:
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful (Status Code 200)
        # This raises an HTTPError if the status is 4xx or 5xx
        response.raise_for_status()
        
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"❌ Error: User '{username}' not found.")
        else:
            print(f"❌ HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Failed to connect to the internet.")
    except requests.exceptions.Timeout:
        print("❌ Error: The request timed out.")
    except Exception as err:
        print(f"❌ An unexpected error occurred: {err}")
    
    return None


def display_user_info(data):
    """Filters and displays user information."""
    user_info = {
        "Username": data.get("login"),
        "Name": data.get("name", "N/A"),
        "Public Repos": data.get("public_repos"),
        "Followers": data.get("followers"),
        "Following": data.get("following")
    }

    print("\n--- GitHub User Information ---")
    for key, value in user_info.items():
        print(f"{key}: {value}")
    return user_info


def save_to_file(data, filename="github_user.json"):
    """Saves data to a JSON file with exception handling."""
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"\n✅ Data successfully saved to {filename}")
    except IOError as e:
        print(f"❌ Error: Could not write to file. {e}")


def main():
    # Handle CLI arguments or default value
    username = sys.argv[1] if len(sys.argv) > 1 else "KhushiKachhawaha14"

    print(f"Fetching data for: {username}...")
    raw_data = fetch_github_user(username)

    # Only proceed if data was successfully fetched
    if raw_data:
        formatted_info = display_user_info(raw_data)
        save_to_file(formatted_info)
    else:
        print("⏭️ Skipping file save because no data was retrieved.")


if __name__ == "__main__":
    main()
