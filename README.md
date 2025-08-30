# Pygame Meteor Avoidance Game

This repository contains a vertical-scrolling meteor avoidance game built with `pygame`. The player controls an upward-facing spaceship and dodges falling meteors while stars stream by in the background.

## Prerequisites

- Python 3.8 or newer installed on your system.

## Setup Instructions

1. **Create the virtual environment and install dependencies.**

   ```bash
   python scripts/setup_env.py
   ```

   The script creates a virtual environment in the `venv` directory, upgrades `pip`, and installs `pygame` along with any other dependencies listed in `requirements.txt`.

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

3. **Download the image assets.**

   Place the following images in the `src/assets` directory:

   - [`spaceship.png` (32x32)](https://assets.st-note.com/img/1744789155-ng0pqZm3B21t4yasCFDVUf5T.png)
   - [`meteor.png` (32x32)](https://assets.st-note.com/img/1744789160-n6wZcxUK2vbAs1FodlQmVOTR.png)
   - [`explosion.png` (48x48)](https://assets.st-note.com/img/1744789165-fybnWPSqovDgrG8tH1wjh5lm.png)

   If the images are not available, the program will use magenta placeholders.

4. **Run the game.**

   ```bash
   python src/main.py
   ```

   Use the left and right arrow keys to avoid the falling meteors. The game ends when the spaceship is hit and an explosion occurs.

## Project Structure

- `requirements.txt` – Python package requirements specifying a modern `pygame` version.
- `scripts/setup_env.py` – Script to create and configure the virtual environment.
- `src/main.py` – Game implementation.
- `src/assets/` – Directory for image assets used by the game.
- `.gitignore` – Keeps generated files such as the virtual environment out of version control.
