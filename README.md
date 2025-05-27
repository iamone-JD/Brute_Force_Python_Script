# Script BF - Brute-Force Login Tester

This script is designed to test the security of web login forms by attempting to guess usernames and passwords. It reads potential usernames from `users.txt` and passwords from `pswd.txt` files respectively.

## Disclaimer

**This tool is intended for educational and authorized security testing purposes ONLY.**

*   **Ethical Use:** You must have explicit, written permission from the website owner before using this script on any system you do not own or have permission to test. Unauthorized use of this script against any system is illegal and unethical.
*   **Responsibility:** The authors and contributors of this script are not responsible for any misuse or damage caused by this script. You are solely responsible for your actions.
*   **Potential Consequences:** Be aware that using this script without authorization can lead to serious consequences, including legal action, account suspension, or IP blocking.

## Prerequisites

- Python 3.x
- The `requests` library

## Setup

1.  **Clone the repository (or download the files).**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Prepare wordlists:**
    *   Create a file named `users.txt` and populate it with potential usernames, one per line.
    *   Create a file named `pswd.txt` and populate it with potential passwords, one per line.
    *(Placeholder `users.txt` and `pswd.txt` files are provided. You should replace their content with your own wordlists for actual testing.)*

## Usage

1.  **Set the Target URL:**
    This script can be configured to target a specific URL via the `LOGIN_URL` environment variable.
    ```bash
    export LOGIN_URL='https://your-target-login-page.com/login'
    ```
    If `LOGIN_URL` is not set, it will default to `https://0a18005104b93cc6810b70d700d200d4.web-security-academy.net/login`.

2.  **Run the script:**
    ```bash
    python script_BF.py
    ```

The script will attempt to log in using the provided usernames and passwords. It will print its progress and any successful credentials found.

## How it Works

The script sends POST requests to the specified login URL with username and password combinations.
- It uses a `ThreadPoolExecutor` to perform multiple attempts concurrently.
- It checks the response text for specific messages like "Invalid username" or "Incorrect password" to determine the outcome of each attempt.
- If a valid credential pair is found, the script will print them and exit.
- A small delay (`time.sleep(0.5)`) is included between attempts for the same user to reduce the chances of detection, though this may not be sufficient for all targets.

## Modifying the Script

- **Target URL:** Can be changed via the `LOGIN_URL` environment variable (see Usage).
- **Number of Threads:** Adjust `MAX_THREADS` in `script_BF.py` to control concurrency.
- **Wordlists:** Modify `users.txt` and `pswd.txt`.
- **Success/Failure Indicators:** If the target website uses different messages to indicate login success or failure, you will need to modify the checks in the `brute_force` function within `script_BF.py` (e.g., `if "Invalid username" in res.text:`).
