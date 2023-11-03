# Hiddify To Marzban Migrate Script

 | Simply Transfer Your Users From X-Ui to Marzban

## Table of Contents
- [About](#about)
- [Prerequisites](#prerequisites)
- [Linux](#Linux)
- [Windows](#windows)

Before running the script, ensure you update the following variables with your specific information in config.py:
```python
# Define Variables for Both Panels

# Hiddify Panel
# Example https://<DOMAIN>/<PROXY PATH>/<ADMIN TOKEN>

H_AUTH = "YOUR_ADDRESS" + "/api/v1/user/"

# Marzban Panel

M_DOMAIN = "YOUR_DOMAIN"
M_PORT = "YOUR_PORT"
M_USERNAME = "YOUR_USERNAME"
M_PASSWORD = "YOUR_PASSWORD"
M_HTTPS = False  # Set to True to use HTTPS, False to use HTTP
```

## About

This script is designed to simplify the transfer of user data from X-Ui to Marzban using the Marzban API. It securely logs into both panels, retrieves user data from X-Ui, and adds it to Marzban.

### Prerequisites
Python 3.0+ with the requests library is required. The script is not compatible with Python 2.0.
### Linux
```bash
# Clone the Repository
git clone https://github.com/ItsAML/Hiddify-to-Marzban.git

# Change Directory
cd X-Ui-to-Marzban

# Install pip (if not already installed)
wget -qO- https://bootstrap.pypa.io/get-pip.py | python3 -

# Install Dependencies
python3 -m pip install -r requirements.txt

# Run the Script
python3 main.py
```
### Windows
```bash
# Clone the Repository
git clone https://github.com/ItsAML/Hiddify-to-Marzban.git

# Navigate to the Repository Directory
cd X-Ui-to-Marzban

# Install Python (if not already installed)
# Download and install Python from https://www.python.org/downloads/
# Ensure you add Python to your system's PATH during installation

# Install Dependencies
pip install -r requirements.txt

# Run the Script
python main.py
```
# Support This Project

If you find my GitHub repository helpful and would like to support my work, you can make a donation using the following cryptocurrencies:

- **USDT (TRC20):** TPXehJNLDqhHBAfs6v5KKHKXX4fZ3uhVGK
- **TRX (TRC20):** TPXehJNLDqhHBAfs6v5KKHKXX4fZ3uhVGK

Your contributions are greatly appreciated and will help me continue developing and maintaining this project. Thank you for your support! 🙌

