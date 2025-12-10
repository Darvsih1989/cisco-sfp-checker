Cisco ISR 4221 SFP Checker

A Python automation tool for identifying Cisco ISR 4221 routers with active SFP ports, using SSH, multithreading, and a Tkinter-based GUI for selecting the device list file.


---

⭐ Features

SSH connection to multiple Cisco routers

Detects router model (ISR 4221 validation)

Extracts active SFP interfaces

Multithreaded execution for high performance

GUI file picker for selecting router list

Saves results into active_sfp_routers.txt

ASCII art output using pyfiglet

Error handling & safe file access using thread locks



---

📦 Requirements

Install dependencies:

pip install paramiko pyfiglet

Tkinter is included by default on Windows & Linux.
(If missing on Linux: sudo apt install python3-tk)


---

📁 Project Structure

.
├── sfp_checker.py          # Main script
├── routers.txt             # Sample router list file
├── active_sfp_routers.txt  # Generated output (ignored by git)
└── README.md               # Documentation


---

⚙️ How It Works

1. User selects a .txt file containing router IP addresses


2. Script connects via SSH using Paramiko


3. Verifies router model (ISR 4221)


4. Runs:

show version | include Model

show interfaces status | include SFP



5. Extracts lines containing active SFP ports


6. Writes router IPs with active SFP ports into active_sfp_routers.txt




---

▶️ Usage

Run the script:

python sfp_checker.py

Steps:

1. A file dialog appears → choose your router list .txt


2. Enter your SSH username


3. Enter your SSH password (hidden)


4. Script runs with multithreading


5. Output saved to:



active_sfp_routers.txt


---

📝 Sample routers.txt

192.168.1.1
192.168.1.2
10.10.20.5


---

💡 Example Output

active_sfp_routers.txt:

192.168.1.2
10.10.20.5


---

🛡️ Error Handling Included

Connection timeout

Authentication failure

Missing commands

Router not ISR 4221

Empty or invalid IP list



---

🎨 ASCII Output

At the end of execution, the script prints:

ABBAS

(created using pyfiglet)



