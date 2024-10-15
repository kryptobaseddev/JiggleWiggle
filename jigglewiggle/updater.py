import requests

def check_for_updates(current_version):
    try:
        response = requests.get("https://example.com/latest_version.txt")  # Replace with your actual URL
        response.raise_for_status()  # Check if the request was successful
        latest_version = response.text.strip()

        # Check if the response is in the correct format
        if len(latest_version.split(".")) == 3 and latest_version.replace(".", "").isdigit():
            return latest_version
        else:
            print(f"Unexpected response format: {latest_version}")
            return current_version  # If the format is unexpected, return the current version

    except Exception as e:
        print(f"Failed to check for updates: {e}")
        return current_version
