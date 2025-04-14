# Auto Upload to Calliope Mini

Automatically watches a folder for `.hex` files and transfers them to your connected **Calliope Mini** device. Comes with a simple GUI to change settings like watch folder, device drive letter, and check interval.

## ✨ Features

- Automatically uploads `.hex` files to Calliope Mini when dropped into a specified folder
- Customizable watch folder, check interval, and Calliope drive path
- Easy-to-use graphical interface
- Simple config file for persistent settings

## 📷 Screenshot

&#x20;

## 🧰 Installation

There are three ways to install and use this tool:

### 1. 🔽 Download Pre-Compiled EXE (Recommended)

- Go to the [Releases](https://github.com/pauwol/calliope-auto-upload/releases) tab
- Download the latest `.exe` file for Windows
- Double-click to run, no installation needed!

### 2. ⚙️ Compile It Yourself

- Clone or download this repo
- Make sure you have Python 3.10+ installed
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Compile with `pyinstaller`:
  ```bash
  pyinstaller --onefile --windowed --add-data "calliope.ico;." --icon=calliope.ico CalliSync.py
  ```
  > Note: `pyinstaller` can be installed using
  > ```bash
  > pip install pyinstaller
  > ```
- Run the generated executable in the `dist/` folder

### 3. 🐍 Run with Python

- Clone this repo:
  ```bash
  git clone https://github.com/pauwol/calliope-auto-uploader.git
  cd calliope-auto-uploader
  ```
- Install requirements:
  ```bash
  pip install -r requirements.txt
  ```
- Run:
  ```bash
  python CalliSync.py
  ```

## ⚙️ Configuration

Settings are stored in a `config.json` file and include:

- Watch folder (default: `%USERPROFILE%/Downloads/calliope-upload`)
- Calliope drive letter (e.g., `E:/`)
- File check interval in seconds

You can change them anytime using the graphical interface.

## 🧑‍💻 License

MIT License

---

> A small utility to streamline your workflow with the Calliope Mini microcontroller. Drop and go!

