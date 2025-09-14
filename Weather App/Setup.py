#Author: Jakub Orlowski

#Setup for the weather app. Checks and asks you to install the directories if they arent present

import subprocess
import sys


def install_and_import(package):
    print(f"Attempting to install {package}. . .")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}. Please run 'pip install {package}' manually")
        return False

# List of required packages
required_packages = ["PyQt5", "requests", "dotenv"]
# Checking if packages are installed
missing_packages = []
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print("The Weather app required the following packages to run:")
    for package in missing_packages:
        print(f" - {package}")

    print("\nAttempting to install missing packages. . . ")
    for package in missing_packages:
        install_and_import(package)

    if not missing_packages:
        print("\nAll required packages are now installed You can run the weather app!")
else:
    print("All required packages are already installed. Ready to run the Weather app")
