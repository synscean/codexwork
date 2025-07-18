# Pygame Environment Template

This repository provides a simple template for setting up a Python virtual environment with the latest stable version of `pygame`.

## Prerequisites

- Python 3.8 or newer installed on your system.

## Setup Instructions

1. **Create the virtual environment and install dependencies.**

   ```bash
   python scripts/setup_env.py
   ```

   The script will create a virtual environment in the `venv` directory, upgrade `pip`, and install `pygame` along with any other dependencies listed in `requirements.txt`.

2. **Activate the virtual environment.**

   On Linux or macOS:

   ```bash
   source venv/bin/activate
   ```

   On Windows (cmd):

   ```cmd
   venv\Scripts\activate
   ```

   On Windows (PowerShell):

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Run the example program.**

   ```bash
   python src/main.py
   ```

   You should see an empty window created by `pygame`. Close the window to exit the program.

## Project Structure

- `requirements.txt` – Python package requirements, specifying a modern `pygame` version.
- `scripts/setup_env.py` – Script to create and configure the virtual environment.
- `src/main.py` – Minimal example demonstrating that `pygame` works correctly.
- `.gitignore` – Keeps generated files such as the virtual environment out of version control.

Feel free to modify or expand this template to suit your project needs.
