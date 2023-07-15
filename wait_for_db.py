import time
import socket

def wait_for_db():
    db_host = "db"
    db_port = 3306
    max_retries = 100

    for _ in range(max_retries):
        try:
            with socket.create_connection((db_host, db_port), timeout=1):
                print("The db service is now healthy.")
                return
        except (ConnectionRefusedError, socket.timeout):
            print("Waiting for the db service to become healthy...")
            time.sleep(1)

    print("Failed to wait for the db service.")

if __name__ == "__main__":
    wait_for_db()
