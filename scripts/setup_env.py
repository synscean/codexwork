#!/usr/bin/env python3
"""Create a virtual environment and install dependencies in a cross-platform way."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import venv


def main() -> None:
    """Set up the virtual environment and install packages."""
    env_dir = Path("venv")

    if not env_dir.exists():
        # Create the venv with bundled pip so we can install packages
        venv.EnvBuilder(with_pip=True).create(env_dir)

    # Determine the path to the environment's pip executable and activation hint
    if sys.platform == "win32":
        pip_path = env_dir / "Scripts" / "pip.exe"
        activate_hint = f"{env_dir}\\Scripts\\activate"
    else:
        pip_path = env_dir / "bin" / "pip"
        activate_hint = f"source {env_dir}/bin/activate"

    # Upgrade pip itself
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
    # Install packages listed in requirements.txt
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)

    print(f"Virtual environment setup complete. Activate with '{activate_hint}'.")


if __name__ == "__main__":
    main()
