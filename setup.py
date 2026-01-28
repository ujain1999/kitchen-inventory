import subprocess
import sys
from pathlib import Path
import getpass


VENV_PATH = Path(".venv")
ENV_FILE = Path(".env")
REQUIRED_VARS = ["DISCORD_TOKEN", "GUILD_ID"]

def ensure_python():
    try:
        print("Checking Python version")
        python_install_yn = input("Install Python version from .python-version? [Y/n]: ")
        if python_install_yn.lower() in ("", "y", "yes", "\n"):
            subprocess.run(
                ["uv", "python", "install"],
                check=True,
                stdout=subprocess.DEVNULL,
            )
        else:
            print("Skipping Python installation")
    except subprocess.CalledProcessError:
        print("Failed to install Python version from .python-version")
        sys.exit(1)

def ensure_venv():
    if VENV_PATH.exists():
        print(".venv already exists")
        return

    try:
        subprocess.run(
            ["uv", "venv"],
            check=True,
        )
        print(".venv created")
    except subprocess.CalledProcessError:
        print("Failed to create virtual environment")
        sys.exit(1)

def parse_env(contents: str) -> dict:
    env = {}
    for line in contents.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env

def ensure_env():
    env_data = {}

    if ENV_FILE.exists():
        env_data = parse_env(ENV_FILE.read_text())
        print(".env file found")
    else:
        print(".env file not found — creating one")

    updated = False

    for var in REQUIRED_VARS:
        if var not in env_data or not env_data[var]:
            if var == "DISCORD_TOKEN":
                value = getpass.getpass("Enter value for DISCORD_TOKEN: ").strip()
            else:
                value = input(f"Enter value for {var}: ").strip()
            env_data[var] = value
            updated = True

    if updated or not ENV_FILE.exists():
        with ENV_FILE.open("w") as f:
            for key, value in env_data.items():
                f.write(f"{key}={value}\n")
        print(".env file updated")

    print("Note: If you need to change these values, edit the .env file directly.")



if __name__ == "__main__":
    ensure_python()
    ensure_venv()
    ensure_env()
    print("Setup complete.")