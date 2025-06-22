# GhostNote

A simple, lightweight Windows tray application for fast, system-wide speech-to-text using OpenAI's Whisper API. Hold a hotkey, speak, release, and have the transcribed text appear anywhere you can type.

![GhostNote Demo](https://place-a-gif-here.com)  

---

## Features

- **System-Wide Hotkey**: Press `Left Alt + \` to start/stop recording from any application.
- **Visual Feedback**: A system tray icon turns red while recording, so you always know when it's listening.
- **Lightweight**: Runs quietly in your system tray with minimal resource usage.
- **Simple & Fast**: No complicated setup. Just add your API key and run.

## The "Why"

This project was inspired by the idea that speech-to-text shouldn't require an expensive subscription. It's a minimal, no-frills tool for developers, writers, or anyone who wants to dictate text without being tied to a specific app or browser window.

## Installation & Setup

Follow these steps to get GhostNote running on your machine.

**1. Clone the Repository**
```bash
git clone <your-repository-url>
cd GhostNote
```

**2. Create a Virtual Environment (Recommended)**

To avoid conflicts with other Python packages, it's best to use a virtual environment.

```bash
# Create the environment
python -m venv venv

# Activate it (on Windows)
.\venv\Scripts\activate
```

**3. Install Dependencies**

Install all the necessary Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**4. Set Up Your API Key**

The application uses your personal OpenAI API key.

- Create a new file in the `GhostNote` directory named `.env`.
- Open the `.env` file and add the following line, pasting your own secret key from the [OpenAI Platform](https://platform.openai.com/api-keys).

```
OPENAI_API_KEY="YOUR_API_KEY_HERE"
```
The `.gitignore` file is configured to prevent this file from ever being uploaded to GitHub.

## Usage

Once the setup is complete, simply run the application from your terminal:

```bash
python main.py
```

A grey circle icon will appear in your system tray.

- **To Record**: Press and hold `Left Alt + \`. The tray icon will turn red.
- **To Stop**: Release the keys. The icon will turn grey, and the transcribed text will be typed into your currently active window.
- **To Quit**: Right-click the tray icon and select "Quit".

## Configuration

The hotkey can be easily changed by modifying the `HOTKEY` variable at the top of the `main.py` file.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details. 
