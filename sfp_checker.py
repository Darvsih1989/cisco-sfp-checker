import paramiko
import time
import threading
import getpass
import tkinter as tk
from tkinter import filedialog
import pyfiglet  # Import ASCII art module

# Open file dialog to select input file
root = tk.Tk()
root.withdraw()  # Hide the root window
input_file = filedialog.askopenfilename(title="Select Router List File", filetypes=[("Text Files", "*.txt")])

# Exit if no file is selected
if not input_file:
    print("No file selected. Exiting...")
    exit()

# Output file
output_file = "active_sfp_routers.txt"

# User input for credentials
username = input("Enter SSH username: ")
password = getpass.getpass("Enter SSH password: ")  # Hides password input

# Commands
model_command = "show version | include Model"
sfp_command = "show interfaces status | include SFP"

# Thread lock for writing to file safely
lock = threading.Lock()

def check_router(ip):
    """SSH into a router, verify model, and check for active SFP ports."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"Connecting to {ip}...")
        client.connect(ip, username=username, password=password, timeout=10)

        # Open shell
        shell = client.invoke_shell()
        time.sleep(1)
        shell.send("terminal length 0\n")  # Disable pagination
        time.sleep(1)

        # Send model command
        shell.send(model_command + "\n")
        time.sleep(2)
        output = shell.recv(5000).decode("utf-8")

        if "ISR 4221" not in output:  # Checking for ISR 4221
            print(f"{ip} is not a Cisco ISR 4221 router.")
            client.close()
            return

        # Send SFP command
        shell.send(sfp_command + "\n")
        time.sleep(2)
        sfp_output = shell.recv(5000).decode("utf-8")

        client.close()

        # Check if any SFP ports are "connected"
        active_sfp_ports = [line for line in sfp_output.split("\n") if "connected" in line.lower()]

        if active_sfp_ports:
            print(f"{ip} has active SFP ports.")
            with lock:
                with open(output_file, "a") as f_out:
                    f_out.write(ip + "\n")

    except Exception as e:
        print(f"Error connecting to {ip}: {e}")

def main():
    with open(input_file, "r") as f:
        router_ips = [line.strip() for line in f.readlines()]

    threads = []
    for ip in router_ips:
        thread = threading.Thread(target=check_router, args=(ip,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Task completed.")

    # Print ASCII art of "ABBAS"
    ascii_art = pyfiglet.figlet_format("ABBAS")
    print(ascii_art)

if __name__ == "__main__":
    main()
